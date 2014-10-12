#!/usr/bin/env sh
rm data_genconf.db3
./manage.py migrate --noinput --verbosity=1
./manage.py loaddata auth_admin
