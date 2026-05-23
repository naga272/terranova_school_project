# Terranova Gestione Ferie

![Platform](https://img.shields.io/badge/OS%20platform%20supported-Windows-green?style=flat)

![Language](https://img.shields.io/badge/Language-python-green?style=flat)

![Testing](https://img.shields.io/badge/Test-Pass-green)


## Descrizione

Per la descrizione del progetto vedere il file word `PCTP2025 - STUDENTI_ Calendari ferie.docx`

## Esecuzione

Se sei su Windows ed è la prima volta che esegui questo programma,
esegui lo script file.bat situato nella directory principale del progetto.

- Se sei su Linux e esegui questo programma per la prima volta,
esegui i seguenti comandi dalla directory principale del progetto:

```bash
python3 manage.py migrate
python3 manage.py makemigrations
python3 manage.py runserver
python3 manage.py createsuperuser
```

Nel caso si volesse rendere raggiungibili esternamente il server:
```cmd
python3 manage.py runserver 0.0.0.0:8000
```

## Requisiti

- python > 3.10

- installa i pacchetti richiesti in requirements.txt

Su windows:

```cmd
pip install -r requirements.txt
```

Su Linux:
```bash
pip3 install -r requirements.txt
```

## Author

- Piscitelli Damiano
- Padrini Raffaele
- Bastianello Federico
- Leonardo Yan Soardo
