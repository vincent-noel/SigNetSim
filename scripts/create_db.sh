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
mkdir -p ${INSTALL_DIR}/static

if [ ! -d ${INSTALL_DIR}/data/db ]
then

    mkdir -p ${INSTALL_DIR}/data/db
    mkdir -p ${INSTALL_DIR}/data/media

fi

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput > /dev/null

chgrp -R www-data ${INSTALL_DIR}/data
chmod -R 664 ${INSTALL_DIR}/data
find ${INSTALL_DIR}/data -type d  -exec chmod 775 {} \;

chgrp -R www-data ${INSTALL_DIR}/signetsim/settings
chmod -R 664 ${INSTALL_DIR}/signetsim/settings
find ${INSTALL_DIR}/signetsim/settings -type d  -exec chmod 775 {} \;


cd $EXEC_DIR
