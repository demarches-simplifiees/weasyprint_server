# WeasyPrint server

## But

Convertir des documents html en pdf.

## Développement
### installation

On utilise [uv](https://github.com/astral-sh/uv) pour gérer python et ces dépendances.

On copy les variables d'env

```bash
cp env.example .env
```

### lancement de l'application

```bash
uv run flask run --debug

# or any process manager reading Procfile.dev
overmind start
```

### tests

```bash
uv run python -m unittest
```

### linters

```bash
uv run ruff format --check && uv run ruff check
```

## Packaging

voir package_scripts/main.sh

## Fonctionnement

Une fois l’app installée on peut vérifier qu’elle fonctionne avec :

```sh
curl -X POST \
  http://localhost:5000/pdf \
  -H "Content-Type: application/json" \
  -d '{"html": "<html><body><h1>Test</h1></body></html>"}' \
  --output test.pdf
```

## Build

Pour la production :

```sh
docker build -f ops/production/Dockerfile -t NAME .
```
