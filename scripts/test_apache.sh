#!/bin/bash

RETURN_APACHE=`wget -q -O - localhost:80/signetsim/success/ | tail -n 1`
RES=`expr $RETURN_APACHE  == SUCCESS`

echo "Return Apache : " $RETURN_APACHE

if [ $RES = 1 ]; then
	exit 0;
else
	exit 1;
fi