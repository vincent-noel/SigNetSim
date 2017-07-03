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

# Gettings apache version
APACHE_FULLVERSION=`apache2 -v | head -n 1 | cut -d" " -f3 | cut -d"/" -f2`
APACHE_VERSION=`echo $APACHE_FULLVERSION | cut -d"." -f1`
APACHE_SUBVERSION=`echo $APACHE_FULLVERSION | cut -d"." -f2`

if [ "${APACHE_VERSION}" -eq 2 ]
then
    if [ "${APACHE_SUBVERSION}" -ge 3 ]
    then echo "greater than 2.3"

    else
        if [ "${APACHE_SUBVERSION}" -ge 1 ]
        then echo "greater than 2.1"
        else echo "Apache version ($APACHE_VERSION.$APACHE_SUBVERSION) not supported"
        fi
    fi
else echo "Apache version ($APACHE_VERSION.$APACHE_SUBVERSION) not supported"
fi

#sed -i "s|BASE_URL = \"/\"|BASE_URL = \"$ROOT_DIR/\"|" $INSTALL_DIR/settings/apache.py

#cp $DIR/apache_template $DIR/apache_conf
#sed -i "s|___ROOT_DIR___|$ROOT_DIR|g" $DIR/apache_conf
#sed -i "s|___ROOT_DIR2___|$ROOT_DIR2|g" $DIR/apache_conf
#sed -i "s|___INSTALL_DIR___|$INSTALL_DIR|g" $DIR/apache_conf


#cp /etc/apache2/sites-available/000-default.conf $DIR
#NB_LINES=`wc -l $DIR/000-default.conf | cut -d' ' -f1`
#POS_ENDVH=`cat $DIR/000-default.conf | grep -n /VirtualHost | cut -d: -f1`
#POS_INSERT=`expr $POS_ENDVH - 1`
#LINES_LEFT=`expr $NB_LINES - $POS_INSERT`

#cat $DIR/000-default.conf | head -n $POS_INSERT > $DIR/signetsim.conf
#cat $DIR/apache_conf >> $DIR/signetsim.conf
#cat $DIR/000-default.conf | tail -n $LINES_LEFT >> $DIR/signetsim.conf

#rm $DIR/000-default.conf $DIR/apache_conf

#chgrp -R www-data $INSTALL_DIR/data/
#chmod -R 664 $INSTALL_DIR/data/
#find $INSTALL_DIR/data/ -type d  -exec chmod 775 {} \;


#mv $DIR/signetsim.conf /etc/apache2/sites-available/
#cd /etc/apache2/sites-enabled/
#a2dissite *
#a2enmod wsgi
#a2enmod rewrite
#a2ensite signetsim
#service apache2 restart
