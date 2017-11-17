#!/bin/bash

if [ $1 = "docker" ]; then
    if [ $2 = "before_install" ]; then
        pip install -U docker-compose || exit 1;
        docker login -u signetsim -p $3

    elif [ $2 = "install" ]; then
        docker-compose build || exit 1;

    elif [ $2 = "test" ]; then
        docker push signetsim/signetsim:test_submodules || exit 1;

    fi

else
    if [ $2 = "before_install" ]; then
        docker pull signetsim/travis_testenv:$1 || exit 1;

    elif [ $2 = "install" ]; then
        docker run -di --name test_env -v $(pwd):/home/travis/build/vincent-noel/SigNetSim signetsim/travis_testenv:$1 bash
        docker exec test_env chown -R www-data:www-data /home/travis/build/vincent-noel/SigNetSim
        docker exec test_env /bin/bash /home/travis/build/vincent-noel/SigNetSim/scripts/install.sh

    elif [ $2 = "test" ]; then
        docker exec -u www-data test_env /bin/bash /home/travis/build/vincent-noel/SigNetSim/scripts/test_apache.sh
        docker exec -u www-data test_env /bin/bash /home/travis/build/vincent-noel/SigNetSim/scripts/run_tests.sh

    else
        exit 0;

    fi

fi
