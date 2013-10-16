#!/bin/bash
sudo supervisorctl stop celery
/var/sites/newsconnector/ve/bin/python /var/sites/newsconnector/newsconnector/manage.py celery purge
kill -9 `ps aux | grep celery | awk -F' ' '{print $2.}'`
sudo supervisorctl restart all
