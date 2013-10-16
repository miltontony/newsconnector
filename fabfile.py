from fabric.api import *

env.path = '/var/sites/newsconnector'
env.hosts = ['ubuntu@23.21.46.126']


def push():
    with cd(env.path):
        run('git pull')


def static():
    with cd(env.path):
        run('ve/bin/python %(path)s/newsconnector/manage.py collectstatic --noinput' % env)


def reload():
    with cd(env.path):
        run('kill -HUP `cat tmp/pids/newsconnector*.pid`')


def restart():
    with cd(env.path):
        sudo('supervisorctl stop celery')
        run('ve/bin/python %(path)s/newsconnector/manage.py celery purge' % env)

    with settings(warn_only=True):
        run('%(path)s/kill_workers.sh' % env)

    sudo('supervisorctl restart all')
