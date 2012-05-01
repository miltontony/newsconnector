from fabric.api import *

env.path = '/var/sites/newsconnector'
env.supervisord_file = 'supervisord.production.conf'
env.hosts = ['ubuntu@23.21.46.126']

def push():
    with cd(env.path):
        run('git pull')

def static():
    with cd(env.path):
        run('ve/bin/python %(path)s/newsconnector/manage.py collectstatic --noinput' % env)

def deploy():
    with cd(env.path):
        run('git pull')
        run('supervisorctl -c config/%(supervisord_file)s restart all' % env)

