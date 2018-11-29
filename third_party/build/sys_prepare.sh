#!/bin/bash

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

if [ "$(id -u)" != "0" ]; then
    echo "the script should be executed as root" 1>&2
    exit -1
fi

###############################################################################
if [ $(command -v apt-get) ]; then
    wget https://bootstrap.pypa.io/ez_setup.py -O - | python
elif [ $(command -v yum) ]; then
    yum install python-setuptools -y
else
    echo "not supported os"
    exit 1
fi
