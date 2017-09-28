# SigNetSim : The Signaling Network Simulator
[![Build Status](https://travis-ci.org/vincent-noel/SigNetSim.svg?branch=master)](https://travis-ci.org/vincent-noel/SigNetSim)
[![Coverage Status](https://coveralls.io/repos/github/vincent-noel/SigNetSim/badge.svg?branch=master)](https://coveralls.io/github/vincent-noel/SigNetSim?branch=master)
[![DOI](https://zenodo.org/badge/20701382.svg)](https://zenodo.org/badge/latestdoi/20701382)


A django web application for building, fitting, and analyzing mathematical models of molecular signaling networks.


## Installation

	sudo bash scripts/install.sh [folder]

The server will run on localhost/[folder], with a default Admin with admin:admin credentials.
Should work for ubuntu [precise|trusty|stretch] and debian [wheezy|jessie|stretch].


## Running within a docker

	bash scripts/run_docker.sh [local data folder]

The server will run on localhost:8080, with a default Admin with admin:admin credentials.
If you inform a local data folder, it will be use to locally store persistent data.


## License

Copyright (C) 2016 Vincent Noel (vincent.noel@butantan.gov.br)

SigNetSim is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SigNetSim is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with SigNetSim. If not, see <http://www.gnu.org/licenses/>.


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
