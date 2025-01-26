#!/bin/sh
set -a
. /api-flask/flaskenv.txt
set +a
exec python app.py