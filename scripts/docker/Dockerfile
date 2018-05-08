FROM debian:stretch

MAINTAINER Vincent Noel version: 0.1

RUN apt-get -qq update
ADD . /SigNetSim
RUN /bin/bash /SigNetSim/scripts/install.sh

EXPOSE 80

CMD /usr/bin/bash