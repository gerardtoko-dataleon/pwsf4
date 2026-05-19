
FROM python:3.10.18-slim-bookworm

# SCW_SECRET_KEY et GOOGLE_APPLICATION_CREDENTIALS doivent être injectés
# au runtime via --env ou un secret manager (ex: Scaleway Secret Manager).
# Ne jamais passer de secrets en ARG de build (visibles dans docker history).
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

# Dépendances pip — installer AVANT le code source pour profiter du cache Docker
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD ["/bin/bash"]
