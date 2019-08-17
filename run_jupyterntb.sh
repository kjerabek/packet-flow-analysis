#!/bin/bash
#$1 - volume path

docker build --rm -t packetanalyst-notebook ./packetanalyst-notebook

docker run --rm -p 10000:8888 -v $(pwd):/home/jovyan/work packetanalyst-notebook:latest
