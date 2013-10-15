#!/bin/bash
######The following is not needed changed#################
cd `dirname $0`

PRODIR=$(pwd)
PRONAME=$(basename $PRODIR)


PIDFILE="/var/run/yapster.pid"
SOCKFILE="/var/run/yapster.sock"
LOGFILE="/var/log/uwsgi.yapster.log"

MODULE="$PRONAME.wsgi:application"

if [ -f $PIDFILE ]; then
    kill -INT `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi

uwsgi --processes 2 --max-requests 10000 --master --pythonpath $PRODIR\
      --chdir $PRODIR --daemonize $LOGFILE --module $MODULE --socket $SOCKFILE --pidfile $PIDFILE

