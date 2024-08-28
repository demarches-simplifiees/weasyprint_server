# WeasyPrint server

## But

Convertir des documents html en pdf.

## Développement
### installation

On utilise [uv](https://github.com/astral-sh/uv) pour gérer python et ces dépendances.

```bash
# installation du project
pyenv install

pip install poetry

# installation des deps
poetry install
```

### lancement de l'application

1. Configurer vos variables d'environnement dans le fichier .env

```bash
cp env.example .env
```

2. lancer l'appli

```bash
poetry run flask run --debug

# or any process manager reading Procfile.dev
overmind start
```

### tests

```bash
poetry run invoke test
```

### linters

```bash
poetry run invoke lint
```

## Packaging

>[!NOTE]
> La version de python sur la machine de packaging et la machine cible doit être la même.

```bash
git clone https://github.com/demarches-simplifiees/weasyprint_server.git
cd weasyprint_server
pip install poetry
poetry self add poetry-plugin-export
bash simple_package.sh
```

l'application avec ces dépendances est dans `dist.tar.gz`

## Production

### deploiement

```bash
cp dist.tar.gz good_directory && cd good_directory
tar -xvf dist.tar.gz
python -m venv .venv
. .venv/bin/activate
pip install --no-index --find-links=deps -r requirements.txt
# si on veut vérifier l'installation
flask run
```

### webserver

On utilise le webserver [uwsgi](https://uwsgi-docs.readthedocs.io/en/latest/)

Exemple de fichier de config :

```INI
[uwsgi]
plugin = python3
virtualenv = /home/weasyprint/weasyprint/.venv
http-socket = server_ip:3000
uid = weasyprint
gid = weasyprint
chdir = /home/weasyprint/weasyprint/
env = ... # see env.example
wsgi-file = wsgi.py
callable = app
processes = 4
stats = server_ip:9191
```
