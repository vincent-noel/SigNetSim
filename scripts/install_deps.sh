#!/bin/bash
EXEC_DIR=$PWD
CMD=$0

apt-get -qq update
apt-get install -y realpath

if [ "${CMD:0:1}" == "/" ]
then
    # absolute path
    DIR=`dirname ${CMD}`

else
    # relative path
    DIR=`dirname $( realpath $PWD/${CMD} )`

fi

INSTALL_DIR=`dirname $DIR`

# System Dependencies
apt-get install -y $( cat ${DIR}/apt_requirements )


# Python Dependencies
pip install pip --upgrade

PIP_VERSION=`pip --version`
LOCAL_PIP_VERSION=`/usr/local/bin/pip --version`

if [ -z "$PIP_VERSION" ] && [ ! -z "$LOCAL_PIP_VERSION" ];
then
    if [ -f /usr/bin/pip ];
    then
        rm /usr/bin/pip
    fi

    ln -s /usr/local/bin/pip /usr/bin/pip
fi

easy_install -U distribute

pip install -r ${DIR}/pip_requirements

# JS Dependencies
curl -sL https://deb.nodesource.com/setup_6.x | bash -
apt-get install -y nodejs
npm install -g yarn

cd $INSTALL_DIR

yarn install

cd $EXEC_DIR
