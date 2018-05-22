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


${INSTALL_DIR}/venv/bin/python manage.py makemigrations --noinput
${INSTALL_DIR}/venv/bin/python manage.py migrate --noinput
${INSTALL_DIR}/venv/bin/python manage.py collectstatic --noinput > /dev/null

APACHE_USER=`apachectl -S | grep User: | cut -d' ' -f2 | cut -d'=' -f2 | tr -d '"'`
APACHE_GROUP=`apachectl -S | grep Group: | cut -d' ' -f2 | cut -d'=' -f2 | tr -d '"'`

chgrp -R ${APACHE_GROUP} ${INSTALL_DIR}/signetsim/settings/wsgi.py
chmod -R 664 ${INSTALL_DIR}/signetsim/settings/wsgi.py

${INSTALL_DIR}/venv/bin/python manage.py runmodwsgi --setup-only \
    --port=80 \
    --user ${APACHE_USER} --group ${APACHE_GROUP} \
    --server-root=/etc/mod_wsgi-express-80 \
    --settings=signetsim.settings.apache \
    --url-alias /static ${INSTALL_DIR}/static/ \
    --url-alias /media ${INSTALL_DIR}/data/media/ \
    --reload-on-changes


cd $EXEC_DIR
