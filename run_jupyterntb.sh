#!/bin/bash

docker run --rm -p 10000:8888 -v $(pwd):/home/jovyan/work jupyter/scipy-notebook
