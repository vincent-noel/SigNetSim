#!/bin/bash
EXEC_DIR=$PWD
DIR=`dirname $PWD/$0`
DIR=`dirname $DIR`
INSTALL_DIR=`dirname $DIR`

apt-get install -y libopenmpi-dev openmpi-bin libsundials-serial-dev libsundials-serial liblapack-dev libblas-dev libatlas-dev libfreetype6-dev libpng12-dev libatlas-base-dev python-dev python-pip python-setuptools git subversion gfortran g++ gcc make pkg-config unzip wget apache2 libapache2-mod-wsgi npm nodejs-legacy graphviz
pip install -r $INSTALL_DIR/requirements.txt

cd $INSTALL_DIR


bower --allow-root install

mkdir -p signetsim/static/mpld3
cp -r /usr/local/lib/python2.7/dist-packages/mpld3/js/d3.v3.min.js signetsim/static/mpld3/
cp -r /usr/local/lib/python2.7/dist-packages/mpld3/js/mpld3.v0.3.min.js signetsim/static/mpld3/



mkdir -p data/db
mkdir -p data/media

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput > /dev/null

cd $EXEC_DIR
