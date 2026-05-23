## Schema logico

Progetti(`idPr`, titolo, descrizione, data_consegna)


Teams(`idT`, num_min_persone, **idPr**)


BaseDataUsers(`idBU`, password, last_login, is_superuser, username, first_name, last_name, is_active, data_joined)


NormalUsers(`idUser`, codF, dataN, *task_assegnata, **idBU**, **idT**)


Ruoli(`idRuolo`, ruolo, **idUser**)


Messaggi(`idM`, content, data, **mittente**, **destinatario**)


Periodi(`idP`, dataI, dataF)


Ferie(`idF`, dataI, dataF, stato, **idUser**, **idP**)



### Note

**mittente** e **destinatario** sono foreign key di Normaluser(`idUser`)

