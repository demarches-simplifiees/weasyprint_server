#!/bin/bash -x

set -o nounset
set -o errexit
set -o pipefail

APP_BRANCH=${1:-main}
BASE_URL="http://$(ip -4 -br addr show wlan0 | awk '{print $3}' | cut -d/ -f1):3000"

# clean
mkdir -p tmp
rm -rf tmp/*
docker container rm -f builder || true
docker container rm -f vanilla || true

# build
docker build -t package_weasyprint .

docker run -dit --name builder package_weasyprint:latest /bin/bash

# try to simulate gitlab `script` section
# docker exec builder git clone https://github.com/demarches-simplifiees/weasyprint_server.git --branch $APP_BRANCH --single-branch --depth 1
# instead we do this, to avoid cloning the repo every time in development
docker cp ../../weasyprint_server builder:/builds
docker exec builder bash weasyprint_server/package_scripts/package.sh $APP_BRANCH

docker cp builder:$(docker exec builder sh -c 'find $(pwd) -iname weasyprint_server*.deb') tmp

# run
docker build -t vanilla -f Dockerfile_vanilla .

docker run -p 8000:8000 -dit --name vanilla vanilla:latest /bin/bash

LAST_DEB=$(find tmp -iname '*.deb' | sort | tail -n 1)
docker cp $LAST_DEB vanilla:/root

docker exec vanilla dpkg -i /root/$(basename $LAST_DEB)

docker exec -u weasyprint vanilla /bin/bash -c "LOG_DIR=/var/log/weasyprint BASE_URL=$BASE_URL /opt/weasyprint/app/.venv/bin/uwsgi --ini /etc/opt/weasyprint/weasyprint.ini"
