# Configuration file for jupyterhub.

import os
import sys

#------------------------------------------------------------------------------
# JupyterHub(Application) configuration
#------------------------------------------------------------------------------
## An Application for starting a Multi-User Jupyter Notebook server.

## Grant admin users permission to access single-user servers.
#  
#  Users should be properly informed if this is enabled.
#  Default: False
# c.JupyterHub.admin_access = False

## Allow named single-user servers per user
#  Default: False
# c.JupyterHub.allow_named_servers = False

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
#  Default: 'jupyterhub.auth.PAMAuthenticator'
from oauthenticator.gitlab import GitLabOAuthenticator
c.JupyterHub.authenticator_class = GitLabOAuthenticator
c.GitLabOAuthenticator.oauth_callback_url = 'https://{subdomain}.{domain}/hub/oauth_callback'.format(
    subdomain = os.environ['JUPYTERHUB_SUBDOMAIN'],
    domain = os.environ['JUPYTERHUB_DOMAIN']
)

## Whether to shutdown single-user servers when the Hub shuts down.
#  
#          Disable if you want to be able to teardown the Hub while leaving the
#  single-user servers running.
#  
#          If both this and cleanup_proxy are False, sending SIGINT to the Hub will
#          only shutdown the Hub, leaving everything else running.
#  
#          The Hub should be able to resume from database state.
#  Default: True
# c.JupyterHub.cleanup_servers = True

## url for the database. e.g. `sqlite:///jupyterhub.sqlite`
#  Default: 'sqlite:///jupyterhub.sqlite'
c.JupyterHub.db_url = 'postgresql://postgres:{password}@{host}:5432/{db}'.format(
    host = os.environ['POSTGRES_HOST'],
    password = os.environ['POSTGRES_PASSWORD'],
    db = os.environ['POSTGRES_DB']
)

## The ip address for the Hub process to *bind* to.
#  
#  By default, the hub listens on localhost only. This address must be accessible
#  from the proxy and user servers. You may need to set this to a public ip or ''
#  for all interfaces if the proxy or user servers are in containers or on a
#  different host.
#  
#  See `hub_connect_ip` for cases where the bind and connect address should
#  differ, or `hub_bind_url` for setting the full bind URL.
#  Default: '127.0.0.1'
c.JupyterHub.hub_ip = ''

## Maximum number of concurrent named servers that can be created by a user at a
#  time.
#  
#  Setting this can limit the total resources a user can consume.
#  
#  If set to 0, no limit is enforced.
#  Default: 0
# c.JupyterHub.named_server_limit_per_user = 0

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
#  Default: []
c.JupyterHub.services = [
    {
        'name': 'idle-culler',
        'admin': True,
        'command': [
            sys.executable,
            '-m', 'jupyterhub_idle_culler',
            '--timeout=3600'
        ],
    }
]

## Shuts down all user servers on logout
#  Default: False
# c.JupyterHub.shutdown_on_logout = False

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
#  Default: 'jupyterhub.spawner.LocalProcessSpawner'
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'

#------------------------------------------------------------------------------
# Spawner(LoggingConfigurable) configuration
#------------------------------------------------------------------------------

## Override escaping with any callable of the form escape(str)->str
#  
#  This is used to ensure docker-safe container names, etc.
#  
#  The default escaping should ensure safety and validity,
#  but can produce cumbersome strings in cases.
#  
#  Set c.DockerSpawner.escape = 'legacy' to preserve the earlier, unsafe behavior
#  if it worked for you.
#  
#  .. versionadded:: 12.0
#  
#  .. versionchanged:: 12.0
#      Escaping has changed in 12.0 to ensure safety,
#      but existing deployments will get different container and volume names.


## Maximum number of cpu-cores a single-user notebook server is allowed to use.
#  
#  If this value is set to 0.5, allows use of 50% of one CPU. If this value is
#  set to 2, allows use of up to 2 CPUs.
#  
#  The single-user notebook server will never be scheduled by the kernel to use
#  more cpu-cores than this. There is no guarantee that it can access this many
#  cpu-cores.
#  
#  **This is a configuration setting. Your spawner must implement support for the
#  limit to work.** The default spawner, `LocalProcessSpawner`, does **not**
#  implement this support. A custom spawner **must** add support for this setting
#  for it to be enforced.
#  Default: None
# c.Spawner.cpu_limit = None

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
#  Default: ''
c.Spawner.default_url = '/lab'

## Extra environment variables to set for the single-user server's process.
#  
#  Environment variables that end up in the single-user server's process come from 3 sources:
#    - This `environment` configurable
#    - The JupyterHub process' environment variables that are listed in `env_keep`
#    - Variables to establish contact between the single-user notebook and the hub (such as JUPYTERHUB_API_TOKEN)
#  
#  The `environment` configurable should be set by JupyterHub administrators to
#  add installation specific environment variables. It is a dict where the key is
#  the name of the environment variable, and the value can be a string or a
#  callable. If it is a callable, it will be called with one parameter (the
#  spawner instance), and should return a string fairly quickly (no blocking
#  operations please!).
#  
#  Note that the spawner class' interface is not guaranteed to be exactly same
#  across upgrades, so if you are using the callable take care to verify it
#  continues to work after upgrades!
#  
#  .. versionchanged:: 1.2
#      environment from this configuration has highest priority,
#      allowing override of 'default' env variables,
#      such as JUPYTERHUB_API_URL.
#  Default: {}
# c.Spawner.environment = {}

## Timeout (in seconds) before giving up on a spawned HTTP server
#  
#  Once a server has successfully been spawned, this is the amount of time we
#  wait before assuming that the server is unable to accept connections.
#  Default: 30
# c.Spawner.http_timeout = 30

## Maximum number of bytes a single-user notebook server is allowed to use.
#  
#  Allows the following suffixes:
#    - K -> Kilobytes
#    - M -> Megabytes
#    - G -> Gigabytes
#    - T -> Terabytes
#  
#  If the single user server tries to allocate more memory than this, it will
#  fail. There is no guarantee that the single-user notebook server will be able
#  to allocate this much memory - only that it can not allocate more than this.
#  
#  **This is a configuration setting. Your spawner must implement support for the
#  limit to work.** The default spawner, `LocalProcessSpawner`, does **not**
#  implement this support. A custom spawner **must** add support for this setting
#  for it to be enforced.
#  Default: None
# c.Spawner.mem_limit = None

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
#  Default: ''
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan'
c.Spawner.notebook_dir = notebook_dir

## An optional hook function that you can implement to do some bootstrapping work
#  before the spawner starts. For example, create a directory for your user or
#  load initial content.
#  
#  This can be set independent of any concrete spawner implementation.
#  
#  This maybe a coroutine.
#  
#  Example::
#  
#      from subprocess import check_call
#      def my_hook(spawner):
#          username = spawner.user.name
#          check_call(['./examples/bootstrap-script/bootstrap.sh', username])
#  
#      c.Spawner.pre_spawn_hook = my_hook
#  Default: None
# c.Spawner.pre_spawn_hook = None

## Timeout (in seconds) before giving up on starting of single-user server.
#  
#  This is the timeout for start to return, not the timeout for the server to
#  respond. Callers of spawner.start will assume that startup has failed if it
#  takes longer than this. start should return when the server process is started
#  and its location is known.
#  Default: 60
# c.Spawner.start_timeout = 60

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
#  Default: 'jupyterhub/singleuser:1.3'
c.Spawner.image = os.environ['DOCKER_JUPYTERLAB_IMAGE']

## Run the containers on this docker network.
#  
#  If it is an internal docker network, the Hub should be on the same network,
#  as internal docker IP addresses will be used. For bridge networking,
#  external ports will be bound.
#  Default: 'bridge'
c.Spawner.network_name = os.environ['DOCKER_NETWORK_NAME']

## Prefix for container names.
#  
#  See name_template for full container name for a particular user’s server.
#  Default: 'jupyter'
c.Spawner.prefix = 'jupyterlab'

## If True, delete containers when servers are stopped.
#  
#  This will destroy any data in the container not stored in mounted volumes.
#  Default: False
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
#  Default: {}
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
#  Default: set()
# c.Authenticator.admin_users = set()
