#!/bin/bash
EXEC_DIR=$PWD
DIR=`dirname $PWD/$0`
INSTALL_DIR=`dirname $DIR`
DATA_DIR=$1

docker build -t signetsim:xenial $DIR/docker

if [[ -z ${DATA_DIR} ]]
then
    docker run -d --name signetsim_container -p 8080:80 signetsim:xenial /SigNetSim/scripts/create_db
else
    docker run -d --name signetsim_container -p 8080:80 -v ${DATA_DIR}:/SigNetSim/data signetsim:xenial /SigNetSim/scripts/create_db
fi

docker exec -d signetsim_container /usr/sbin/apache2ctl -D FOREGROUND
