# WeasyPrint server

## But

Fournir un webservice qui converti un document html en pdf.

## Installation
### with pipenv (recommended)

Install pipenv :
```bash
pip install pipenv
PIPENV_VENV_IN_PROJECT=true pipenv install
```

Install apt :
```bash
apt install python3-flask weasyprint
```

## Lancement
### en local

```bash
flask run --host=0.0.0.0 -h ${CWD}/.venv # par défaut sur port 5000`
```

Une variable d'environnement `BASE_URL` doit pointer vers le serveur qui contient les assets,
par exemple `BASE_URL="http://localhost:3000"`

ou éventuellement, en local, grâce au `Procfile.dev` avec votre process manager favori (overmind, …).

Eventuellement rajouter `-p 5001` si le port 5000 est déjà utilisé (ce qui est le cas sous MacOS), ou avec la variable d'environnement `FLASK_RUN_PORT`.

### uwsgi

```bash
BASE_URL='http://127.0.0.1:3000' uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app
```

un exemple de fichier de configuration pour uWSGI :

```INI
[uwsgi]
plugin = python3
virtualenv = /home/weasyprint/weasyprint/.venv
http-socket = server_ip:3000
uid = weasyprint
gid = weasyprint
chdir = /home/weasyprint/weasyprint/
env = BASE_URL=https://root_of_your_statics
wsgi-file = wsgi.py
callable = app
processes = 4
stats = server_ip:9191
```
