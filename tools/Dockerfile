FROM amazonlinux:2
MAINTAINER tsubasaogawa

WORKDIR /work/build

COPY ./compile.sh .

RUN set -x && yum install -y gcc make zlib zlib-devel libpng libpng-devel git sudo automake autoconf libtool

RUN ./compile.sh
