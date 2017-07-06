#!/bin/bash
EXEC_DIR=$PWD
DIR=`dirname $PWD/$0`
INSTALL_DIR=`dirname $DIR`

cd ${INSTALL_DIR}

mkdir -p signetsim/static/mpld3
cp -r /usr/local/lib/python2.7/dist-packages/mpld3/js/d3.v3.min.js signetsim/static/mpld3/
cp -r /usr/local/lib/python2.7/dist-packages/mpld3/js/mpld3.v0.3.min.js signetsim/static/mpld3/
mkdir static

if [ ! -d ${INSTALL_DIR}/data/db ]
then

    mkdir -p data/db
    mkdir -p data/media

    python manage.py makemigrations --noinput
    python manage.py migrate --noinput
    python manage.py collectstatic --noinput > /dev/null

    echo "from signetsim.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

else

    python manage.py makemigrations --noinput
    python manage.py migrate --noinput
    python manage.py collectstatic --noinput > /dev/null

fi


mkdir -p settings
if [ ! -f ${INSTALL_DIR}/settings/settings.json ]
then
    cp signetsim/settings/settings.json settings/settings.json
fi

chgrp -R www-data data
chmod -R 664 data
find data -type d  -exec chmod 775 {} \;

cd $EXEC_DIR
