FROM amazonlinux:2
MAINTAINER tsubasaogawa

WORKDIR /work

RUN set -x && yum install -y gcc make zlib zlib-devel libpng libpng-devel
RUN ./setup.sh
