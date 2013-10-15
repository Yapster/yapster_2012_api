#!/bin/bash
######The following is not needed changed#################
cd `dirname $0`

PRODIR=$(pwd)
PRONAME=$(basename $PRODIR)


LOGFILE="$PRODIR/log/uwsgi.log"
PIDFILE="/tmp/yapster..pid"
SOCKFILE="/tmp/yapster.sock"

MODULE="$PRONAME.wsgi:application"

if [ -f $PIDFILE ]; then
    kill -INT `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi