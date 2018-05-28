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

if [[ $(apt-cache search libsundials-serial | wc -l) -gt 0 ]]; then
    SUNDIALS_BIN="libsundials-serial"

elif [[ $(apt-cache search libsundials-nvecserial2 | wc -l) -gt 0 ]] && [[ $(apt-cache search libsundials-cvode2 | wc -l) -gt 0 ]] && [[ $(apt-cache search libsundials-ida2 | wc -l) -gt 0 ]] ; then
    SUNDIALS_BIN="libsundials-nvecserial2 libsundials-cvode2 libsundials-ida2"

else
    SUNDIALS_BIN=""

fi

if [[ $(apt-cache search libsundials-serial-dev | wc -l) -gt 0 ]]; then
    SUNDIALS_DEV="libsundials-serial-dev"

elif [[ $(apt-cache search libsundials-dev | wc -l) -gt 0 ]]; then
    SUNDIALS_DEV="libsundials-dev"

else
    SUNDIALS_DEV=""

fi

if [[ $(apt-cache search libatlas-dev | wc -l) -gt 0 ]]; then
    ATLAS_DEV="libatlas-dev"

elif [[ $(apt-cache search libatlas-base-dev | wc -l) -gt 0 ]]; then
    ATLAS_DEV="libatlas-base-dev"

else
    ATLAS_DEV=""

fi

# libSigNetSim Dependencies
apt-get install -y libopenmpi-dev openmpi-bin \
                    ${SUNDIALS_BIN} ${SUNDIALS_DEV} \
                    liblapack-dev libblas-dev ${ATLAS_DEV}

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
apt-get install -y wget curl realpath git swig  apt-transport-https

echo "> Installing JS dependencies...";

# JS Dependencies
curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
apt-get update -qq && apt-get install -y nodejs yarn

cd $INSTALL_DIR

yarn install

cd $EXEC_DIR
