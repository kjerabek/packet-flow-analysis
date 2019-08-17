FROM jupyter/scipy-notebook

RUN conda install --quiet --yes 'dpkt'

ENV PYTHONPATH "${PYTHONPATH}:/home/jovyan/work"
