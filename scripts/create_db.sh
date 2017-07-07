#!/bin/bash
EXEC_DIR=$PWD
CMD=$0

if [ "${CMD:0:1}" == "/" ]
then
    # absolute path
    DIR=`dirname ${CMD}`

else
    # relative path
    DIR=`dirname $( realpath $PWD/${CMD} )`

fi
INSTALL_DIR=`dirname $DIR`

cd ${INSTALL_DIR}

mkdir -p ${INSTALL_DIR}/signetsim/static/mpld3
cp -r /usr/local/lib/python2.7/dist-packages/mpld3/js/d3.v3.min.js ${INSTALL_DIR}/signetsim/static/mpld3/
cp -r /usr/local/lib/python2.7/dist-packages/mpld3/js/mpld3.v0.3.min.js ${INSTALL_DIR}/signetsim/static/mpld3/
mkdir ${INSTALL_DIR}/static

if [ ! -d ${INSTALL_DIR}/data/db ]
then

    mkdir -p ${INSTALL_DIR}/data/db
    mkdir -p ${INSTALL_DIR}/data/media

    python manage.py makemigrations --noinput
    python manage.py migrate --noinput
    python manage.py collectstatic --noinput > /dev/null

    echo "from signetsim.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

else

    python manage.py makemigrations --noinput
    python manage.py migrate --noinput
    python manage.py collectstatic --noinput > /dev/null

fi


chgrp -R www-data ${INSTALL_DIR}/data
chmod -R 664 ${INSTALL_DIR}/data
find ${INSTALL_DIR}/data -type d  -exec chmod 775 {} \;

cd $EXEC_DIR
