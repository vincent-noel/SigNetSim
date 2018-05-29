#!/bin/bash
EXEC_DIR=$PWD
CMD=$0
PYTHON_VERSION=$1

yum -y install epel-release
yum -y makecache

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
yum -y install openmpi openmpi-devel \
                sundials sundials-devel \
                lapack-devel blas-devel atlas-devel

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
    yum -y install python2-devel python2-pip python2-virtualenv gcc-c++

else
    # Python 3 dependencies
    yum -y install python34-devel python34-pip python34-virtualenv gcc-c++

fi

# Apache dependencies
yum -y install httpd httpd-devel

# Misc dependencies
yum -y install wget curl git swig make

echo "> Installing JS dependencies...";

# JS Dependencies
curl --silent --location https://dl.yarnpkg.com/rpm/yarn.repo | tee /etc/yum.repos.d/yarn.repo
curl -sL https://rpm.nodesource.com/setup_6.x | bash -
yum -y install yarn

cd $INSTALL_DIR

yarn install

cd $EXEC_DIR
