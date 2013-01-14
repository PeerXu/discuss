#!/bin/bash

set -e

PIDFILE=/tmp/gunicorn.pid

kill -9 `cat $PIDFILE`
