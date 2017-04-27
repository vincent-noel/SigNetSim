#!/bin/bash
EXEC_DIR=$PWD
DIR=`dirname $PWD/$0`
INSTALL_DIR=`dirname $DIR`

docker build -t signetsim:xenial $DIR/docker
docker run -d -p 8080:80 signetsim:xenial /usr/sbin/apache2ctl -D FOREGROUND