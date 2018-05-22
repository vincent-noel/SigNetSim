#!/bin/bash
EXEC_DIR=$PWD
CMD=$0
ROOT_DIR=$1


if [ "${CMD:0:1}" == "/" ]
then
    # absolute path
    DIR=`dirname ${CMD}`

else
    # relative path
    DIR=`dirname $( realpath $PWD/${CMD} )`

fi

INSTALL_DIR=`dirname $DIR`

DISTRIB=`cat /etc/os-release | grep ^ID= | cut -d'=' -f2`

if [ "${DISTRIB}" == "ubuntu" ] || [ "${DISTRIB}" == "debian" ]; then
    ${DIR}/install_deps.sh

elif [ "${DISTRIB}" == "fedora" ]; then
    ${DIR}/install_deps-fedora.sh

fi

mkdir -p ${INSTALL_DIR}/static
mkdir -p ${INSTALL_DIR}/tmp

if [ ! -d ${INSTALL_DIR}/data/db ]
then

    mkdir -p ${INSTALL_DIR}/data/db
    mkdir -p ${INSTALL_DIR}/data/media
    mkdir -p ${INSTALL_DIR}/data/settings

fi

${DIR}/create_db.sh

APACHE_USER=`apachectl -S | grep User: | cut -d' ' -f2 | cut -d'=' -f2 | tr -d '"'`
APACHE_GROUP=`apachectl -S | grep Group: | cut -d' ' -f2 | cut -d'=' -f2 | tr -d '"'`

chgrp -R ${APACHE_GROUP} ${INSTALL_DIR}/data
chmod -R 664 ${INSTALL_DIR}/data
find ${INSTALL_DIR}/data -type d  -exec chmod 775 {} \;

chgrp -R ${APACHE_GROUP} ${INSTALL_DIR}/tmp
chmod -R 664 ${INSTALL_DIR}/tmp
find ${INSTALL_DIR}/tmp -type d  -exec chmod 775 {} \;

mkdir /var/www/.config
chgrp ${APACHE_GROUP} /var/www/.config
chmod 664 /var/www/.config

mkdir /var/www/.cache
chgrp ${APACHE_GROUP} /var/www/.cache
chmod 664 /var/www/.cache

/etc/mod_wsgi-express-80/apachectl start