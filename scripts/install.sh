#!/bin/bash
EXEC_DIR=$PWD
DIR=`dirname $PWD/$0`
INSTALL_DIR=`dirname $DIR`
ROOT_DIR=$1


${DIR}/scripts/install_deps.sh
${DIR}/apache/install_apache.sh ${ROOT_DIR}
${DIR}/create_db.sh