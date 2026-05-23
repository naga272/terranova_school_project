
create database if not exists terranovadb;
use terranovadb;


create table if not exists app_periodi(
    id int auto_increment primary key,
    dataI date not null,
    dataF date not null
);


create table if not exists app_progetto(
    id int auto_increment primary key,
    titolo varchar(255) not null,
    descrizione text not null,
    stato varchar (4) not null,
    data_consegna date not null
);


create table if not exists app_teams(
    id int auto_increment,
    num_min_persone int not null,
    progetto_id int not null,
    
    primary key(id, progetto_id),
    foreign key (progetto_id) references app_progetto(id)
);


create table if not exists app_basedatauser(
    id int auto_increment primary key,
    password varchar(128) not null,
    last_login datetime,
    is_superuser boolean not null,
    username varchar(150) unique,
    first_name varchar(150) not null,
    last_name varchar(150) not null,
    email varchar(254) unique,
    is_staff boolean not null,
    is_active boolean not null,
    date_joined datetime not null 
);


create table if not exists app_normaluser(
    id int auto_increment,
    codFisc varchar(16) unique,
    dataN date not null,
    user_id int,
    cod_team_id int,
	task_assegnata varchar(32),  -- breve descrizione della task

    primary key(id, user_id, cod_team_id),
    foreign key (user_id) references app_basedatauser(id),
    foreign key (cod_team_id) references app_teams(id)
);


create table if not exists app_ruoli(
    id int auto_increment,
    ruolo varchar(4) not null,
    user_id int,
    
    primary key(id, user_id),
    foreign key (user_id) references app_normaluser(id)
);


create table if not exists app_ferie(
    id int auto_increment,
    dataI date not null,
    dataF date not null,
    stato int not null,
    user_id int,
    periodo_id int,
    
    primary key(id, user_id, periodo_id),
    foreign key (user_id) references app_normaluser(id),
    foreign key (periodo_id) references app_periodi(id)
);


create table if not exists app_messaggio(
    id int auto_increment,
    content text not null,
    data real not null,     -- timestamp, documentazione spiega il perche
    destinatario_id int,
    mittente_id int,
    primary key(id, destinatario_id, mittente_id),
    foreign key (destinatario_id) references app_normaluser(id),
    foreign key (mittente_id) references app_normaluser(id)
);


-- Inserimento periodi
INSERT INTO app_periodi (dataI, dataF) VALUES
('2026-04-01', '2026-04-30'),
('2026-05-01', '2026-05-31');

-- Inserimento progetto
INSERT INTO app_progetto (titolo, descrizione, stato, data_consegna) VALUES
('Sito Web Aziendale', 'Progetto per la creazione di un sito web aziendale completo', 'NYST', '2026-06-30');


-- Inserimento team
INSERT INTO app_teams (tot_num_persone, num_min_persone, progetto_id) VALUES
(7, 2, 1);


-- Inserimento utenti BaseDataUser
INSERT INTO app_basedatauser (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES
('pbkdf2_sha256$260000$admin$hashedpassword', NULL, 1, 'admin', 'Admin', 'Superuser', 'admin@example.com', 1, 1, '2026-04-01'),
('pbkdf2_sha256$260000$user1$hashedpassword', NULL, 0, 'user1', 'Mario', 'Rossi', 'mario.rossi@example.com', 0, 1, '2026-04-01'),
('pbkdf2_sha256$260000$user2$hashedpassword', NULL, 0, 'user2', 'Luca', 'Bianchi', 'luca.bianchi@example.com', 0, 1, '2026-04-01'),
('pbkdf2_sha256$260000$user3$hashedpassword', NULL, 0, 'user3', 'Giulia', 'Verdi', 'giulia.verdi@example.com', 0, 1, '2026-04-01'),
('pbkdf2_sha256$260000$user4$hashedpassword', NULL, 0, 'user4', 'Francesca', 'Neri', 'francesca.neri@example.com', 0, 1, '2026-04-01'),
('pbkdf2_sha256$260000/user5$hashedpassword', NULL, 0, 'user5', 'Davide', 'Gialli', 'davide.gialli@example.com', 0, 1, '2026-04-01'),
('pbkdf2_sha256$260000/user6$hashedpassword', NULL, 0, 'user6', 'Alice', 'Blu', 'alice.blu@example.com', 0, 1, '2026-04-01'),
('pbkdf2_sha256$260000/user7$hashedpassword', NULL, 0, 'user7', 'Matteo', 'Viola', 'matteo.viola@example.com', 0, 1, '2026-04-01');


-- Inserimento normalUser con ruoli
INSERT INTO app_normaluser (codFisc, dataN, user_id, cod_team_id) VALUES
('RSSMRA80A01H501U', '1980-01-01', 2, 1),
('BNCLCU85B12H501V', '1985-02-12', 3, 1),
('VRDGLI90C23H501X', '1990-03-23', 4, 1),
('NRSFNC95D04H501Y', '1995-04-04', 5, 1),
('GLLDVD92E15H501Z', '1992-05-15', 6, 1),
('BLUALC88F06H501W', '1988-06-06', 7, 1),
('VLTMTT93G17H501T', '1993-07-17', 8, 1);


-- Inserimento ruoli
INSERT INTO app_ruoli (ruolo, user_id) VALUES
('RESP', 1),  -- responsabile del team
('DIPE', 2),
('DIPE', 3),
('DIPE', 4),
('DIPE', 5),
('DIPE', 6),
('DIPE', 7);

-- Inserimento ferie
-- Utente 2
INSERT INTO app_ferie (dataI, dataF, stato, user_id, periodo_id) VALUES
('2026-04-02', '2026-04-02', 2, 2, 1),
('2026-04-05', '2026-04-06', 2, 2, 1),
('2026-04-10', '2026-04-10', 2, 2, 1),
('2026-04-15', '2026-04-15', 2, 2, 1),
('2026-04-20', '2026-04-21', 2, 2, 1);

-- Utente 3
INSERT INTO app_ferie (dataI, dataF, stato, user_id, periodo_id) VALUES
('2026-04-03', '2026-04-03', 2, 3, 1),
('2026-04-07', '2026-04-07', 2, 3, 1),
('2026-04-12', '2026-04-12', 2, 3, 1),
('2026-04-18', '2026-04-18', 2, 3, 1),
('2026-04-25', '2026-04-25', 2, 3, 1);

-- Utente 4
INSERT INTO app_ferie (dataI, dataF, stato, user_id, periodo_id) VALUES
('2026-04-04', '2026-04-04', 2, 4, 1),
('2026-04-08', '2026-04-09', 2, 4, 1),
('2026-04-13', '2026-04-13', 2, 4, 1),
('2026-04-19', '2026-04-19', 2, 4, 1),
('2026-04-22', '2026-04-22', 2, 4, 1);


-- Inserimento messaggi tra utente e responsabile
INSERT INTO app_messaggio (content, data, destinatario_id, mittente_id) VALUES
('Buongiorno, vorrei richiedere ferie per il 5 Aprile.', UNIX_TIMESTAMP('2026-04-01 08:00:00'), 1, 2),
('Ferie approvate per il 5 Aprile.', UNIX_TIMESTAMP('2026-04-01 09:00:00'), 2, 1),
('Posso prendere anche il 6 Aprile?', UNIX_TIMESTAMP('2026-04-02 08:30:00'), 1, 2),
('Ok, 6 Aprile approvato.', UNIX_TIMESTAMP('2026-04-02 09:15:00'), 2, 1);


-- query che trova tutte le persone che appartengono a un team
SELECT u.username, u.first_name, u.last_name, r.ruolo
FROM app_normaluser nu
JOIN app_basedatauser u ON nu.user_id = u.id
JOIN app_ruoli r ON r.user_id = nu.id
WHERE nu.cod_team_id = 1;


-- query che trova tutte le ferie prenotate da un team
SELECT u.username, f.dataI, f.dataF, f.stato
FROM app_ferie f
JOIN app_normaluser nu ON f.user_id = nu.id
JOIN app_basedatauser u ON nu.user_id = u.id
WHERE nu.cod_team_id = 1
ORDER BY f.dataI;


-- query che ottiene tutti gli scambi di messaggi tra dipendenti e responsabili
SELECT 
    mittente.username       AS mittente,
    destinatario.username   AS destinatario,
    m.content               AS messaggio,
    FROM_UNIXTIME(m.data)   AS data_leggibile
FROM app_messaggio      AS m
JOIN app_normaluser     AS mitt_nu      ON m.mittente_id = mitt_nu.id
JOIN app_normaluser     AS dest_nu      ON m.destinatario_id = dest_nu.id
JOIN app_basedatauser   AS mittente     ON mitt_nu.user_id = mittente.id
JOIN app_basedatauser   AS destinatario ON dest_nu.user_id = destinatario.id
JOIN app_ruoli          AS r_dest       ON dest_nu.id = r_dest.user_id
WHERE mitt_nu.cod_team_id = 1 AND dest_nu.cod_team_id = 1
ORDER BY m.data;
