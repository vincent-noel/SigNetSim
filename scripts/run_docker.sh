#!/bin/bash
EXEC_DIR=$PWD
DIR=`dirname $PWD/$0`
INSTALL_DIR=`dirname $DIR`
DATA_DIR=$1

docker build -t signetsim:xenial $DIR/docker
if [[ -z "${DATA_DIR}" ]]
then
    docker run -d --name signetsim_container -p 8080:80 signetsim:xenial usr/sbin/apache2ctl -D FOREGROUND
else
    docker run -d --name signetsim_container -p 8080:80 -v ${DATA_DIR}:/SigNetSim/data signetsim:xenial usr/sbin/apache2ctl -D FOREGROUND
fi

if [ ! -d "${DATA_DIR}/db" ]
then
    docker exec -d signetsim_container /bin/bash /SigNetSim/scripts/create_db.sh
fi