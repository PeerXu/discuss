#!/bin/bash

set -e

PROJECT=discuss
GUNICORN=gunicorn

PIDFILE=/tmp/$GUNICORN-$PROJECT.pid

kill -9 `cat $PIDFILE`
