FROM registry.gitlab.b-data.ch/jupyterhub/jupyterhub-onbuild:1.3.0

RUN dpkgArch="$(dpkg --print-architecture)" \
  # Install gcc, libpq-dev and python3-dev to build psycopg2-binary on aarch64
  # https://github.com/psycopg/psycopg2-wheels/issues/16
  && if [ "$dpkgArch" = "arm64" ]; then \
    apt-get update; \
    DEPS="gcc python3-dev"; \
    apt-get install -y --no-install-recommends libpq-dev $DEPS; \
  fi \
  && pip install --no-cache-dir \
    psycopg2-binary \
    dockerspawner \
    jupyterhub-idle-culler \
    oauthenticator \
  # Remove gcc and python3-dev
  && if [ "$dpkgArch" = "arm64" ]; then \
    apt-get remove --purge -y $DEPS; \
    apt-get autoremove -y; \
    apt-get autoclean -y; \
    rm -rf /var/lib/apt/lists/*; \
  fi \
  # Clean up
  && rm -rf /tmp/*
