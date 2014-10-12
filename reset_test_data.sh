#!/usr/bin/env sh
rm db.sqlite3
./manage.py migrate --noinput --verbosity=1
./manage.py loaddata auth_admin genconf_test.json
