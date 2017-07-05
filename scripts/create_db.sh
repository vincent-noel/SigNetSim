#!/bin/bash
EXEC_DIR=$PWD
DIR=`dirname $PWD/$0`
DIR=`dirname $DIR`
INSTALL_DIR=`dirname $DIR`

cd ${INSTALL_DIR}
pwd
ls -al
mkdir -p ${INSTALL_DIR}data/db
mkdir -p ${INSTALL_DIR}data/media
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput > /dev/null
echo "from signetsim.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

cd $EXEC_DIR
