from shovel import task
import subprocess
import signal
from os.path import join
from os import chdir, getcwd

REPO_DIR = getcwd()
APP_DIR = 'hiddentalent'

ENV_FORMAT = join(REPO_DIR, 'deploy/environments/.env.{}')
PROC_FORMAT = join(REPO_DIR, 'deploy/procfiles/Procfile.{}')

HONCHO_RUN = "honcho run -e {0} {1}"
HONCHO_START = "honcho start -e {0} -f {1}"
HEROKU_RUN = 'heroku run "{}" --app {}'

APP_NAME_VAR = 'HEROKU_APP_NAME'
REMOTE_URI_VAR = 'GIT_REMOTE'
ES_URL = "'localhost:9200'"


def get_env_dict(env):
    d = {}
    with open(ENV_FORMAT.format(env), 'r') as f:
        for var in f:
            var_parts = var.replace('\n', '').split('=')
            k, v = var_parts[0], ''.join(var_parts[1:])
            d[k] = v
    return d


def wait_and_kill(csp):
    try:
        return csp.wait()
    except KeyboardInterrupt:
        csp.send_signal(signal.SIGINT)
        return wait_and_kill(csp)


@task
def run(command, env='dev', local=False):
    env_path = ENV_FORMAT.format(env)
    env_dict = get_env_dict(env)

    if not local and APP_NAME_VAR in env_dict:
        command = HEROKU_RUN.format(command, env_dict[APP_NAME_VAR])
    else:
        command = HONCHO_RUN.format(env_path, command)
    csp = subprocess.Popen(command, shell=True)
    return wait_and_kill(csp)


@task
def start(env='dev'):
    env_path = ENV_FORMAT.format('dev')
    proc_path = PROC_FORMAT.format(env)
    command = HONCHO_START.format(env_path, proc_path)
    csp = subprocess.Popen(command, shell=True)
    wait_and_kill(csp)


@task
def curl(action, url, env='dev'):
    command = 'curl -{} {}'.format(action, url)
    csp = subprocess.Popen(command, shell=True)
    wait_and_kill(csp)


@task
def manage(command, env='dev'):
    if env == 'dev':
        chdir(join(REPO_DIR, APP_DIR))
        command = 'python manage.py {}'.format(command)
        retcode = run(command, env=env)
        chdir(REPO_DIR)
        return retcode
    else:
        command = 'cd {} && python manage.py {}'.format(APP_DIR, command)
        run(command, env=env)


@task
def deploy(env='stag'):
    """Deploy to the named configuration stored in deploy. Defaults to staging."""
    env_path = ENV_FORMAT.format(env)
    env_dict = get_env_dict(env)

    run("heroku maintenance:on --app {}".format(env_dict[APP_NAME_VAR]), env=env, local=True)
    run("heroku config:push -o -e {} --app {}".format(env_path, env_dict[APP_NAME_VAR]), env=env, local=True)
    run("git push -f {} $(git rev-parse --abbrev-ref HEAD):master".format(env_dict[REMOTE_URI_VAR]), env=env, local=True)
    manage('syncdb --migrate --noinput', env=env)
    run("heroku maintenance:off --app {}".format(env_dict[APP_NAME_VAR]), env=env, local=True)


@task
def resetdb():
    """"Delete local database and index and setup again."""
    run('rm -rf db.sqlite3')
    curl('XDELETE', ES_URL)
    manage('syncdb --migrate --noinput', env='dev')
    manage('createcachetable cache', env='dev')
    manage('createsuperuser', env='dev')


@task
def resetrabbitmq():
    run('rabbitmqctl stop_app')
    run('rabbitmqctl reset')
    run('rabbitmqctl start_app')


@task
def migrate():
    manage('schemamigration listings --auto', env='dev')
    manage('migrate listings', env='dev')
