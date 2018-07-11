#!/bin/bash

RETURN_APACHE=`wget -q -O - localhost:80/success | tail -n 1`
echo "> Apache returned : ${RETURN_APACHE}"

RETURN_APACHE_STATIC=`wget -q -O - localhost:80/static/success | tail -n 1`
echo "> Apache returned : ${RETURN_APACHE_STATIC}"

if [ -z "${RETURN_APACHE}" ] && [ "${RETURN_APACHE}" == "SUCCESS" ] && [ -z "${RETURN_APACHE_STATIC}" ] && [ "${RETURN_APACHE_STATIC}" == "SUCCESS" ];
then
	exit 0;
else
	exit 1;
fi
