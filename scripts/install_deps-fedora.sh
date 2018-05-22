#!/bin/bash
EXEC_DIR=$PWD
CMD=$0

dnf -y update

if [ "${CMD:0:1}" == "/" ]
then
    # absolute path
    DIR=`dirname ${CMD}`

else
    # relative path
    DIR=`dirname $( realpath $PWD/${CMD} )`

fi

INSTALL_DIR=`dirname $DIR`

echo "> Installing system dependencies..."

# libSigNetSim Dependencies
dnf -y install openmpi-devel openmpi \
                sundials sundials-devel \
                lapack-devel blas-devel atlas-devel atlas-static

#apt-get install -y libopenmpi-dev openmpi-bin \
#                    libsundials-serial-dev libsundials-serial \
#                    liblapack-dev libblas-dev libatlas-dev libatlas-base-dev

# Python 3 dependencies
#apt-get install -y python3-dev python3-pip python-virtualenv
dnf -y install python3-devel python3-pip python3-virtualenv gcc-c++

# Apache dependencies
dnf -y install httpd httpd-devel

# Misc dependencies
dnf install -y wget curl git swig
#apt-get install -y wget curl realpath git swig

echo "> Installing Python dependencies...";

virtualenv-3 -p python3 ${INSTALL_DIR}/venv

# Python Dependencies
${INSTALL_DIR}/venv/bin/pip install -i https://pypi.python.org/simple pip --upgrade
${INSTALL_DIR}/venv/bin/pip install setuptools --upgrade
${INSTALL_DIR}/venv/bin/easy_install -U distribute

${INSTALL_DIR}/venv/bin/pip install -r ${DIR}/pip_requirements --no-build-isolation

echo "> Installing JS dependencies...";

# JS Dependencies
curl -sL https://rpm.nodesource.com/setup_6.x | bash -
#apt-get install -y nodejs
dnf install -y nodejs
npm install -g yarn

cd $INSTALL_DIR

yarn install

cd $EXEC_DIR
