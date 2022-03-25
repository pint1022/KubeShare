# call from repo root

FROM ubuntu:18.04 AS build

ENV GOLANG_VERSION 1.17.6
ENV GOPATH /go
ENV PATH $GOPATH/bin:/usr/local/go/bin:$PATH

WORKDIR /go/src/kubeshare

COPY . .

RUN apt update && \
    apt install -y g++ wget make && \
    wget -nv -O - https://storage.googleapis.com/golang/go${GOLANG_VERSION}.linux-amd64.tar.gz | tar -C /usr/local -xz && \
    make alnair-exporter

FROM alpine:3.9

COPY --from=build /go/src/kubeshare/bin/pf-exporter /usr/bin/pf-exporter

CMD ["pf-exporter", "-alsologtostderr", "-v=4"]
