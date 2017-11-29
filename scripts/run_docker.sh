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
DATA_DIR=$1

docker build -t signetsim:xenial $DIR/docker

if [[ -z "${DATA_DIR}" ]]
then
    docker run -dt --name signetsim_container -p 8080:80 signetsim:xenial bash
else
    docker run -dt --name signetsim_container -p 8080:80 \
                -v ${DATA_DIR}/data:/SigNetSim/data \
                signetsim:xenial bash
fi

docker exec signetsim_container /bin/bash /SigNetSim/scripts/install.sh