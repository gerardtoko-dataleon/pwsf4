
FROM python:3.10.18-slim-bookworm

# SCW_SECRET_KEY et GOOGLE_APPLICATION_CREDENTIALS doivent être injectés
# au runtime via --env ou un secret manager (ex: Scaleway Secret Manager).
# Ne jamais passer de secrets en ARG de build (visibles dans docker history).
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get upgrade -y --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Dépendances pip — installer AVANT le code source pour profiter du cache Docker
COPY requirements.txt ./
RUN pip install --no-cache-dir "pip>=26.1" "setuptools>=78.1.1" "wheel>=0.46.2" && \
    pip install --no-cache-dir -r requirements.txt && \
    pip uninstall -y coloredlogs verboselogs 2>/dev/null || true

COPY config.py ./

CMD ["/bin/bash"]
