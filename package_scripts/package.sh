#!/bin/bash -x

# This script is meant to be run inside a ubuntu container with git and uv installed
# and the directories /home/weasyprint and /opt/weasyprint owned by weasyprint user

set -o nounset
set -o errexit
set -o pipefail

APP_BRANCH=${1:-main}
echo "Building weasyprint-server from branch $APP_BRANCH"

GITLAB_RUNNER_DIR=$(pwd)

TARGET_DIR="/opt/weasyprint"
BUILD_DIR="/home/weasyprint/build"
DEB_DIR="$BUILD_DIR/deb"

# cleaning
rm -rf $BUILD_DIR "${TARGET_DIR:?}/*" && mkdir -p $BUILD_DIR

# fetch app
git clone https://github.com/demarches-simplifiees/weasyprint_server.git --branch "$APP_BRANCH" --single-branch --depth 1 "$TARGET_DIR/app"

# analyze
cd "$TARGET_DIR/app" || return
APP_COMMIT_HASH=$(git rev-parse --short HEAD)
PACKAGE_VERSION=$(date '+%Y-%m-%d-%H-%M')+${APP_COMMIT_HASH}
APP_COMMIT_MESSAGE=$(git log -n 1 --pretty=%B | sed 's/^[[:space:]]*$/\./' | sed 's/^/ /' | sed '${/\./d}')

# install python and app under target dir
UV_PYTHON_INSTALL_DIR="$TARGET_DIR" uv sync --no-dev --frozen

# cleanup
rm -rf .git .github .gitignore .pylintrc Procfile.dev package_scripts tests
rm -rf "$TARGET_DIR/.cache" "$TARGET_DIR/.gitignore" "$TARGET_DIR/.lock"

# prepare deb
cp -r "$GITLAB_RUNNER_DIR/weasyprint_server/package_scripts/deb" "$DEB_DIR"
cp -r "$TARGET_DIR" "$DEB_DIR/opt"

# on crée le fichier de contrôle
cat >> "$DEB_DIR/DEBIAN/control" <<EOF
Version: $PACKAGE_VERSION
Installed-Size: $(du -s "$DEB_DIR" | cut -f1)
Date: $(date -R)
APP-Hash: $APP_COMMIT_HASH
APP-Commit-Message:
$APP_COMMIT_MESSAGE
EOF

# build deb
dpkg-deb --build "$DEB_DIR" "$GITLAB_RUNNER_DIR/weasyprint_server_${PACKAGE_VERSION}_amd64.deb"
