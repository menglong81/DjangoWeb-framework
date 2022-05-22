#!/bin/bash
cd /home/q/www/{#APPNAME#}
if [[ ! -e pidfile ]]
then
    gunicorn37 -w 1 -k gevent -b 0.0.0.0:{#APPPORT#} DjangoProject.{#APPNAME#}_wsgi -D --pid pidfile
fi
ps auxf | grep {#APPNAME#} | grep -v grep
echo "start done"
