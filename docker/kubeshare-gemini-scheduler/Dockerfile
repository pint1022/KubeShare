# call from repo root

FROM centaurusinfra/pytorch-gpu-devel:latest AS build

WORKDIR /tmp/build

COPY . kubeshare
USER root

RUN apt-get update && apt-get install -y \
    make \
    build-essential &&\
    apt install -y git && \
    git clone https://github.com/pint1022/Gemini_UM.git && cd Gemini_UM && \
    make -C src

FROM python:3.9.1-buster

RUN pip3 install inotify
USER deployer

ENV NVIDIA_VISIBLE_DEVICES      all
ENV NVIDIA_DRIVER_CAPABILITIES  utility

COPY docker/lib/libdl.so.2          /lib
COPY docker/lib/libnvidia-ml.so.1   /lib

COPY --from=build /tmp/build/kubeshare/docker/kubeshare-gemini-scheduler/launcher-multigpus.sh /launcher-multigpus.sh
COPY --from=build /tmp/build/kubeshare/docker/kubeshare-gemini-scheduler/launcher.py /launcher.py
COPY --from=build /tmp/build/Gemini_UM/bin/gem-schd /gem-schd
COPY --from=build /tmp/build/Gemini_UM/bin/gem-pmgr /gem-pmgr

CMD ["/launcher-multigpus.sh", "/kubeshare/scheduler/config", "/kubeshare/scheduler/podmanagerport"]