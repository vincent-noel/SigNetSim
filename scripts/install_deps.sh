#!/bin/bash
EXEC_DIR=$PWD
CMD=$0

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
if [ ! -f /usr/bin/pip ]
then
    ln -s /usr/local/bin/pip /usr/bin/pip
fi

easy_install -U distribute

pip install -r ${DIR}/pip_requirements

# JS Dependencies
curl -sL https://deb.nodesource.com/setup_6.x | bash -
apt-get install -y nodejs
npm install -g bower

cd $INSTALL_DIR

bower --allow-root install

cd $EXEC_DIR
