#!/bin/bash

PROJECT=discuss
HOME=~/discuss
GUNICORN=gunicorn
LOGFILE=/dev/shm/$GUNICORN-$PROJECT.log
ACCESSLOGFILE=/dev/shm/$GUNICORN-$PROJECT-access.log
PIDFILE=/tmp/$GUNICORN-$PROJECT.pid
NUM_WORKERS=1
WORKER=gevent
ADDRESS=0.0.0.0:10002
APPFILE=core
APP=app

cd $HOME

$GUNICORN \
 --worker-class=$WORKER \
 --workers=$NUM_WORKERS \
 --pid=$PIDFILE \
 --log-file=$LOGFILE \
 --access-logfile=$ACCESSLOGFILE \
 --bind=$ADDRESS \
 --daemon \
$APPFILE:$APP
