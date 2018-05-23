#!/bin/bash
EXEC_DIR=$PWD
CMD=$0
PYTHON_VERSION=$1

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

echo "> Installing system dependencies..."

# libSigNetSim Dependencies
apt-get install -y libopenmpi-dev openmpi-bin \
                    libsundials-serial-dev libsundials-serial \
                    liblapack-dev libblas-dev libatlas-dev libatlas-base-dev

if [ "${PYTHON_VERSION}" == 2 ] ; then
    # Python 2 dependencies
    apt-get install -y python-dev python-pip python-virtualenv

else
    # Python 3 dependencies
    apt-get install -y python-dev python3-dev python3-pip python-virtualenv

fi

# Apache dependencies
if apt-cache show apache2-dev &> /dev/null; then
    apt-get install -y apache2 apache2-dev

elif apt-cache show apache2-threaded-dev &> /dev/null; then
    apt-get install -y apache2 apache2-threaded-dev

elif apt-cache show apache2-prefork-dev &> /dev/null; then
    apt-get install -y apache2 apache2-prefork-dev

else
    echo "> Could not find apache2 development header !";

fi

# Misc dependencies
apt-get install -y wget curl realpath git swig


echo "> Installing Python dependencies...";

virtualenv ${INSTALL_DIR}/venv

# Python Dependencies
${INSTALL_DIR}/venv/bin/pip install -i https://pypi.python.org/simple pip --upgrade
${INSTALL_DIR}/venv/bin/pip install distribute setuptools --upgrade

${INSTALL_DIR}/venv/bin/pip install -r ${DIR}/pip_requirements --no-build-isolation

echo "> Installing JS dependencies...";

# JS Dependencies
curl -sL https://deb.nodesource.com/setup_6.x | bash -
apt-get install -y nodejs
npm install -g yarn

cd $INSTALL_DIR

yarn install

cd $EXEC_DIR
