#!/bin/bash
######The following is not needed changed#################
cd `dirname $0`

PRODIR=$(pwd)
PRONAME=$(basename $PRODIR)


LOGFILE="/var/log/uwsgi.yapster.log"
PIDFILE="/tmp/yapster.uwsgi.pid"
SOCKFILE="/tmp/yapster.uwsgi.sock"

MODULE="$PRONAME.wsgi:application"

if [ -f $PIDFILE ]; then
    kill -INT `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi

uwsgi --processes 2 --max-requests 10000 --master --pythonpath $PRODIR\
      --chdir $PRODIR --daemonize $LOGFILE --module $MODULE --socket $SOCKFILE --pidfile $PIDFILE\
      --chmod-socket=666
