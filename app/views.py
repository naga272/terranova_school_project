from django.shortcuts import (
    render, redirect, HttpResponse
)

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from .models import Ruoli, Ferie, Periodi, Teams
from .forms import StatoApprovazione, FerieForm
from datetime import timedelta
# import threading


def home(request):
    return render(request, "index.html")


def send_mail_user(email: str, oggetto: str, message: str):
    send_mail(
        subject=oggetto,
        message=message,
        from_email=None,    # usa DEFAULT_FROM_EMAIL di settings.py
        recipient_list=[email],
        fail_silently=False,
    )


def async_send_email(email: str, oggetto: str, message: str):
    '''
    threading.Thread(
        target=send_mail_user,
        args=(email=email, oggetto=oggetto, message=message)
    ).start()
    Per qualche ragione, l'host pythonanywhere non me lo lascia fare,
    quindi faccio semplicemente send_mail_user
    '''
    send_mail_user(email, oggetto, message)


@login_required
def cambia_stato_ferie(request):
    # si puo fare solo con richieste POST
    if request.method != "POST":
        return redirect("profile")

    form = StatoApprovazione(request.POST)
    if not form.is_valid():
        return HttpResponse(
                "Si è verificato un errore durante l'elaborazione della richiesta."
            )

    responsabile = Ruoli.objects.get(user_id=request.user.id)
    cod_team_responsabile = responsabile.user.cod_team

    # ruolo responsabile?
    if responsabile.ruolo != "RESP":
        raise PermissionDenied()

    # dati dal form
    nuovo_stato = form.cleaned_data["stato"]
    ferie_id = form.cleaned_data["ferie_id"]

    # chi ha prenotato il giorno di ferie
    richiedente_ferie = Ferie.objects.get(id=ferie_id).user

    # il responsabile deve poter accettare solo quelli del proprio team
    if richiedente_ferie.cod_team != cod_team_responsabile:
        raise PermissionDenied()

    # update stato per chi ha prenotato
    Ferie.objects.filter(id=ferie_id).update(stato=nuovo_stato)

    ferie_user = Ferie.objects.get(id=ferie_id)

    async_send_email(
        richiedente_ferie.user_id.email,
        "Stato delle ferie aggiornato",
        f"""
        Gentile {richiedente_ferie.user_id.username},

        La sua richiesta di ferie del giorno {ferie_user.dataI}
        è stata {'approvata' if nuovo_stato == 2 else 'rifiutata'}.

        Cordiali saluti.
        """
    )
    return redirect("profile")


def check_if_giorni_consecutivi(user, periodo, giorno):
    consecutivi = 1

    giorni_utente = list(
        Ferie.objects.filter(
            user=user.user,
            periodo=periodo
        ).values_list("dataI", flat=True)
    )

    giorni_utente.append(giorno)

    giorni_utente = sorted(set(giorni_utente))

    consecutivi = 1

    for i in range(1, len(giorni_utente)):
        giorno_corrente = giorni_utente[i]
        giorno_precedente = giorni_utente[i - 1]

        if giorno_corrente == giorno_precedente + timedelta(days=1):
            consecutivi += 1
        else:
            consecutivi = 1

        if consecutivi >= 5:
            return 1
    return 0


def check_failed_total_single_user(user, periodo):
    total_ferie_single_u = Ferie.objects.filter(
        user=user.user,
        periodo=periodo
    ).count()

    if total_ferie_single_u == 5:
        return 1

    return 0


def check_giorno_free_by_team(user, giorno):
    team_info = Teams.objects.filter(
        id=user.user.cod_team.pk
    )[0]

    in_ferie = Ferie.objects.filter(
        user__cod_team=team_info,
        stato=2,                 # solo ferie approvate
        dataI__lte=giorno,
        dataF__gte=giorno,
    ).count()

    min_presenze = team_info.num_min_persone
    tot_team = team_info.appartiene.count()

    presenti = tot_team - in_ferie

    puo_prendere_ferie = presenti - 1 >= min_presenze

    return puo_prendere_ferie


def add_ferie(request, user: Ruoli, periodo: Periodi):
    # data_selezionata
    form = FerieForm(request.POST)

    if not form.is_valid():
        return (0, "Error! something bad is happened!",)

    giorno = form.cleaned_data["data_selezionata"]

    if giorno.weekday() == 6:
        return (0, "Error! non puoi prenotare ferie di domenica",)

    if check_failed_total_single_user(user, periodo):
        return (0, "Error! stai tentando di prenotare per piu di 5 giorni in questo periodo!",)

    if check_if_giorni_consecutivi(user, periodo, giorno):
        return (0, "Error! non puoi prenotare 5 giorni consecutivi nello stesso periodo!",)

    if not check_giorno_free_by_team(user, giorno):
        return (0, "Error! troppe persone del tuo team hanno prenotato per questo giorno",)

    Ferie.objects.create(
        user=user.user,
        dataI=giorno,
        dataF=giorno,
        stato=1,
        periodo=periodo
    ).save()

    async_send_email(
        user.user.user_id.email,
        "Inserite con successo nuove ferie",
        f"""Gentile {user.user.user_id.username},
        Le scriviamo per informarle che le ferie del {giorno} sono state
        messe in stato di approvazione con successo.
        Attenda che un responsabile approvi o rifiuti la sua giornata di ferie
        """
    )

    return (1,)


@login_required
def profile(request):
    user = request.user
    user = Ruoli.objects.filter(user_id=user.id)[0]
    periodo = Periodi.objects.order_by("-id").first()
    storico_ferie = Ferie.objects.filter(user_id=user.user_id)[::-1]

    if request.method == "POST":
        response = add_ferie(request, user, periodo)

        if not response[0]:
            return render(
                request,
                "errors/errno.html",
                context={
                    "msg": response[1]
                }
            )
        return redirect("profile")

    ferie_pending_team = []
    if user.ruolo == "RESP":
        ferie_pending_team = Ferie.objects.filter(
            user__cod_team=user.user.cod_team,
            stato=1,
            periodo_id=periodo
        )[::-1]

    # ferie pending dell'utente corrente
    ferie_pending_user = Ferie.objects.filter(
        user=user.user,
        stato=1,
        periodo_id=periodo
    )

    giorni_pending = set()
    giorni_approvati = set()

    # richieste pending del team
    for ferie in ferie_pending_team:
        giorno = ferie.dataI
        while giorno <= ferie.dataF:
            giorni_pending.add(giorno.isoformat())
            giorno += timedelta(days=1)

    # richieste pending dell'utente corrente
    for ferie in ferie_pending_user:
        giorno = ferie.dataI
        while giorno <= ferie.dataF:
            giorni_pending.add(giorno.isoformat())
            giorno += timedelta(days=1)

    # ferie approvate dell'utente corrente
    ferie_approvate_user = Ferie.objects.filter(
        user=user.user,
        stato=2,
        periodo_id=periodo
    )

    for ferie in ferie_approvate_user:
        giorno = ferie.dataI
        while giorno <= ferie.dataF:
            giorni_approvati.add(giorno.isoformat())
            giorno += timedelta(days=1)

    context = {
        "periodo_start": periodo.dataI.isoformat(),
        "periodo_end": periodo.dataF.isoformat(),
        "user": user,
        "ferie_team": ferie_pending_team,
        "storico_ferie_user": storico_ferie,
        "giorni_pending": list(giorni_pending),
        "giorni_approvati": list(giorni_approvati),
    }

    return render(request, "profile.html", context)


def ratelimit_handler(request, exception):
    return render(
        request,
        "errors/errno.html",
        context={
            "msg": "Too many attempts. Please wait 1 minute before trying again."
        },
        status=429
    )
