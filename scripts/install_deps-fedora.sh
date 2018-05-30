#!/bin/bash
EXEC_DIR=$PWD
CMD=$0
PYTHON_VERSION=$1

dnf -y update

if [ "${CMD:0:1}" == "/" ]
then
    # absolute path
    DIR=`dirname ${CMD}`

else
    # relative path
    DIR=`dirname $( readlink -e $PWD/${CMD} )`

fi

INSTALL_DIR=`dirname $DIR`

echo "> Installing system dependencies..."

# libSigNetSim Dependencies
dnf -y install openmpi-devel openmpi \
                sundials sundials-devel \
                lapack-devel blas-devel atlas-devel atlas-static

# Checking if mpicc is in /usr/bin
if [ ! -f /usr/bin/mpicc ] ; then
    mpicc_path=$(echo $(find /usr -name mpicc) | cut -d' ' -f1)
    ln -s ${mpicc_path} /usr/bin
fi

# Checking if mpirun is in /usr/bin
if [ ! -f /usr/bin/mpirun ] ; then
    mpirun_path=$(echo $(find /usr -name mpirun) | cut -d' ' -f1)
    ln -s ${mpirun_path} /usr/bin
fi

# Checking if libatlas is in /usr/lib
if [ ! -f /usr/lib/libatlas.so ] ; then
    ATLAS_PATH=$(find /usr -name libatlas.so)
    if [ -z "${ATLAS_PATH}" ] ; then
        ATLAS_PATH=$(find /usr -name libtatlas.so)
    fi

    ln -s ${ATLAS_PATH} /usr/lib/libatlas.so
fi


if [ "${PYTHON_VERSION}" == 2 ] ; then
    # Python 2 dependencies
    dnf -y install python-devel python-pip python-virtualenv gcc-c++

else
    # Python 3 dependencies
    dnf -y install python3-devel python3-pip python3-virtualenv gcc-c++

fi

# Apache dependencies
dnf -y install httpd httpd-devel

# Misc dependencies
dnf install -y wget curl git swig

echo "> Installing JS dependencies...";

# JS Dependencies
curl -sL https://rpm.nodesource.com/setup_6.x | bash -
dnf install -y nodejs
npm install -g yarn

cd $INSTALL_DIR

yarn install

cd $EXEC_DIR
