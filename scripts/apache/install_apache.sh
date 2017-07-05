EXEC_DIR=$PWD
DIR=`dirname $( realpath $PWD/$0 )`
T_DIR=`dirname $DIR`
INSTALL_DIR=`dirname $T_DIR`
ROOT_DIR=$1

APACHE_ACTIVE_CONF_NAME=`ls /etc/apache2/sites-enabled/`
NB_ACTIVE_CONF=`echo ${APACHE_ACTIVE_CONF_NAME} | wc -w`


if [ "${NB_ACTIVE_CONF}" -eq 1 ]
then

    APACHE_ACTIVE_CONF=`realpath /etc/apache2/sites-enabled/$( readlink /etc/apache2/sites-enabled/${APACHE_ACTIVE_CONF_NAME} )`
    cp ${APACHE_ACTIVE_CONF} ${DIR}
    NB_LINES=`wc -l $DIR/$( basename ${APACHE_ACTIVE_CONF} ) | cut -d' ' -f1`
    POS_ENDVH=`cat $DIR/$( basename ${APACHE_ACTIVE_CONF} ) | grep -n /VirtualHost | cut -d: -f1`
    POS_INSERT=`expr $POS_ENDVH - 1`
    LINES_LEFT=`expr $NB_LINES - $POS_INSERT`

    cat $DIR/$( basename ${APACHE_ACTIVE_CONF} ) | head -n $POS_INSERT > $DIR/signetsim.conf
    cat $DIR/apache_conf >> $DIR/signetsim.conf
    cat $DIR/$( basename ${APACHE_ACTIVE_CONF} ) | tail -n $LINES_LEFT >> $DIR/signetsim.conf

    rm $DIR/$( basename ${APACHE_ACTIVE_CONF} ) $DIR/apache_conf

    mv $DIR/signetsim.conf /etc/apache2/sites-available/
    cd /etc/apache2/sites-enabled/
    a2dissite ${APACHE_ACTIVE_CONF_NAME}
    a2enmod wsgi
    a2enmod rewrite
    a2ensite signetsim.conf
    service apache2 restart
else
    echo "More than one active configuration in apache."
fi

#chgrp -R www-data $INSTALL_DIR/data/
#chmod -R 664 $INSTALL_DIR/data/
#find $INSTALL_DIR/data/ -type d  -exec chmod 775 {} \;

