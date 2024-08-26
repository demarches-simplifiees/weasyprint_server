FROM ubuntu:focal

RUN apt-get update \
    && apt-get install -yqq curl git \
    && curl -sSL "https://github.com/astral-sh/uv/releases/download/0.3.3/uv-x86_64-unknown-linux-gnu.tar.gz" | tar -xz -C /usr/local/bin --strip-components=1 \
    && adduser --disabled-password --gecos "" weasyprint \
    && mkdir -p /opt/weasyprint \
    # simulate gitlab runner builds directory
    && mkdir -p /builds \ 
    && chown -R weasyprint:weasyprint /opt/weasyprint /builds

WORKDIR /builds
USER weasyprint
