#!/bin/bash
sudo apt update
sudo apt upgrade -y
sudo apt purge -y wolfram-engine
sudo apt purge -y libreoffice*
sudo apt -y clean
sudo apt -y autoremove
sudo apt install \
    python-dev \
    python-pip \
    libfreetype6-dev \
    libjpeg-dev \
    build-essential \
    swig \
    portaudio19-dev \
    python3-all-dev \
    python3-pyaudio \
    flac \
    bison \
    libasound2-dev \
    i2c-tools \
    python3-smbus \
    libqtgui4 \
    libhdf5-dev \
    libhdf5-serial-dev \
    libatlas-base-dev \
    libjasper-dev \
    libqt4-test \
    util-linux \
    procps \
    hostapd \
    iproute2 \
    iw \
    haveged \
    dnsmasq \
    libpulse-dev \
    libilmbase23 \
    libopenexr23 \
    pocketsphinx
