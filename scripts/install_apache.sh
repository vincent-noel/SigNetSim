#!/bin/bash
EXEC_DIR=$PWD
DIR=`dirname $PWD/$0`
INSTALL_DIR=`dirname $DIR`

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
service apache2 reload
