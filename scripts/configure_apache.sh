EXEC_DIR=$PWD
DIR=`dirname $PWD/$0`
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
