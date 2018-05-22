#!/bin/bash
EXEC_DIR=$PWD
CMD=$0
ROOT_DIR=$1

GLOBAL=1
PORT=80

if [ "${CMD:0:1}" == "/" ]
then
    # absolute path
    DIR=`dirname ${CMD}`

else
    # relative path
    DIR=`dirname $( realpath $PWD/${CMD} )`

fi

INSTALL_DIR=`dirname $DIR`


${DIR}/install_deps-python3.sh

mkdir -p ${INSTALL_DIR}/static
mkdir -p ${INSTALL_DIR}/tmp

if [ ! -d ${INSTALL_DIR}/data/db ]
then

    mkdir -p ${INSTALL_DIR}/data/db
    mkdir -p ${INSTALL_DIR}/data/media
    mkdir -p ${INSTALL_DIR}/data/settings

fi

chgrp -R www-data ${INSTALL_DIR}/data
chmod -R 664 ${INSTALL_DIR}/data
find ${INSTALL_DIR}/data -type d  -exec chmod 775 {} \;

chgrp -R www-data ${INSTALL_DIR}/tmp
chmod -R 664 ${INSTALL_DIR}/tmp
find ${INSTALL_DIR}/tmp -type d  -exec chmod 775 {} \;

mkdir /var/www/.config
chown www-data:www-data /var/www/.config

mkdir /var/www/.cache
chown www-data:www-data /var/www/.cache

${DIR}/create_db.sh ${GLOBAL} ${PORT}


if [ ${GLOBAL} -eq 1 ] ; then
    SERVICE_DIR=${INSTALL_DIR}/service

else
    SERVICE_DIR=/etc/signetsim

fi

${SERVICE_DIR}/apachectl start