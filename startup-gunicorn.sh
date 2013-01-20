#!/bin/bash

PROJECT=discuss
HOME=~/git/discuss
GUNICORN=gunicorn
LOGFILE=/dev/shm/$GUNICORN-$PROJECT.log
ACCESSLOGFILE=/dev/shm/$GUNICORN-$PROJECT-access.log
PIDFILE=/tmp/$GUNICORN-$PROJECT.pid
NUM_WORKERS=1
WORKER=gevent
ADDRESS=127.0.0.1:10002
APPFILE=core
APP=app

cd $HOME

if [ -z $DEBUG ]; then
$GUNICORN \
 --worker-class=$WORKER \
 --workers=$NUM_WORKERS \
 --pid=$PIDFILE \
 --log-file=$LOGFILE \
 --access-logfile=$ACCESSLOGFILE \
 --bind=$ADDRESS \
 --daemon \
$APPFILE:$APP
else
$GUNICORN \
 --worker-class=$WORKER \
 --workers=$NUM_WORKERS \
 --pid=$PIDFILE \
 --access-logfile=$ACCESSLOGFILE \
 --bind=$ADDRESS \
 --graceful-timeout=3600 \
 --timeout=3600 \
$APPFILE:$APP
fi
