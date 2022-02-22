# call from repo root

FROM centaurusinfra/pytorch-gpu-devel:latest AS build

WORKDIR /tmp/build

COPY . kubeshare
USER root
ARG GEMINI=Gemini
ENV DEBIAN_FRONTEND=noninteractive 

RUN apt-get update && apt-get install -y \
    make \
    build-essential \
    libzmq3-dev \
    libglib2.0-dev &&\
    apt install -y git && \
    git clone https://github.com/pint1022/$GEMINI.git && cd $GEMINI && \
    make DEBUG=1 -C src

FROM python:3.9.1-buster
ARG GEMINI=Gemini

RUN pip3 install inotify

ENV NVIDIA_VISIBLE_DEVICES      all
ENV NVIDIA_DRIVER_CAPABILITIES  utility

COPY docker/lib/libdl.so.2          /lib
COPY docker/lib/libnvidia-ml.so.1   /lib

COPY --from=build /tmp/build/kubeshare/docker/kubeshare-gemini-scheduler/launcher-multigpus.sh /launcher-multigpus.sh
COPY --from=build /tmp/build/kubeshare/docker/kubeshare-gemini-scheduler/launcher.py /launcher.py
COPY --from=build /tmp/build/$GEMINI/bin/gem-schd /gem-schd
# COPY --from=build /tmp/build/$GEMINI/bin/gem-pmgr /gem-pmgr

CMD ["/launcher-multigpus.sh", "/kubeshare/scheduler/config", "/kubeshare/scheduler/podmanagerport"]