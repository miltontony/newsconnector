from fabric.api import *

env.path = '/var/sites/newsconnector'
env.hosts = ['ubuntu@newsworld.co.za']


def push():
    with cd(env.path):
        run('git pull')


def static():
    with cd(env.path):
        run('ve/bin/python %(path)s/newsconnector/manage.py collectstatic --noinput' % env)


def reload_g():
    with cd(env.path):
        run('kill -HUP `cat tmp/pids/newsconnector*.pid`')


def deploy():
    push()
    static()
    reload_g()


def restart():
    sudo('supervisorctl restart newsconnector:')


def restart_celery():
    with cd(env.path):
        sudo('supervisorctl stop celery')
        run('ve/bin/python %(path)s/newsconnector/manage.py celery purge -f' % env)

    with settings(warn_only=True):
        run('%(path)s/kill_workers.sh' % env)

    sudo('supervisorctl start celery')
