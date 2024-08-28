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
