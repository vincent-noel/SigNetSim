EXEC_DIR=$PWD
DIR=`dirname $PWD/$0`
T_DIR=`dirname $DIR`
INSTALL_DIR=`dirname $T_DIR`

cp $DIR/apache_template $DIR/apache_conf
sed -i "s|___ROOT_DIR___|signetsim|g" $DIR/apache_conf
sed -i "s|___INSTALL_DIR___|$INSTALL_DIR|g" $DIR/apache_conf


cp /etc/apache2/sites-available/default $DIR
NB_LINES=`wc -l $DIR/default | cut -d' ' -f1`
POS_ENDVH=`cat $DIR/default | grep -n /VirtualHost | cut -d: -f1`
POS_INSERT=`expr $POS_ENDVH - 1`
LINES_LEFT=`expr $NB_LINES - $POS_INSERT`

cat $DIR/default | head -n $POS_INSERT > $DIR/signetsim
cat $DIR/apache_conf >> $DIR/signetsim
cat $DIR/default | tail -n $LINES_LEFT >> $DIR/signetsim

rm $DIR/default $DIR/apache_conf

chgrp -R www-data $INSTALL_DIR/data/
#chgrp -R www-data $INSTALL_DIR/settings/

chmod -R 664 $INSTALL_DIR/data/
#chmod -R 664 $INSTALL_DIR/settings/

find $INSTALL_DIR/data/ -type d  -exec chmod 775 {} \;


mv $DIR/signetsim /etc/apache2/sites-available/
cd /etc/apache2/sites-enabled/
a2dissite *
a2enmod wsgi
a2enmod rewrite
a2ensite signetsim
service apache2 restart
