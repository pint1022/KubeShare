# call from repo root

FROM centaurusinfra/pytorch-gpu-devel:latest AS build

WORKDIR /tmp/build

COPY . kubeshare
USER root
ARG GEMINI=Gemini_UM
ENV DEBIAN_FRONTEND=noninteractive 
# RUN sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A4B469963BF863CC

RUN rm /etc/apt/sources.list.d/cuda.list
RUN apt-get update && apt-get install -y \
    make \
    build-essential \
    libzmq3-dev \
    libglib2.0-dev &&\
    apt install -y git && \
    git clone -b dev https://github.com/pint1022/$GEMINI.git && cd $GEMINI && \
    make -C src

FROM python:3.9.1-buster
ARG GEMINI=kubeshare

RUN pip3 install inotify

ENV NVIDIA_VISIBLE_DEVICES      all
ENV NVIDIA_DRIVER_CAPABILITIES  utility
RUN apt-get update && apt-get install -y libzmq3-dev

COPY docker/lib/libdl.so.2          /lib
COPY docker/lib/libnvidia-ml.so.1   /lib
COPY --from=build /tmp/build/kubeshare/docker/kubeshare-gemini-scheduler/launcher-multigpus.sh /launcher-multigpus.sh
COPY --from=build /tmp/build/kubeshare/docker/kubeshare-gemini-scheduler/launcher.py /launcher.py
COPY --from=build /tmp/build/kubeshare/docker/kubeshare-gemini-scheduler/launcher_alnr.py /launcher_alnr.py
COPY --from=build /tmp/build/$GEMINI/bin/gem-schd /gem-schd
# COPY gem-pmgr /gem-pmgr
COPY --from=build /tmp/build/$GEMINI/bin/gem-pmgr /gem-pmgr
COPY --from=build /tmp/build/$GEMINI/bin/alnr /alnr

CMD ["/launcher-multigpus.sh", "/kubeshare/scheduler/config", "/kubeshare/scheduler/podmanagerport"]