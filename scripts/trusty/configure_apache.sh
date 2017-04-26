EXEC_DIR=$PWD
DIR=`dirname $PWD/$0`
DIR=`dirname $DIR`
INSTALL_DIR=`dirname $DIR`

cp $DIR/apache_template $DIR/apache_conf
sed -i "s|___ROOT_DIR___|signetsim|g" $DIR/apache_conf
sed -i "s|___INSTALL_DIR___|$INSTALL_DIR|g" $DIR/apache_conf


cp /etc/apache2/sites-available/000-default.conf $DIR
NB_LINES=`wc -l $DIR/000-default.conf | cut -d' ' -f1`
POS_ENDVH=`cat $DIR/000-default.conf | grep -n /VirtualHost | cut -d: -f1`
POS_INSERT=`expr $POS_ENDVH - 1`
LINES_LEFT=`expr $NB_LINES - $POS_INSERT`

cat $DIR/000-default.conf | head -n $POS_INSERT > $DIR/signetsim.conf
cat $DIR/apache_conf >> $DIR/signetsim.conf
cat $DIR/000-default.conf | tail -n $LINES_LEFT >> $DIR/signetsim.conf

rm $DIR/000-default.conf $DIR/apache_conf

chgrp -R www-data $INSTALL_DIR/data/
#chgrp -R www-data $INSTALL_DIR/settings/

chmod -R 664 $INSTALL_DIR/data/
#chmod -R 664 $INSTALL_DIR/settings/

find $INSTALL_DIR/data/ -type d  -exec chmod 775 {} \;


mv $DIR/signetsim.conf /etc/apache2/sites-available/
cd /etc/apache2/sites-enabled/
a2dissite *
a2enmod wsgi
a2enmod rewrite
a2ensite signetsim
service apache2 restart
