FROM debian:stretch

MAINTAINER Vincent Noel version: 0.1

RUN apt-get -qq update
ADD . /SigNetSim
RUN /bin/bash /SigNetSim/scripts/install.sh --global --python 2 --port 80

EXPOSE 80

CMD /etc/signetsim/apachectl -D FOREGROUND