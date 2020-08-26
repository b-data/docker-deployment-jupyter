FROM jupyterhub/jupyterhub-onbuild:1.0.0

RUN wget https://raw.githubusercontent.com/jupyterhub/jupyterhub/d126baa443ad7d893be2ff4a70afe9ef5b8a4a1a/examples/cull-idle/cull_idle_servers.py \
  && conda install -yq psycopg2 \
  && conda clean -tipsy \
  && pip install --no-cache-dir \
    dockerspawner \
    oauthenticator
