FROM debian:stretch

MAINTAINER Vincent Noel version: 0.1

RUN apt-get -qq update
RUN apt-get install -y curl
RUN curl -sL https://raw.githubusercontent.com/vincent-noel/libSigNetSim/develop/scripts/install_dep.sh | bash -
RUN git clone -b develop https://github.com/vincent-noel/SigNetSim.git
RUN /bin/bash /SigNetSim/scripts/install.sh

EXPOSE 80

CMD /usr/sbin/apache2ctl -D FOREGROUND