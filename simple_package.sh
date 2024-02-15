#! /bin/bash

poetry install --without=dev
mkdir -p dist/deps
poetry export --format="requirements.txt" --without-hashes > requirements.txt
pip download -r requirements.txt -d dist/deps
cp -r weasyprint_server dist
cp pyproject.toml wsgi.py requirements.txt .python-version dist
tar -czvf dist.tar.gz -C dist .
