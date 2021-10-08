FROM registry.gitlab.b-data.ch/jupyterhub/jupyterhub-onbuild:1.4

RUN apt-get update \
  && apt-get upgrade -y \
  && pip install --no-cache-dir \
    psycopg2-binary \
    dockerspawner \
    jupyterhub-idle-culler \
    oauthenticator \
  # Clean up
  && rm -rf /var/lib/apt/lists/*
