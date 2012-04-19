Newsconnector
============

A python app that relates news stories graphically sourced via rss feeds

Getting it running
------------------

#. From a terminal run the following::

    $ git clone git://github.com/miltontony/newsconnector.git
    $ cd newsconnector
    $ virtualenv --no-site-packages ve
    $ sudo -u postgres createuser --superuser --pwprompt news
    ... // snip, default password is `yal` // ...
    $ createdb -W -U news -h localhost -E UNICODE news
    $ source ve/bin/activate
    (ve)$ pip install -r requirements.pip
    (ve)$ ./manage.py syncdb
    (ve)$ ./manage.py migrate
    (ve)$ ./manage.py loaddata fixtures/*
    (ve)$ ./manage.py runserver
