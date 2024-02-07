# WeasyPrint server

## But
Fournir un webservice qui converti un document html en pdf.

## Installation
apt install python3-flask weasyprint

## Lancement

Une variable d'environnement `BASE_URL` doit pointer vers le serveur qui contient les assets,
par exemple `BASE_URL="http://localhost:3000"`

`flask run --host=0.0.0.0 # par défaut sur port 5000`

ou éventuellement, en local, grâce au `Procfile.dev` avec votre process manager favori (overmind, …).

Eventuellement rajouter `-p 5001` si le port 5000 est déjà utilisé (ce qui est le cas sous MacOS), ou avec la variable d'environnement `FLASK_RUN_PORT`.


