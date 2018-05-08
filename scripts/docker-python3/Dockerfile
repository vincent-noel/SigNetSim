FROM debian:stretch

MAINTAINER Vincent Noel version: 0.1

RUN apt-get -qq update
ADD . /SigNetSim
RUN /bin/bash /SigNetSim/scripts/install-python3.sh

EXPOSE 80

CMD /etc/mod_wsgi-express-80/apachectl -D FOREGROUND