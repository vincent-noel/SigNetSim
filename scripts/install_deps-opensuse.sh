#!/bin/bash
EXEC_DIR=$PWD
CMD=$0
PYTHON_VERSION=$1
DISTRIB_NAME=`cat /etc/os-release| grep PRETTY_NAME | cut -d'=' -f2 | tr -d '"' | tr ' ' '_'`

zypper ar -f https://download.opensuse.org/repositories/science/${DISTRIB_NAME}/ repo-science
zypper ar -f https://download.opensuse.org/repositories/home:/beyerle:/IAC/${DISTRIB_NAME}/ beyerle
zypper --no-gpg-checks refresh

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
zypper -n install openmpi-devel openmpi \
                sundials sundials-devel \
                lapack-devel blas-devel libatlas3-basic-devel


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
    zypper -n install python2-devel python2-pip python2-virtualenv gcc-c++

else
    # Python 3 dependencies
    zypper -n install python3-devel python3-pip python3-virtualenv gcc-c++

fi

# Apache dependencies
zypper -n install w3m lynx apache2 apache2-devel

# Misc dependencies
zypper -n install wget curl git swig tar nodejs make

echo "> Installing JS dependencies...";

# JS Dependencies
curl -o- -L https://yarnpkg.com/install.sh | bash
ln -s $HOME/.yarn/bin/yarn /usr/bin

cd $INSTALL_DIR

yarn install

cd $EXEC_DIR
