CMD=$0

if [ "${CMD:0:1}" == "/" ]
then
    # absolute path
    DIR=`dirname ${CMD}`

else
    # relative path
    DIR=`dirname $( readlink -e $PWD/${CMD} )`

fi

INSTALL_DIR=`dirname $DIR`

cd ${INSTALL_DIR}

${INSTALL_DIR}/venv/bin/coverage run -a manage.py test --settings=signetsim.settings.test -v 2 || exit 1;
