# tests.py (o da incollare direttamente in django shell)

from datetime import date
from django.utils import timezone
from app.models import (
    Progetto, Teams, BaseDataUser, NormalUser,
    Ruoli, Messaggio, Periodi
)


'''
File che popola istanze di prova
'''


# --- progetto ---
progetto1 = Progetto.objects.create(
    titolo="Sistema Gestionale",
    descrizione="Sviluppo di un gestionale interno",
    stato="NOTR",
    data_consegna=date(2026, 6, 30)
)

# --- team ---
team1 = Teams.objects.create(
    num_min_persone=3,
    progetto=progetto1
)

# --- base users ---
base_user1 = BaseDataUser.objects.create_user(
    username="alice",
    password="password123",
    email="alice@example.com"
)

base_user2 = BaseDataUser.objects.create_user(
    username="bob",
    password="password123",
    email="bob@example.com"
)


base_user3 = BaseDataUser.objects.create_user(
    username="giacomo",
    password="password123",
    email="giacomo@example.com"
)

base_user4 = BaseDataUser.objects.create_user(
    username="lorem",
    password="password123",
    email="lorem@example.com"
)


base_user5 = BaseDataUser.objects.create_user(
    username="ipsum",
    password="password123",
    email="bastianellofederico4@gmail.com"
)

# --- Normal users ---
normal_user1 = NormalUser.objects.create(
    user_id=base_user1,
    cod_team=team1,
    codFisc="ALICEX00X00X000A",
    dataN=date(2000, 1, 1),
    task_assegnata="lorem ipsum dolor"
)

normal_user2 = NormalUser.objects.create(
    user_id=base_user2,
    cod_team=team1,
    codFisc="BOBXXX00X00X000B",
    dataN=date(1999, 5, 20),
    task_assegnata="lorem ipsum dolor"
)

normal_user3 = NormalUser.objects.create(
    user_id=base_user3,
    cod_team=team1,
    codFisc="GIACOX00X00X000A",
    dataN=date(2000, 1, 1),
    task_assegnata="lorem ipsum dolor"
)

normal_user4 = NormalUser.objects.create(
    user_id=base_user4,
    cod_team=team1,
    codFisc="GIOXXX00X00X000B",
    dataN=date(1999, 5, 20),
    task_assegnata="lorem ipsum dolor"
)

normal_user5 = NormalUser.objects.create(
    user_id=base_user5,
    cod_team=team1,
    codFisc="GIOGOX00X00X000A",
    dataN=date(2000, 1, 1),
    task_assegnata="lorem ipsum dolor"
)


# --- ruoli ---
ruolo1 = Ruoli.objects.create(
    user=normal_user1,
    ruolo="RESP"
)

ruolo2 = Ruoli.objects.create(
    user=normal_user2,
    ruolo="DIPE"
)

ruolo3 = Ruoli.objects.create(
    user=normal_user3,
    ruolo="DIPE"
)

ruolo4 = Ruoli.objects.create(
    user=normal_user4,
    ruolo="DIPE"
)

ruolo5 = Ruoli.objects.create(
    user=normal_user5,
    ruolo="DIPE"
)

# --- messaggio ---
msg1 = Messaggio.objects.create(
    content="Ciao, a che punto siamo con il progetto?",
    data=timezone.now().timestamp(),
    mittente=normal_user1,
    destinatario=normal_user2
)

# --- periodi ---
periodo1 = Periodi.objects.create(
    dataI=date(2026, 1, 1),
    dataF=date(2026, 1, 31)
)
