# SigNetSim : The Signaling Network Simulator
[![Build Status](https://travis-ci.org/vincent-noel/SigNetSim.svg?branch=develop)](https://travis-ci.org/vincent-noel/SigNetSim)
[![Coverage Status](https://coveralls.io/repos/github/vincent-noel/SigNetSim/badge.svg?branch=develop)](https://coveralls.io/github/vincent-noel/SigNetSim?branch=develop)
[![DOI](https://zenodo.org/badge/20701382.svg)](https://zenodo.org/badge/latestdoi/20701382)


A django web application for building, fitting, and analyzing mathematical models of molecular signaling networks.


## Running within a docker using docker-compose 
    
First, you need to create the following docker-compose.yml file: 
    
    version: '3.3'

    services:
      signetsim:
        image: signetsim/signetsim:develop
        container_name: signetsim
        volumes:
          - signetsim_data:/SigNetSim/data
        ports:
          - "8080:80"
        restart: always
    
    volumes:
      signetsim_data:
      

This will pull the latest signetsim image from Docker Hub, and run SigNetSim on port 8080:

    docker-compose up -d signetsim
    

If you downloaded the repository and want to build the image locally:

    docker-compose up -d signetsim    
    
## Running within a docker

	docker pull signetsim/signetsim:develop
	docker run --name signetsim -d signetsim/signetsim:develop

The server will run on localhost:80.

If you want to locally store persistent data, use :

    docker run --name signetsim -v <data folder>:/SigNetSim/data -d signetsim/signetsim:develop

If you want to run it on a different port :

    docker run --name signetsim -p <port>:80 -d signetsim/signetsim:develop


## Installation script

	sudo bash scripts/install.sh [folder]

The server will run on localhost/[folder].
Should work for ubuntu [precise|trusty|stretch] and debian [wheezy|jessie|stretch].


## License

Copyright (C) 2016 Vincent Noel (vincent.noel@butantan.gov.br)

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.


## Financial support

This program was developed within the CeTICS project, at the Butantan Institute.

<p align="center">
	<a href="http://cetics.butantan.gov.br"><img src="docs/logos/cetics.png" align="middle" hspace="50"></a>
	<a href="http://www.butantan.gov.br"><img src="docs/logos/butantan.png" width="300" align="middle" hspace="50"></a>
</p>

The work was supported by grants #12/20186-9, #13/07467-1, and #13/24212-7 of the São Paulo Research Foundation (FAPESP) and fellowships from CNPq.


<p align="center">
	<a href="http://www.fapesp.br"><img src="docs/logos/FAPESP.jpg" width="300" align="middle" hspace="50"></a>
	<a href="http://cnpq.br"><img src="docs/logos/CNPq.jpg" width="175" align="middle" hspace="50"></a>
</p>
