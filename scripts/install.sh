#!/bin/bash
EXEC_DIR=$PWD
DIR=`dirname $PWD/$0`
DIR=`dirname $DIR`
INSTALL_DIR=`dirname $DIR`

apt-get install -y  \
    libopenmpi-dev openmpi-bin \
    libsundials-serial-dev libsundials-serial \
    liblapack-dev libblas-dev libatlas-dev libatlas-base-dev \
    git python-pip python-dev \
    gcc g++ make \
    unzip wget curl realpath gnupg \
    apache2 libapache2-mod-wsgi

pip install pip --upgrade
if [ ! -f /usr/bin/pip ]
then
    ln -s /usr/local/bin/pip /usr/bin/pip
fi

easy_install -U distribute

curl -sL https://deb.nodesource.com/setup_6.x | bash -
apt-get install nodejs
npm install -g bower

pip install -r $INSTALL_DIR/requirements.txt

cd $INSTALL_DIR

bower --allow-root install

cd $EXEC_DIR
