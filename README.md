# WeasyPrint server

## But

Convertir des documents html en pdf.

## Développement
### installation

On utilise les outils [pyenv](https://github.com/pyenv/pyenv) et [pipenv](https://pipenv.pypa.io/en/latest/) pour gérer les dépendances.

```bash
# installation de la version de python definit dans .python-version
pyenv install

pip install pipenv

# installation des deps
pipenv install --dev
```

### lancement de l'application

1. Configurer vos variables d'environnement dans le fichier .env

```bash
cp env.example .env
```

2. lancer l'appli

```bash
pipenv run flask run

# or any process manager reading Procfile.dev
overmind start
```

### tests

```bash
pipenv run invoke test
```

### linters

```bash
pipenv run invoke lint
```

## Production

On utilise le webserver [uwsgi](https://uwsgi-docs.readthedocs.io/en/latest/)

```bash
pipenv run uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app
```

Exemple de fichier de config :

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
