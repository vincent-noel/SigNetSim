FROM signetsim/signetsim:xenial

MAINTAINER Vincent Noel version: 0.1

RUN git clone -b develop https://github.com/vincent-noel/SigNetSim.git
RUN /bin/bash /SigNetSim/scripts/xenial/install.sh
RUN /bin/bash /SigNetSim/scripts/apache/generate_apache.sh
RUN /bin/bash /SigNetSim/scripts/apache/install_apache.sh
EXPOSE 80
