#!/usr/bin/env bash
MANAGE=python manage.py
FIXTURES=fixtures
# initial
$MANAGE migrate
$MANAGE collectstatic --noinput
$MANAGE loaddata "$FIXTURES/members/admin.json" "$FIXTURES/members/groups.json"

gunicorn --bind "0.0.0.0:$PORT" system.wsgi:application
