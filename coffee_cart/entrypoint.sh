#!/bin/sh
set -e

/app/coffee_cart/manage.py makemigrations menu_backend
/app/coffee_cart/manage.py migrate

/app/coffee_cart/manage.py runserver 0.0.0.0:8000

exec "$@"