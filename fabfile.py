from fabric.api import *
env.path = '/var/sites/newsconnector'
is_web = False


def cloud():
    env.hosts = ['ubuntu@162.243.76.49']


def web():
    global is_web
    is_web = True
    env.hosts = ['ubuntu@192.241.255.58']


def push():
    with cd(env.path):
        run('git pull')


def static():
    if is_web:
        with cd(env.path):
            run('ve/bin/python %(path)s/newsconnector/manage.py '
                'collectstatic --noinput' % env)


def reload_g():
    if is_web:
        with cd(env.path):
            run('kill -HUP `cat tmp/pids/newsconnector*.pid`')


def deploy():
    push()
    static()
    reload_g()


def restart():
    if is_web:
        sudo('supervisorctl restart newsconnector:')


def restart_celery():
    with cd(env.path):
        sudo('supervisorctl stop celery')
        run('ve/bin/python %(path)s/newsconnector/manage.py '
            'celery purge -f' % env)

    with settings(warn_only=True):
        run('%(path)s/kill_workers.sh' % env)

    sudo('supervisorctl start celery')
