#!/bin/bash
EXEC_DIR=$PWD
CMD=$0
GLOBAL=$1
PORT=$2

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

${INSTALL_DIR}/venv/bin/python manage.py makemigrations --noinput
${INSTALL_DIR}/venv/bin/python manage.py migrate --noinput
${INSTALL_DIR}/venv/bin/python manage.py collectstatic --noinput > /dev/null

APACHE_USER=`apachectl -S | grep User: | cut -d' ' -f2 | cut -d'=' -f2 | tr -d '"'`
APACHE_GROUP=`apachectl -S | grep Group: | cut -d' ' -f2 | cut -d'=' -f2 | tr -d '"'`

if [ -z "$APACHE_USER" ]; then
    source /etc/apache2/envvars
    APACHE_USER=${APACHE_RUN_USER}
    APACHE_GROUP=${APACHE_RUN_GROUP}
fi

chgrp -R ${APACHE_GROUP} ${INSTALL_DIR}/signetsim/settings/wsgi.py
chmod -R 664 ${INSTALL_DIR}/signetsim/settings/wsgi.py

if [ ${GLOBAL} -eq 1 ] ; then
    SERVICE_DIR=${INSTALL_DIR}/service

else
    SERVICE_DIR=/etc/signetsim
    APACHE_USER=$USER
    APACHE_GROUP=$GROUP
fi

${INSTALL_DIR}/venv/bin/python manage.py runmodwsgi --setup-only \
    --port ${PORT} \
    --user ${APACHE_USER} --group ${APACHE_GROUP} \
    --server-root=${SERVICE_DIR} \
    --settings=signetsim.settings.apache \
    --url-alias /static ${INSTALL_DIR}/static/ \
    --url-alias /media ${INSTALL_DIR}/data/media/ \
    --python-path ${INSTALL_DIR} \
    --working-directory ${INSTALL_DIR}/tmp/ \
    --reload-on-changes

cd $EXEC_DIR
