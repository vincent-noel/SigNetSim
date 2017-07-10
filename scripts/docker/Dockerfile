FROM signetsim/signetsim:xenial

MAINTAINER Vincent Noel version: 0.1

RUN apt-get -qq update
RUN apt-get install -y git
RUN git clone -b develop https://github.com/vincent-noel/SigNetSim.git

EXPOSE 80
