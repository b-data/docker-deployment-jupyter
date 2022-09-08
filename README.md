<a href="https://benz0li.b-data.io/donate?project=2"><img src="https://benz0li.b-data.io/donate/static/donate-with-fosspay.png" alt="Donate with fosspay"></a> <a href="https://liberapay.com/benz0li/donate"><img src="https://liberapay.com/assets/widgets/donate.svg" alt="Donate using Liberapay" height="20"></a>

# Jupyter

[This project](https://gitlab.com/b-data/docker/deployments/jupyter) serves as
a template to run [jupyterhub](https://gitlab.b-data.ch/jupyterhub/jupyterhub/container_registry)
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
    *  **Quarto**: An open-source scientific and technical publishing system built on Pandoc. (amd64 only)
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
*  [.gitignore Generator](https://github.com/piotrpalarz/vscode-gitignore-generator)
*  [Git Graph](https://open-vsx.org/extension/mhutchie/git-graph)
*  [GitLab Workflow](https://open-vsx.org/extension/GitLab/gitlab-workflow)
*  [GitLens — Git supercharged](https://open-vsx.org/extension/eamodio/gitlens)
*  [Excel Viewer](https://open-vsx.org/extension/GrapeCity/gc-excelviewer)
*  [Jupyter](https://open-vsx.org/extension/ms-toolsai/jupyter)
*  [LaTeX Workshop](https://open-vsx.org/extension/James-Yu/latex-workshop)
*  [Path Intellisense](https://open-vsx.org/extension/christian-kohler/path-intellisense)
*  [Project Manager](https://open-vsx.org/extension/alefragnani/project-manager)
*  [Python](https://open-vsx.org/extension/ms-python/python)
*  [Quarto](https://open-vsx.org/extension/quarto/quarto) (amd64 only)
*  [R](https://open-vsx.org/extension/Ikuyadeu/r)
*  [YAML](https://open-vsx.org/extension/redhat/vscode-yaml)

**About**

*  **JupyterHub**
    *  Homepage: https://jupyter.org/hub
    *  Documentation: https://jupyterhub.readthedocs.io/en/stable/
*  **JupyterLab**
    *  Homepage: https://jupyter.org
    *  Documentation: https://jupyterlab.readthedocs.io/en/stable/
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
1.  Make a copy of all `sample.` files and folders:  
    ```bash
    for file in sample.*; do cp -r "$file" "${file#sample.}"; done;
    ```
1.  Update environment variables `JH_DOMAIN`, `GL_DOMAIN` and
    `JH_CERTRESOLVER_NAME` in '.env':
    *  Replace `mydomain.com` with your **own domain** that serves the
       **subdomain**.
    *  Replace `mydomain-com` with a valid certificate resolvers name of
       Træfik.
1.  Set environment variable `JH_COOKIE_SECRET` in '.env':  
    Generate random cookie secret:  
    ```bash
    openssl rand -hex 32
    ```
1.  [Add JupyterHub as an OAuth application](https://docs.gitlab.com/ee/integration/oauth_provider.html#oauth-applications-in-the-admin-area)
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
1.  Update the following environment variable in 'db.env':
    *  `POSTGRES_PASSWORD`: Superuser password for PostgreSQL (default:
       `password`)
1.  Start the container in detached mode:  
    ```bash
    docker-compose up -d
    ```

The image for service jupyterhub will be built now, because it does not exist
yet. This souldn't take long...  
→ To rebuild the image you must use `docker-compose build` or
`docker-compose up --build`.

### Test

Wait a moment and visit https://jupyter.mydomain.com to confirm everything went
fine.

## Further reading

### JupyterHub

*  [Authenticators](https://jupyterhub.readthedocs.io/en/stable/reference/authenticators.html)
*  [DockerSpawner API](https://jupyterhub-dockerspawner.readthedocs.io/en/stable/api/index.html)
*  [The Hub's Database](https://jupyterhub.readthedocs.io/en/stable/reference/database.html)

### JupyterLab

*  [ServerProxy](https://jupyter-server-proxy.readthedocs.io/en/stable/)

## License

[MIT License](LICENSE), Copyright (c) 2020 b-data GmbH

### Third party code

This project was inspired by the [JupyterHub deployment in use at Université de Versailles](https://github.com/defeo/jupyterhub-docker)
by [Luca De Feo](https://github.com/defeo).

See [LICENSE-THIRD-PARTY](LICENSE-THIRD-PARTY) for details.
