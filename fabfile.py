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
        run('sudo supervisorctl stop celery')
        run('ve/bin/python %(path)s/newsconnector/manage.py celery purge' % env)
        run('./kill_celery.sh')
        run('sudo supervisorctl restart all')
