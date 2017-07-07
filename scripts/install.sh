#!/bin/bash
EXEC_DIR=$PWD
CMD=$0

if [ "${CMD:0:1}" = "/" ]
then
    # absolute path
    DIR=`dirname ${CMD}`

else
    # relative path
    DIR=`dirname $( realpath $PWD/${CMD} )`

fi

INSTALL_DIR=`dirname $DIR`
ROOT_DIR=$1


${DIR}/install_deps.sh
${DIR}/apache/install_apache.sh ${ROOT_DIR}
${DIR}/create_db.sh