Newsconnector
============

A python app that relates news stories sourced via rss feeds

Getting it running
------------------
#. Requirements::
    
    sudo apt-get install supervisor nginx memcached rabbitmq-server \
    libxml2-dev libxslt-dev git libpq-dev virtualenvwrapper haproxy \
    aptitude postgresql-9.1 postgresql-server-dev-all python-dev \
    redis-server openjdk-7-jre-headless
    
#.  Install Elasticsearch

    https://gist.github.com/wingdspur/2026107
    
#. Create db::

    sudo -u postgres createuser --superuser --pwprompt news
    createdb -W -U news -h localhost -E UNICODE news
    
#. Clone the repo + virtual environment::

    git clone git@github.com:miltontony/newsconnector.git
    cd newsconnector
    virtualenv --no-site-packages ve
    source ve/bin/activate
    
    pip install -r requirements.pip
    
#. Setup Django::

    cd newsconnector
    
    ./manage.py syncdb
    ./manage.py migrate
    ./manage.py loaddata fixtures/*
    ./manage.py collectstatic --noinput

#. Run app::

    ./manage.py runserver
