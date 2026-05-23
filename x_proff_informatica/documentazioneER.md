# Documentazione tabelle

## Tabella `app_periodi`

Memorizza i periodi di riferimento.

| Colonna | Tipo | Vincoli  | Funzione                                 |
|---------|------|----------|------------------------------------------|
| id      | int  | PK       | Chiave primaria                          |
| dataI   | date | not null | Data di inizio del priodo da selezionare |
| dataF   | date | not null | Data di fine del priodo da selezionare   |

---

## Tabella `app_progetto`

Memorizza le informazioni sui progetti aziendali.

| Colonna       | Tipo        | Vincoli  | Funzione                         |
|---------------|------------|-----------|---------------------------------|
| id            | int        | PK        | Chiave primaria                          |
| titolo        | varchar(255)| not null | Titolo del progetto       |
| descrizione   | text       | not null  | Descrizione del progetto |
| stato         | varchar(4) | not null  | Stato del progetto (es. "FINE", "NOTR", "NYST"), obbligatorio |
| data_consegna | date       | not null  | Data di consegna del progetto, obbligatoria |

---

## Tabella `app_teams`

Memorizza i team assegnati ai progetti.

| Colonna         | Tipo | Vincoli           | Funzione                                           |
|-----------------|------|-------------------|----------------------------------------------------|
| id              | int  | PK auto increment |Identificativo del team, parte della chiave primaria |
| num_min_persone | int  | not null | Numero minimo di membri richiesto, obbligatorio      |
| progetto_id     | int  | FOREIGN KEY -> `app_progetto(id)` | Riferimento al progetto in `app_progetto`, FK, parte della chiave primaria |

### Vincoli

- **Primary Key**: `(id, progetto_id)` -> un team è univoco per progetto.
- **Foreign Key**: `progetto_id` riferisce `app_progetto(id)` -> per ogni team può essere assegnato un progetto.

---

## Tabella `app_basedatauser`

Contiene tutto ciò che serve per la login, recupero credenziali e autorizzazioni

| Campo         | Tipo          | Vincoli      | Descrizione |
|----------------|---------------|---------------|-------------|
| id             | int           | PRIMARY KEY   | Identificatore univoco dell'utente |
| password       | varchar(128)  | NOT NULL      | Password cifrata dell'utente |
| last_login     | datetime      | NULL          | Data e ora dell'ultimo login effettuato |
| is_superuser   | boolean       | NOT NULL      | Indica se l'utente possiede tutti i permessi amministrativi |
| username       | varchar(150)  | UNIQUE      | Nome utente utilizzato per effettuare il login |
| first_name     | varchar(150)  | NOT NULL      | Nome dell'utente |
| last_name      | varchar(150)  | NOT NULL      | Cognome dell'utente |
| email          | varchar(254)  | UNIQUE      | Indirizzo email dell'utente |
| is_staff       | boolean       | NOT NULL      | Indica se l'utente può accedere al pannello admin |
| is_active      | boolean       | NOT NULL      | Indica se l'account è attivo |
| date_joined    | datetime      | NOT NULL      | Data e ora di registrazione dell'utente |

## Note

- La password non viene salvata in chiaro ma come hash.
- Gli utenti con `is_staff = true` possono accedere al pannello di amministrazione.
- Gli utenti con `is_superuser = true` hanno accesso completo a tutte le funzionalità amministrative.
- Se `is_active = false`, l'utente non può autenticarsi.

---

## Tabella `app_normaluser`

Memorizza informazioni aggiuntive sui normali utenti collegati all'utente base (`app_basedatauser`) e al team di appartenenza.

| Campo          | Tipo       | Vincoli                                   | Descrizione |
|----------------|------------|-------------------------------------------|-------------|
| id             | int        | primary_key auto_increment                | Identificatore univoco dell'utente all'interno della tabella specifica |
| codFisc        | varchar(16)| UNIQUE                                    | Codice fiscale dell'utente |
| dataN          | date       | NOT NULL                                  | Data di nascita dell'utente |
| task_assegnata | varchar(32)|                                           | Breve descrizione della task che deve svolgere il dipendente |
| user_id        | int        | FOREIGN KEY -> `app_basedatauser(id)`     | Riferimento all'utente base autenticabile |
| cod_team_id    | int        | FOREIGN KEY -> `app_teams(id)`            | Riferimento al team di appartenenza dell'utente |

### Vincoli e note

- La chiave primaria è composta da `(id, user_id, cod_team_id)`.
- `user_id` garantisce il collegamento con la tabella `app_basedatauser` per autenticazione e credenziali.
- `cod_team_id` lega l'utente a un team specifico nella tabella `app_teams`.
- La tabella permette di estendere le informazioni di utenti normali senza modificare direttamente la tabella degli utenti base.

---

## Tabella `app_ruoli`

Questa tabella permette di assegnare un ruolo a ciascun utente della tabella `app_normaluser`.

| Colonna   | Tipo      | Vincoli                    | Funzione                                                                         |
|-----------|-----------|----------------------------|----------------------------------------------------------------------------------|
| id        | int       |  PK, autoincrement         | Identificativo del ruolo (parte della chiave primaria)                           |
| ruolo     | varchar(4)|     not null                       | Codice del ruolo, obbligatorio (es. "DIPE" = Dipendente, "RESP" = Responsabile)  |
| user_id   | int       |  FOREIGN KEY -> `app_normaluser(id)` | Riferimento all'utente in `app_normaluser`, parte della chiave primaria, FK      |


### Vincoli

- **Primary Key**: `(id, user_id)` -> un utente può avere più ruoli, ma non duplicati identici.
- **Foreign Key**: `user_id` riferisce `app_normaluser(id)` -> garantisce che il ruolo appartenga a un utente esistente.

---

## Tabella `app_ferie`

Memorizza le richieste di ferie degli utenti e lo stato di approvazione.

| Colonna     | Tipo | Vincoli | Funzione                                      |
|------------|------|----------|-------------------------------------------|
| id         | int  | pk, autoincrement | Identificativo della richiesta, parte della chiave primaria |
| dataI      | date | not null | Data di inizio ferie, obbligatoria                  |
| dataF      | date | not null | Data di fine ferie, obbligatoria                    |
| stato      | int  | not null | Stato della richiesta (0=Rifiutata, 1=In attesa, 2=Accettata), obbligatorio |
| user_id    | int  | FOREIGN KEY -> `app_normaluser(id)` | Riferimento all'utente (`app_normaluser.id`), FK, parte della chiave primaria |
| periodo_id | int  | FOREIGN KEY -> `app_periodi(id)` | Periodo deciso dall'azienda |


### Vincoli

- **Primary Key**: `(id, user_id, periodo_id)` -> ogni richiesta è univoca per utente e periodo.
- **Foreign Key**: `user_id` riferisce `app_normaluser(id)` -> la richiesta deve appartenere a un utente esistente.
- **Foreign Key**: `periodo_id` riferisce `app_periodi(id)` -> la richiesta deve rientrare in un periodo definito.

---

## Tabella `app_messaggio`

Memorizza i messaggi scambiati tra gli utenti.

| Colonna          | Tipo | Vincoli/Funzione                                      |
|-----------------|------|------------------------------------------------------|
| id              | int  | Identificativo del messaggio, parte della chiave primaria |
| content         | text | Contenuto del messaggio, obbligatorio               |
| data            | real | Data e ora del messaggio (timestamp), obbligatorio  |
| destinatario_id | int  | Riferimento all'utente destinatario (`app_normaluser.id`), FK, parte della chiave primaria |
| mittente_id     | int  | Riferimento all'utente mittente (`app_normaluser.id`), FK, parte della chiave primaria |


## Vincoli e note

- **Primary Key**: `(id, destinatario_id, mittente_id)` → garantisce unicità dei messaggi per mittente/destinatario.
- **Foreign Key**: `destinatario_id` riferisce `app_normaluser(id)` → il destinatario deve essere un utente esistente.
- **Foreign Key**: `mittente_id` riferisce `app_normaluser(id)` → il mittente deve essere un utente esistente.

Ho deciso di usare il timestamp per la data del messaggio cosi' se implementero' in interfaccia web
la sezione per i messaggi, posso facilmente mostrare quanto tempo fa e' stato mandato il messaggio (30 secondi fa, 1 min fa, 1 giorno fa alle ore x)

---
### authors

- Piscitelli Damiano
- Bastianello Federico
- Soardo Yan Leonardo
- Padrini Raffaele
