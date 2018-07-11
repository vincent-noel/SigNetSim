#!/bin/bash
EXEC_DIR=$PWD
CMD=$0

GLOBAL=1
PORT=80
PYTHON_VERSION=3

# Reading arguments
POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -g|--global)
    GLOBAL=1
    shift # past argument
    ;;
    -py|--python)
    PYTHON_VERSION="$2"
    shift # past argument
    shift # past value
    ;;
    -p|--port)
    PORT="$2"
    shift # past argument
    shift # past value
    ;;
    *)    # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift # past argument
    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

echo GLOBAL          = "${GLOBAL}"
echo PYTHON_VERSION  = "${PYTHON_VERSION}"
echo PORT            = "${PORT}"

if [ "${CMD:0:1}" == "/" ]
then
    # absolute path
    DIR=`dirname ${CMD}`

else
    # relative path
    DIR=`dirname $( readlink -e $PWD/${CMD} )`

fi

INSTALL_DIR=`dirname $DIR`

DISTRIB=`cat /etc/os-release | grep ^ID= | cut -d'=' -f2 | tr -d '"'`

if [ "${DISTRIB}" == "ubuntu" ] || [ "${DISTRIB}" == "debian" ]; then
    ${DIR}/install_deps-debian.sh ${PYTHON_VERSION}

elif [ "${DISTRIB}" == "fedora" ]; then
    ${DIR}/install_deps-fedora.sh ${PYTHON_VERSION}

elif [ "${DISTRIB}" == "centos" ]; then
    ${DIR}/install_deps-centos.sh ${PYTHON_VERSION}

elif [ "${DISTRIB}" == "opensuse" ] || [ "${DISTRIB}" == "opensuse-leap" ]; then
    ${DIR}/install_deps-opensuse.sh ${PYTHON_VERSION}

fi

echo "> Installing Python dependencies...";

if [ "${PYTHON_VERSION}" == 2 ] ; then
    virtualenv ${INSTALL_DIR}/venv

else
    if [ "${DISTRIB}" == "fedora" ] || [ "${DISTRIB}" == "centos" ]; then
        virtualenv-3 -p python3 ${INSTALL_DIR}/venv

    else
        virtualenv -p python3 ${INSTALL_DIR}/venv

    fi
fi

# Python Dependencies
${INSTALL_DIR}/venv/bin/pip install -i https://pypi.python.org/simple pip --upgrade
${INSTALL_DIR}/venv/bin/easy_install --upgrade distribute
${INSTALL_DIR}/venv/bin/pip install setuptools distribute --upgrade

${INSTALL_DIR}/venv/bin/pip install -r ${DIR}/pip_requirements --no-build-isolation


APACHE_USER=`apachectl -S | grep User: | cut -d' ' -f2 | cut -d'=' -f2 | tr -d '"'`
APACHE_GROUP=`apachectl -S | grep Group: | cut -d' ' -f2 | cut -d'=' -f2 | tr -d '"'`
if [ -z "$APACHE_USER" ]; then
    source /etc/apache2/envvars
    APACHE_USER=${APACHE_RUN_USER}
    APACHE_GROUP=${APACHE_RUN_GROUP}
fi

mkdir -p ${INSTALL_DIR}/static
mkdir -p ${INSTALL_DIR}/tmp

if [ ! -d ${INSTALL_DIR}/data/db ]
then

    mkdir -p ${INSTALL_DIR}/data/db
    mkdir -p ${INSTALL_DIR}/data/media
    mkdir -p ${INSTALL_DIR}/data/settings

fi

chgrp -R ${APACHE_GROUP} ${INSTALL_DIR}/data
chmod -R 664 ${INSTALL_DIR}/data
find ${INSTALL_DIR}/data -type d  -exec chmod 775 {} \;

chgrp -R ${APACHE_GROUP} ${INSTALL_DIR}/tmp
chmod -R 664 ${INSTALL_DIR}/tmp
find ${INSTALL_DIR}/tmp -type d  -exec chmod 775 {} \;

mkdir /var/www/.config
chgrp ${APACHE_GROUP} /var/www/.config
chmod 664 /var/www/.config

mkdir /var/www/.cache
chgrp ${APACHE_GROUP} /var/www/.cache
chmod 664 /var/www/.cache

${DIR}/create_db.sh ${GLOBAL} ${PORT}

chgrp ${APACHE_GROUP}  ${INSTALL_DIR}/data/db/db.sqlite3
chmod 664  ${INSTALL_DIR}/data/db/db.sqlite3

if [ ${GLOBAL} == 1 ] ; then
    SERVICE_DIR=/etc/signetsim

else
    SERVICE_DIR=${INSTALL_DIR}/service

fi

${SERVICE_DIR}/apachectl start