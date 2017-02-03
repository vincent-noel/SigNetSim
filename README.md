# SigNetSim : The Signaling Network Simulator [![Build Status](https://travis-ci.org/vincent-noel/SigNetSim.svg?branch=master)](https://travis-ci.org/vincent-noel/SigNetSim)

A django web application for building, fitting, and analyzing mathematical models of molecular signaling networks.



##Non-Python Dependencies
You will need :

- Apache 2 and apache's mod wsgi
- MPI libraries to execute C code in parallel
- Sundials library to perform numerical integration,
- Git to download the non-linear optimization library and libSigNetSim,
- Pip to download python dependencies
- Npm, Node to download JS dependencies
- Virtualenv to encapsulate signetsim within a virtual environment
- GraphViz to generate PNGs from DOT files.



		apache2 libapache2-mod-wsgi \

		libopenmpi-dev openmpi-bin \

		libsundials-serial-dev libsundials-serial \

		git python-pip npm nodejs-legacy \

		virtualenv graphviz



##Python dependencies

	pip install -r requirements.txt



##Installation

	bash scripts/build_dep_[xenial|precise]
	bash scripts/make



##Run the development server

	bash scripts/run_env



##Run the apache server

	bash scripts/configure_apache_[xenial|precise]
	sudo bash scripts/install_apache_[xenial|precise]



##License

	Copyright (C) 2016 Vincent Noel (vincent.noel@butantan.gov.br)

	libSigNetSim is free software: you can redistribute it and/or modify
	it under the terms of the GNU Affero General Public License as published
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	libSigNetSim is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU Affero General Public License
	along with libSigNetSim. If not, see <http://www.gnu.org/licenses/>.
