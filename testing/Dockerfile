ARG BASE_CONTAINER=tensorflow/tensorflow:nightly-gpu-jupyter
FROM $BASE_CONTAINER

USER root

RUN /usr/bin/python3 -m pip install --upgrade pip
RUN pip install tensorflow-datasets
RUN pip install -U tensorboard_plugin_profile

WORKDIR /tmp/test

COPY mnist.py . 
COPY tf-cf-rn50-pack.py . 
