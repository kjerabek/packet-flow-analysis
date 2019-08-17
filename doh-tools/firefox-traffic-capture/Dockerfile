FROM selenium/standalone-firefox
USER root

RUN apt-get update && apt-get install -y \
python3 \
python3-pip \
zip \
tcpdump \
wget \
sudo \
xvfb \
iputils-ping

RUN pip3 install selenium browsermob-proxy xvfbwrapper

ARG SOURCES=./sources
ADD $SOURCES /sources
WORKDIR /sources

RUN wget https://github.com/lightbody/browsermob-proxy/releases/download/browsermob-proxy-2.1.4/browsermob-proxy-2.1.4-bin.zip
RUN unzip *.zip
RUN rm *.zip
RUN chown -R seluser:seluser /sources

RUN mkdir /capture
RUN chown -R seluser:seluser /capture

ENV REQUEST_DOMAIN_NAME=example.com
ENV OUTPUT_FILE_NAME=example


CMD NAME=/capture/$OUTPUT_FILE_NAME /sources/run.sh
