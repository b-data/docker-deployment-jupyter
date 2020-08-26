# Jupyter

[This project](https://gitlab.com/b-data/docker/deployments/jupyter) serves as
a template to run [jupyterhub](https://hub.docker.com/r/jupyterhub/jupyterhub)
with [jupyterlab/r/verse](https://gitlab.b-data.ch/jupyterlab/r/verse/container_registry)
in docker containers using docker-compose.

**Features**

*  **JupyterHub**: A multi-user Hub which spawns, manages, and proxies multiple
   instances of the single-user JupyterLab server.
    *  **PostgreSQL** database to store information about users, services, and
       other data needed for operating the Hub.
*  **JupyterLab**: A web-based interactive development environment for Jupyter
   notebooks, code, and data. The custom Docker image includes
    *  **code-server**: VS Code in the browser without MS
       branding/telemetry/licensing.
    *  **Git**: A distributed version-control system for tracking changes in
       source code.
    *  **Pandoc**: A universal markup converter.
    *  **R**: A language and environment for statistical computing and
       graphics.
    *  **radian**: An alternative console for R with multiline editing and rich
       syntax highlight.
    *  **TinyTeX**: A lightweight, cross-platform, portable, and
       easy-to-maintain LaTeX distribution based on TeX Live.
    *  **Zsh**: A shell designed for interactive use, although it is also a
       powerful scripting language.
*  Pre-configured to run at a **subdomain** (jupyter) of your **own domain**.
*  Use of environment files for variable substitution in the Compose file.

The following extensions are pre-installed for **code-server**:
*  [.gitignore Generator](https://marketplace.visualstudio.com/items?itemName=piotrpalarz.vscode-gitignore-generator)
*  [GitLens — Git supercharged](https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens)
*  [Excel Viewer](https://marketplace.visualstudio.com/items?itemName=GrapeCity.gc-excelviewer)
*  [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop)
*  [Path Intellisense](https://marketplace.visualstudio.com/items?itemName=christian-kohler.path-intellisense)
*  [Project Manager](https://marketplace.visualstudio.com/items?itemName=alefragnani.project-manager)
*  [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
*  [R](https://marketplace.visualstudio.com/items?itemName=Ikuyadeu.r)
*  [R LSP Client](https://marketplace.visualstudio.com/items?itemName=REditorSupport.r-lsp)
*  [YAML](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml)

**About**

*  **JupyterHub**
    *  Homepage: https://jupyter.org/hub
    *  Documentation: https://jupyterhub.readthedocs.io/en/1.0.0/
*  **JupyterLab**
    *  Homepage: https://jupyter.org
    *  Documentation: https://jupyterlab.readthedocs.io/en/1.2.x/
*  **code-server**
    *  Homepage: https://github.com/cdr/code-server
    *  Documentation: https://code.visualstudio.com/Docs
*  **Git**
    *  Homepage: https://git-scm.com
    *  Documentation: https://git-scm.com/docs
*  **Pandoc**
    *  Homepage: https://pandoc.org
    *  Manual: https://pandoc.org/MANUAL.html
*  **R**
    *  Homepage: https://www.r-project.org
    *  Manuals: https://cran.r-project.org/manuals.html
*  **radian**
    *  Homepage: https://github.com/randy3k/radian
*  **TinyTeX**
    *  Homepage: https://yihui.org/tinytex/
*  **Zsh**
    *  Homepage: http://zsh.sourceforge.net
    *  Documentation: http://zsh.sourceforge.net/Doc/Release/zsh_toc.html

## Prerequisites

The following is required:

*  [Docker Deployments](https://gitlab.com/b-data/docker/deployments) of
    *  [Træfik](https://gitlab.com/b-data/docker/deployments/traefik)
    *  [GitLab CE](https://gitlab.com/b-data/docker/deployments/gitlab-ce)
*  A DNS record for **subdomain** jupyter pointing to this host.

## Setup

1.  Create an external docker network named "jupyter":  
    ```bash
    docker network create jupyter
    ```
1.  Make a copy of '[.env.sample](.env.sample)' and rename it to '.env'.
1.  Update environment variables `JH_DOMAIN`, `GL_DOMAIN` and
    `JH_CERTRESOLVER_NAME` in '.env':
    *  Replace `mydomain.com` with your **own domain** that serves the
       **subdomain**.
    *  Replace `mydomain-com` with a valid certificate resolvers name of
       Træfik.
1.  [Add JupyterHub as an OAuth application](https://docs.gitlab.com/ce/integration/oauth_provider.html#oauth-applications-in-the-admin-area)
    in GitLab CE:  
      ```
      Name: JupyterHub
      Redirect URL: https://jupyter.mydomain.com/hub/oauth_callback
      ```
      → Replace `mydomain.com` with your **own domain** that serves the
      **subdomains**.
    *  Tick "Trusted"
    *  Scopes:
        *  Tick "api"
    *  Click "Submit" and copy "Application ID" and "Secret"
1.  Update environment variables `JH_GITLAB_APPLICATION_ID` and
    `JH_GITLAB_SECRET` in '.env' accordingly.
1.  Make a copy of '[db.env.sample](db.env.sample)' and rename it to 'db.env'.
1.  Update the following environment variable in 'db.env':
    *  `POSTGRES_PASSWORD`: Superuser password for PostgreSQL (default:
       `password`)
1.  Make a copy of folder '[jupyterhub.sample](jupyterhub.sample)' and rename
    it to 'jupyterhub'.
1.  Make a copy of '[docker-compose.yml.sample](docker-compose.yml.sample)' and
    rename it to 'docker-compose.yml'.
1.  Start the container in detached mode:  
    ```bash
    docker-compose up -d
    ```

The image for service jupyterhub will be built now, because it does not exist
yet. This might take a while...  
→ To rebuild the image you must use `docker-compose build` or
`docker-compose up --build`.

### Test

Wait a moment and visit https://jupyter.mydomain.com to confirm everything went
fine.

## Further reading

### JupyterHub

*  [Authenticators](https://jupyterhub.readthedocs.io/en/1.0.0/reference/authenticators.html)
*  [DockerSpawner API](https://jupyterhub-dockerspawner.readthedocs.io/en/latest/api/index.html)
*  [The Hub's Database](https://jupyterhub.readthedocs.io/en/1.0.0/reference/database.html)

### JupyterLab

*  [ServerProxy](https://jupyter-server-proxy.readthedocs.io/en/latest/)

## License

[MIT License](LICENSE), Copyright (c) 2020 b-data GmbH

### Third party code

This project was inspired by the [JupyterHub deployment in use at Université de Versailles](https://github.com/defeo/jupyterhub-docker)
by [Luca De Feo](https://github.com/defeo).

See [LICENSE-THIRD-PARTY](LICENSE-THIRD-PARTY) for details.
