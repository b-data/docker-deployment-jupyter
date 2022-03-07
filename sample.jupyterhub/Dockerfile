FROM registry.gitlab.b-data.ch/jupyterhub/jupyterhub-onbuild:2.2

RUN apt-get update \
  && apt-get install -y \
    ca-certificates \
    openssl \
  && pip install --no-cache-dir \
    psycopg2-binary \
    dockerspawner \
    jupyterhub-idle-culler \
    oauthenticator \
  # Clean up
  && rm -rf /var/lib/apt/lists/*
