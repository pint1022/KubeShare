# call from repo root

FROM centaurusinfra/pytorch-gpu-devel:latest AS build

WORKDIR /tmp/build
USER root
# COPY . kubeshare


ENV DEBIAN_FRONTEND=noninteractive 
ENV CU_HOOK_DEBUG=1
ARG GEMINI=Gemini_UM

RUN apt update && \
    apt-get install -y libzmq3-dev &&\
    apt-get install -y libglib2.0-dev &&\
    apt install -y git && \
    git clone https://github.com/pint1022/$GEMINI.git && cd $GEMINI && \
    make DEBUG=1 -C src

# FROM busybox:1.31.1-glibc
FROM alpine:3.9
ARG GEMINI=Gemini_UM

RUN apk update && \
    apk add py3-zmq \
        libc6-compat
    
COPY --from=build /tmp/build/$GEMINI/lib/libgemhook.so.1 /libgemhook.so.1

CMD ["cp", "/libgemhook.so.1", "/kubeshare/library/libgemhook.so.1"]

