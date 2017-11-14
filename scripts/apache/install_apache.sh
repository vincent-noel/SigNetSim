EXEC_DIR=$PWD
CMD=$0

if [ "${CMD:0:1}" == "/" ]
then
    # absolute path
    DIR=`dirname ${CMD}`

else
    # relative path
    DIR=`dirname $( realpath $PWD/${CMD} )`

fi

T_DIR=`dirname $DIR`
INSTALL_DIR=`dirname $T_DIR`
ROOT_DIR=$1

# Generating the template to be added to apache conf
${DIR}/generate_apache.sh ${ROOT_DIR}

# Detecting active apache configurations
APACHE_ACTIVE_CONF_NAME=`ls /etc/apache2/sites-enabled/`
NB_ACTIVE_CONF=`echo ${APACHE_ACTIVE_CONF_NAME} | wc -w`

# If there is just one, then we add signetsim configuration to that one
if [ "${NB_ACTIVE_CONF}" -eq 1 ]
then

    # Getting the real filename, which is linked to in site-enabled
    APACHE_ACTIVE_CONF=`realpath /etc/apache2/sites-enabled/$( readlink /etc/apache2/sites-enabled/${APACHE_ACTIVE_CONF_NAME} )`

    # And we copy it
    cp ${APACHE_ACTIVE_CONF} ${DIR}

    # We look for the end of the virtualhost configuration
    NB_LINES=`wc -l $DIR/$( basename ${APACHE_ACTIVE_CONF} ) | cut -d' ' -f1`
    POS_ENDVH=`cat $DIR/$( basename ${APACHE_ACTIVE_CONF} ) | grep -n /VirtualHost | cut -d: -f1`
    POS_INSERT=`expr $POS_ENDVH - 1`
    LINES_LEFT=`expr $NB_LINES - $POS_INSERT`

    # We insert the active config
    cat $DIR/$( basename ${APACHE_ACTIVE_CONF} ) | head -n $POS_INSERT > $DIR/signetsim.conf

    # Then ours
    cat $DIR/apache_conf >> $DIR/signetsim.conf

    # Then the rest of the file
    cat $DIR/$( basename ${APACHE_ACTIVE_CONF} ) | tail -n $LINES_LEFT >> $DIR/signetsim.conf

    # We delete our config file
    rm $DIR/$( basename ${APACHE_ACTIVE_CONF} ) $DIR/apache_conf

    # We add the new config to the apache folder
    mv $DIR/signetsim.conf /etc/apache2/sites-available/

    # We inactivate the previous one
    a2dissite ${APACHE_ACTIVE_CONF_NAME}

    # Activate wsgi module
    a2enmod wsgi

    # Activate our new configuration
    a2ensite signetsim.conf

    # And finally restart apache
    service apache2 restart

else
    echo "More than one active configuration in apache, we prefer to let you do."
    echo "Please insert the content of apache_conf in the proper configuration"

fi

# We make the settings folders in case if doesn't already exists
mkdir -p ${INSTALL_DIR}/data/settings

# We copy the default settings files if it doesn't already exists
if [ ! -f ${INSTALL_DIR}/data/settings/settings.json ]
then
    cp ${INSTALL_DIR}/signetsim/settings/settings.json ${INSTALL_DIR}/data/settings/settings.json
fi

# And finally we write the proper apache folder in signetsim settings
sed -i "s|  \"base_url\": \"/\"|  \"base_url\": \"$ROOT_DIR/\"|" $INSTALL_DIR/data/settings/settings.json
