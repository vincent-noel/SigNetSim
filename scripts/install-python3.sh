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


${DIR}/install_deps-python3.sh
${DIR}/apache-python3/install_apache.sh ${ROOT_DIR}
${DIR}/create_db-python3.sh

mkdir /var/www/.config
chown www-data:www-data /var/www/.config

mkdir /var/www/.cache
chown www-data:www-data /var/www/.cache