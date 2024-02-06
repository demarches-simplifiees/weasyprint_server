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

```bash
apt install python3-flask weasyprint
```

## Lancement
### en local

```bash
flask run --host=0.0.0.0 -H ${CWD}/.venv # par défaut sur port 5000`
```

Une variable d'environnement `BASE_URL` doit pointer vers le serveur qui contient les assets,
par exemple `BASE_URL="http://localhost:3000"`

ou éventuellement, en local, grâce au `Procfile.dev` avec votre process manager favori (overmind, …).

Eventuellement rajouter `-p 5001` si le port 5000 est déjà utilisé (ce qui est le cas sous MacOS), ou avec la variable d'environnement `FLASK_RUN_PORT`.

### uwsgi

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
wsgi-file = app.py
callable = app
processes = 4
stats = server_ip:9191
```
