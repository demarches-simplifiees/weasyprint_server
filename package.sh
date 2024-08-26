#!/bin/bash -x

# This script is meant to be run inside a ubuntu container
# with git and uv installed
# and the directories /home/weasyprint and /opt/weasyprint owned by weasyprint user

set -o nounset
set -o errexit
set -o pipefail

APP_BRANCH=${APP_BRANCH:-main}

TARGET_DIR="/opt/weasyprint"
BUILD_DIR="/home/weasyprint/build"
DEB_DIR="/home/weasyprint/build/deb"

# cleaning
rm -rf $BUILD_DIR "${TARGET_DIR:?}/*"

# fetch app
echo "cloning repo"
git clone https://github.com/demarches-simplifiees/weasyprint_server.git "$TARGET_DIR/app"
cd "$TARGET_DIR/app" || return
git checkout "$APP_BRANCH"

# analyze
APP_COMMIT_HASH=$(git rev-parse --short HEAD)
PACKAGE_VERSION=$(date '+%Y-%m-%d-%H-%M')+${APP_COMMIT_HASH}
APP_COMMIT_MESSAGE=$(git log -n 1 --pretty=%B | sed 's/^[[:space:]]*$/\./' | sed 's/^/ /' | sed '${/\./d}')

# install python and app under target dir
UV_PYTHON_INSTALL_DIR="$TARGET_DIR" uv sync

# prepare deb
mkdir -p "$DEB_DIR"/{DEBIAN,opt}
cp -r "$TARGET_DIR" "$DEB_DIR/opt"

# on crée le fichier de contrôle
cat > "$DEB_DIR/DEBIAN/control" <<EOF
Package: weasyprint-server
Version: $PACKAGE_VERSION
Installed-Size: $(du -s "$DEB_DIR" | cut -f1)
Date: $(date -R)
APP-Hash: $APP_COMMIT_HASH
APP-Commit-Message:
$APP_COMMIT_MESSAGE
Architecture: all
Maintainer: equipe ds <tech@demarches-simplifiees.fr>
Description: a flask wrapper around weasyprint
  This package contains a flask wrapper around weasyprint
Depends: pango1.0-tools
EOF

# build deb
dpkg-deb --build "$DEB_DIR" "$BUILD_DIR/weasyprint_server_${PACKAGE_VERSION}_amd64.deb"
