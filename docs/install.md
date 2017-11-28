## Installation

	sudo bash scripts/install.sh [folder]

The server will run on localhost/[folder], with a default Admin with admin:admin credentials. Should work for ubuntu [precise|trusty|stretch] and debian [wheezy|jessie|stretch].


## Running within a docker

	docker pull signetsim/signetsim
	docker run --name signetsim -p 127.0.0.1:8080:80 -d signetsim/signetsim

The server will run on localhost:8080, with a default Admin with admin:admin credentials.

To locally store persistent data, run

	docker run --name signetsim -p 127.0.0.1:8080:80 \
		-v <data_folder>:/SigNetSim/data \
		-d signetsim/signetsim
