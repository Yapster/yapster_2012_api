#!/bin/bash
######The following is not needed changed#################
cd `dirname $0`

PRODIR=$(pwd)
PRONAME=$(basename $PRODIR)


PIDFILE="$PRODIR/run/uwsgi.pid"
LOGFILE="$PRODIR/log/uwsgi.log"
SOCKFILE="$PRODIR/run/uwsgi.sock"

MODULE="$PRONAME.wsgi:application"

if [ -f $PIDFILE ]; then
    kill -INT `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi

uwsgi --processes 2 --max-requests 10000 --master --pythonpath $PRODIR\
      --chdir $PRODIR --daemonize $LOGFILE --module $MODULE --socket $SOCKFILE --pidfile $PIDFILE

