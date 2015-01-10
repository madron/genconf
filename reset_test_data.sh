#!/usr/bin/env sh
rm db.sqlite3
./manage.py migrate --noinput --verbosity=1
./manage.py loaddata auth_admin netcore_test.json genconf_test.json
