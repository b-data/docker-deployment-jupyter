# Configuration file for jupyterhub.

import os

#------------------------------------------------------------------------------
# JupyterHub(Application) configuration
#------------------------------------------------------------------------------

## An Application for starting a Multi-User Jupyter Notebook server.

## Grant admin users permission to access single-user servers.
#  
#  Users should be properly informed if this is enabled.
#c.JupyterHub.admin_access = False

## Class for authenticating users.
#  
#          This should be a subclass of :class:`jupyterhub.auth.Authenticator`
#  
#          with an :meth:`authenticate` method that:
#  
#          - is a coroutine (asyncio or tornado)
#          - returns username on success, None on failure
#          - takes two arguments: (handler, data),
#            where `handler` is the calling web.RequestHandler,
#            and `data` is the POST form data from the login page.
#  
#          .. versionchanged:: 1.0
#              authenticators may be registered via entry points,
#              e.g. `c.JupyterHub.authenticator_class = 'pam'`
#  
#  Currently installed: 
#    - auth0: oauthenticator.auth0.Auth0OAuthenticator
#    - azuread: oauthenticator.azuread.AzureAdOAuthenticator
#    - bitbucket: oauthenticator.bitbucket.BitbucketOAuthenticator
#    - cilogon: oauthenticator.cilogon.CILogonOAuthenticator
#    - generic-oauth: oauthenticator.generic.GenericOAuthenticator
#    - github: oauthenticator.github.GitHubOAuthenticator
#    - gitlab: oauthenticator.gitlab.GitLabOAuthenticator
#    - globus: oauthenticator.globus.GlobusOAuthenticator
#    - google: oauthenticator.google.GoogleOAuthenticator
#    - local-auth0: oauthenticator.auth0.LocalAuth0OAuthenticator
#    - local-azuread: oauthenticator.azuread.LocalAzureAdOAuthenticator
#    - local-bitbucket: oauthenticator.bitbucket.LocalBitbucketOAuthenticator
#    - local-cilogon: oauthenticator.cilogon.LocalCILogonOAuthenticator
#    - local-generic-oauth: oauthenticator.generic.LocalGenericOAuthenticator
#    - local-github: oauthenticator.github.LocalGitHubOAuthenticator
#    - local-gitlab: oauthenticator.gitlab.LocalGitLabOAuthenticator
#    - local-globus: oauthenticator.globus.LocalGlobusOAuthenticator
#    - local-google: oauthenticator.google.LocalGoogleOAuthenticator
#    - local-okpy: oauthenticator.okpy.LocalOkpyOAuthenticator
#    - local-openshift: oauthenticator.openshift.LocalOpenShiftOAuthenticator
#    - mediawiki: oauthenticator.mediawiki.MWOAuthenticator
#    - okpy: oauthenticator.okpy.OkpyOAuthenticator
#    - openshift: oauthenticator.openshift.OpenShiftOAuthenticator
#    - default: jupyterhub.auth.PAMAuthenticator
#    - dummy: jupyterhub.auth.DummyAuthenticator
#    - pam: jupyterhub.auth.PAMAuthenticator
from oauthenticator.gitlab import GitLabOAuthenticator
c.JupyterHub.authenticator_class = GitLabOAuthenticator

## url for the database. e.g. `sqlite:///jupyterhub.sqlite`
c.JupyterHub.db_url = 'postgresql://postgres:{password}@{host}/{db}'.format(
    host = os.environ['POSTGRES_HOST'],
    password = os.environ['POSTGRES_PASSWORD'],
    db = os.environ['POSTGRES_DB']
)

## The ip address for the Hub process to *bind* to.
#  
#  By default, the hub listens on localhost only. This address must be
#  accessible from the proxy and user servers. You may need to set this to a
#  public ip or '' for all interfaces if the proxy or user servers are in
#  containers or on a different host.
#  
#  See `hub_connect_ip` for cases where the bind and connect address should
#  differ, or `hub_bind_url` for setting the full bind URL.
c.JupyterHub.hub_ip = os.environ['HUB_IP']

## List of service specification dictionaries.
#  
#  A service
#  
#  For instance::
#  
#      services = [
#          {
#              'name': 'cull_idle',
#              'command': ['/path/to/cull_idle_servers.py'],
#          },
#          {
#              'name': 'formgrader',
#              'url': 'http://127.0.0.1:1234',
#              'api_token': 'super-secret',
#              'environment':
#          }
#      ]
c.JupyterHub.services = [
    {
        'name': 'cull_idle',
        'admin': True,
        'command': 'python /srv/jupyterhub/cull_idle_servers.py --timeout=3600'.split()
    }
]

## The class to use for spawning single-user servers.
#  
#          Should be a subclass of :class:`jupyterhub.spawner.Spawner`.
#  
#          .. versionchanged:: 1.0
#              spawners may be registered via entry points,
#              e.g. `c.JupyterHub.spawner_class = 'localprocess'`
#  
#  Currently installed: 
#    - docker: dockerspawner.DockerSpawner
#    - docker-swarm: dockerspawner.SwarmSpawner
#    - docker-system-user: dockerspawner.SystemUserSpawner
#    - default: jupyterhub.spawner.LocalProcessSpawner
#    - localprocess: jupyterhub.spawner.LocalProcessSpawner
#    - simple: jupyterhub.spawner.SimpleLocalProcessSpawner
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'

#------------------------------------------------------------------------------
# Spawner(LoggingConfigurable) configuration
#------------------------------------------------------------------------------

## The URL the single-user server should start in.
#  
#  `{username}` will be expanded to the user's username
#  
#  Example uses:
#  
#  - You can set `notebook_dir` to `/` and `default_url` to
#    `/tree/home/{username}` to allow people to navigate the whole filesystem
#    from their notebook server, but still start in their home directory.
#  - Start with `/notebooks` instead of `/tree` if `default_url` points to a
#    notebook instead of a directory.
#  - You can set this to `/lab` to have JupyterLab start by default, rather
#    than Jupyter Notebook.
c.Spawner.default_url = '/lab'

## Path to the notebook directory for the single-user server.
#  
#  The user sees a file listing of this directory when the notebook interface is
#  started. The current interface does not easily allow browsing beyond the
#  subdirectories in this directory's tree.
#  
#  `~` will be expanded to the home directory of the user, and {username} will be
#  replaced with the name of the user.
#  
#  Note that this does *not* prevent users from accessing files outside of this
#  path! They can do so with many other means.
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan'
c.Spawner.notebook_dir = notebook_dir

#------------------------------------------------------------------------------
# DockerSpawner(LoggingConfigurable) configuration
#------------------------------------------------------------------------------
# See https://jupyterhub-dockerspawner.readthedocs.io/en/latest/api/index.html

## The image to use for single-user servers.
#  
#  This image should have the same version of jupyterhub as the Hub itself
#  installed.
#  
#  If the default command of the image does not launch jupyterhub-singleuser,
#  set `c.Spawner.cmd` to launch jupyterhub-singleuser, e.g.
#  
#  Any of the jupyter docker-stacks should work without additional config, as
#  long as the version of jupyterhub in the image is compatible.
c.Spawner.image = os.environ['DOCKER_JUPYTERLAB_IMAGE']

## Run the containers on this docker network.
#  
#  If it is an internal docker network, the Hub should be on the same network,
#  as internal docker IP addresses will be used. For bridge networking,
#  external ports will be bound.
c.Spawner.network_name = os.environ['DOCKER_NETWORK_NAME']

## Prefix for container names.
#  
#  See name_template for full container name for a particular user’s server.
c.Spawner.prefix = 'jupyterlab'

## If True, delete containers when servers are stopped.
#  
#  This will destroy any data in the container not stored in mounted volumes.
c.Spawner.remove = True

## Map from host file/directory to container (guest) file/directory mount point
## and (optionally) a mode.
#  
#  When specifying the guest mount point (bind) for the volume, you may use a
#  dict or str. If a str, then the volume will default to a read-write
#  (mode="rw"). With a dict, the bind is identified by "bind" and the "mode"
#  may be one of "rw" (default), "ro" (read-only), "z" (public/shared SELinux
#  volume label), and "Z" (private/unshared SELinux volume label).
#  
#  If format_volume_name is not set, default_format_volume_name is used for
#  naming volumes. In this case, if you use {username} in either the host or
#  guest file/directory path, it will be replaced with the current user’s name.
c.Spawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }

#------------------------------------------------------------------------------
# Authenticator(LoggingConfigurable) configuration
#------------------------------------------------------------------------------

## Base class for implementing an authentication provider for JupyterHub

## Set of users that will have admin rights on this JupyterHub.
#  
#  Admin users have extra privileges:
#   - Use the admin panel to see list of users logged in
#   - Add / remove users in some authenticators
#   - Restart / halt the hub
#   - Start / stop users' single-user servers
#   - Can access each individual users' single-user server (if configured)
#  
#  Admin access should be treated the same way root access is.
#  
#  Defaults to an empty set, in which case no user has admin access.
#c.Authenticator.admin_users = set()
