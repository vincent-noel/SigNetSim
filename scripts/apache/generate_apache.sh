EXEC_DIR=$PWD
DIR=`dirname $( realpath $PWD/$0 )`
T_DIR=`dirname $DIR`
INSTALL_DIR=`dirname $T_DIR`
ROOT_DIR=$1

# Settings properly the folder.
# ROOT_DIR will be either blank or in the form /folder (or /folder/folder2)
# ROOT_DIR2 will be either / or in the form /folder (or /folder/folder2)
if [[ -z ${ROOT_DIR} ]];
then
    ROOT_DIR=""
    ROOT_DIR2="/"

else
    if [ ${ROOT_DIR:0:1} != "/" ]
    then
        ROOT_DIR=/${ROOT_DIR}
    fi

    if [ ${ROOT_DIR: -1} == "/" ]
    then
        ROOT_DIR=${ROOT_DIR::-1}
    fi
    ROOT_DIR2=${ROOT_DIR}
fi

cp $DIR/apache_template $DIR/apache_conf
sed -i "s|___ROOT_DIR___|$ROOT_DIR|g" $DIR/apache_conf
sed -i "s|___ROOT_DIR2___|$ROOT_DIR2|g" $DIR/apache_conf
sed -i "s|___INSTALL_DIR___|$INSTALL_DIR|g" $DIR/apache_conf


if [ ! -f ${INSTALL_DIR}/settings/settings.json ]
then
    cp signetsim/settings/settings.json settings/settings.json
fi
sed -i "s|  \"base_url\": \"/\"|  \"base_url\": \"$ROOT_DIR/\"|" $INSTALL_DIR/settings/settings.json
