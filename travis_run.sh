#!/bin/bash
echo $1
if [ $1 = "docker" ]; then
    if [ $2 = "before_install" ]; then
        pip install -U docker-compose || exit 1;
        docker login -u signetsim -p $4

    elif [ $2 = "install" ]; then
        docker-compose build signetsim || exit 1;

    elif [ $2 = "script" ]; then
        docker run --name signetsim -p 80:80 -d signetsim/signetsim:develop || exit 1;

        APACHE_RETURN=`wget -q -O - localhost:80 | grep \<title\> | cut -d">" -f2 | cut -d" " -f1`
        if [ -n "${APACHE_RETURN}" ] && [ "${APACHE_RETURN}" == "Install" ];
        then
            exit 0;
        else
            exit 1;
        fi


    elif [ $2 = "after_script" ]; then
        docker push signetsim/signetsim:develop || exit 1;

    fi

else

    if [ $2 = "before_install" ]; then
        docker pull $1 || exit 1;

    elif [ $2 = "install" ]; then
        docker run -di --name test_env -v $(pwd):/home/travis/build/vincent-noel/SigNetSim $1 bash
        docker exec test_env /bin/bash /home/travis/build/vincent-noel/SigNetSim/scripts/install.sh --python $3

    elif [ $2 = "script" ]; then

        APACHE_USER=`docker exec test_env /bin/bash apachectl -S | grep User: | cut -d' ' -f2 | cut -d'=' -f2 | tr -d '"'`
        APACHE_GROUP=`docker exec test_env /bin/bash apachectl -S | grep Group: | cut -d' ' -f2 | cut -d'=' -f2 | tr -d '"'`

        if [ -z "$APACHE_USER" ]; then
            source /etc/apache2/envvars
            APACHE_USER=`docker exec test_env /bin/bash -c 'source /etc/apache2/envvars; echo "${APACHE_RUN_USER}"'`
            APACHE_GROUP=`docker exec test_env /bin/bash -c 'source /etc/apache2/envvars; echo "${APACHE_RUN_GROUP}"'`
        fi

        docker exec test_env chown ${APACHE_USER}:${APACHE_GROUP} /home/travis/build/vincent-noel/SigNetSim
        docker exec -u ${APACHE_USER} test_env /bin/bash /home/travis/build/vincent-noel/SigNetSim/scripts/test_apache.sh
        docker exec -u ${APACHE_USER} test_env /bin/bash /home/travis/build/vincent-noel/SigNetSim/scripts/run_tests.sh

    elif [ $2 = "after_script" ]; then
        coveralls

    else
        exit 0;

    fi

fi
