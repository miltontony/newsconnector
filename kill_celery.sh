#!/bin/bash
kill -9 `ps aux | grep celery | awk -F' ' '{print $2.}'`
return 0
