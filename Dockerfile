FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y wget \
    build-essential \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libssl-dev \
    libreadline-dev \
    libffi-dev \
    curl \
    libbz2-dev \
    libsqlite3-dev && \
    apt-get clean

ENV PYTHON_VERSION=3.13.0

RUN wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz && \
    tar -xf Python-${PYTHON_VERSION}.tgz && \
    cd Python-${PYTHON_VERSION} && \
    ./configure --enable-optimizations && \
    make -j$(nproc) && \
    make altinstall && \
    cd .. && \
    rm -rf Python-${PYTHON_VERSION} Python-${PYTHON_VERSION}.tgz

RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.13

WORKDIR /app

COPY reqs.txt .

RUN python3.13 -m pip install setuptools
RUN python3.13 -m pip install --no-cache-dir -r reqs.txt
# RUN python3.13 -m pip install -r reqs.txt