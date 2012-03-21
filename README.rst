Newsconnector
============

A python app that relates news stories graphically sourced via rss feeds

Getting it running
------------------

#. From a terminal run the following::

    $ git clone git://github.com/miltontony/newsconnector.git
    $ cd newsconnector
    $ virtualenv --no-site-packages ve
    $ source ve/bin/activate
    (ve)$ pip install -r requirements.pip
    (ve)$ ./manage.py syncdb
    (ve)$ ./manage.py migrate
    (ve)$ ./manage.py runserver
