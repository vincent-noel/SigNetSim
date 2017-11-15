FROM debian:stretch

MAINTAINER Vincent Noel version: 0.1

RUN apt-get -qq update
RUN git clone -b develop https://github.com/vincent-noel/SigNetSim.git
RUN /bin/bash /SigNetSim/scripts/install.sh

EXPOSE 80

CMD /usr/sbin/apache2ctl -D FOREGROUND