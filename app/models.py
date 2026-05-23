from django.db import models
from django.contrib.auth.models import AbstractUser


class Progetto(models.Model):
    # progetto che viene sviluppato dal team

    STATO_PROGETTO = [
        ('FINE', 'Ended'),                 # progetto finito
        ('NOTR', 'Not ready'),             # ancora non finito
        ('NYIM', 'Not yet started'),       # not yet started
    ]

    titolo = models.CharField(max_length=255)
    descrizione = models.TextField()
    stato = models.CharField(max_length=4, choices=STATO_PROGETTO)
    data_consegna = models.DateField()

    class Meta:
        verbose_name = "Progetto"
        verbose_name_plural = "Progetti"

    def __str__(self):
        return f'{self.titolo}'


class Teams(models.Model):
    num_min_persone = models.IntegerField()

    progetto = models.ForeignKey(
        Progetto,
        on_delete=models.CASCADE,
        related_name="lavorato",
        null=True,
        blank=True,
        default=None
    )

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"

    def __str__(self):
        return f'{self.id}'


class BaseDataUser(AbstractUser):
    def __str__(self):
        return f'{self.id} - {self.username}'


class NormalUser(models.Model):
    user_id = models.ForeignKey(
        BaseDataUser,
        on_delete=models.CASCADE,
        related_name="istanza",
    )

    cod_team = models.ForeignKey(
        Teams,
        on_delete=models.CASCADE,
        related_name="appartiene",
    )
    codFisc = models.CharField(max_length=16)
    dataN = models.DateField()
    task_assegnata = models.CharField(max_length=32, null=True)

    def __str__(self):
        return f'{self.user_id.username}'


class Ruoli(models.Model):
    RUOLI = [
        ('DIPE', 'Dipendente'),
        ('RESP', 'Responsabile'),
    ]

    user = models.ForeignKey(
        NormalUser,
        on_delete=models.CASCADE,
        related_name="possiede"
    )

    ruolo = models.CharField(max_length=4, choices=RUOLI)

    class Meta:
        verbose_name = "Ruolo"
        verbose_name_plural = "Ruoli"

    def __str__(self):
        return f'{self.ruolo} - {self.user.cod_team}'


class Messaggio(models.Model):
    content = models.TextField()
    data = models.FloatField()
    mittente = models.ForeignKey(
        NormalUser,
        on_delete=models.CASCADE,
        related_name="manda_messaggio"
    )
    destinatario = models.ForeignKey(
        NormalUser,
        on_delete=models.CASCADE,
        related_name="ricevi_messaggio"
    )

    class Meta:
        verbose_name = "Messaggio"
        verbose_name_plural = "Messaggi"


class Periodi(models.Model):
    dataI = models.DateField()
    dataF = models.DateField()

    class Meta:
        verbose_name = "Periodo"
        verbose_name_plural = "Periodi"

    def __str__(self):
        return f'{self.dataI} - {self.dataF}'


class Ferie(models.Model):
    user = models.ForeignKey(
        NormalUser,
        on_delete=models.CASCADE
    )
    dataI = models.DateField()
    dataF = models.DateField()
    # 0 = rifiutato
    # 1 = In attesa
    # 2 = accettato
    stato = models.IntegerField()

    periodo = models.ForeignKey(
        Periodi,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Ferie"
        verbose_name_plural = "Ferie"

    def __str__(self):
        return f'{self.dataI} - {self.dataF} - {self.stato}'
