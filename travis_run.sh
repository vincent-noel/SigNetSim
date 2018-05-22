#!/bin/bash

if [ $1 = "docker" ]; then
    if [ $2 = "before_install" ]; then
        pip install -U docker-compose || exit 1;
        docker login -u signetsim -p $4

    elif [ $2 = "install" ]; then
        if [ $3 = "2" ]; then
            docker-compose build signetsim || exit 1;
        else
            docker-compose build signetsim-python3 || exit 1;
        fi

    elif [ $2 = "script" ]; then
        if [ $3 = "2" ]; then
            docker run --name signetsim -p 80:80 -d signetsim/signetsim:develop || exit 1;
        else
            docker run --name signetsim -p 80:80 -d signetsim/signetsim:develop-python3 || exit 1;
        fi

        APACHE_RETURN=`wget -q -O - localhost:80 | grep \<title\> | cut -d">" -f2 | cut -d" " -f1`
        if [ -n "${APACHE_RETURN}" ] && [ "${APACHE_RETURN}" == "Install" ];
        then
            exit 0;
        else
            exit 1;
        fi


    elif [ $2 = "after_script" ]; then
        if [ $3 = "2" ]; then
            docker push signetsim/signetsim:develop || exit 1;
        else
            docker push signetsim/signetsim:develop-python3 || exit 1;
        fi

    fi

else

    if [ $2 = "before_install" ]; then
        if [ $3 = "2" ]; then
            docker pull signetsim/travis_testenv:$1 || exit 1;
        else
            docker pull signetsim/travis_testenv:$1-python3 || exit 1;
        fi

    elif [ $2 = "install" ]; then
        if [ $3 = "2" ]; then
            docker run -di --name test_env -v $(pwd):/home/travis/build/vincent-noel/SigNetSim signetsim/travis_testenv:$1 bash
            if [ "$1" != fedora* ] ; then
                docker exec test_env chown -R www-data:www-data /home/travis/build/vincent-noel/SigNetSim
            fi
            docker exec test_env /bin/bash /home/travis/build/vincent-noel/SigNetSim/scripts/install.sh
        else
            docker run -di --name test_env -v $(pwd):/home/travis/build/vincent-noel/SigNetSim signetsim/travis_testenv:$1-python3 bash
            if [ "$1" != fedora* ] ; then
                docker exec test_env chown -R www-data:www-data /home/travis/build/vincent-noel/SigNetSim
            fi
            docker exec test_env /bin/bash /home/travis/build/vincent-noel/SigNetSim/scripts/install-python3.sh
        fi

    elif [ $2 = "script" ]; then
        docker exec -u www-data test_env /bin/bash /home/travis/build/vincent-noel/SigNetSim/scripts/test_apache.sh
        docker exec -u www-data test_env /bin/bash /home/travis/build/vincent-noel/SigNetSim/scripts/run_tests.sh

    elif [ $2 = "after_script" ]; then
        coveralls

    else
        exit 0;

    fi

fi
