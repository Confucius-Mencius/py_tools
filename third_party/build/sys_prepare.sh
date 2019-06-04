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

    yum -y install epel-release # 安装epel扩展源
    yum -y install python-pip # 安装pip
    yum clean all # 清除cache
    pip install --upgrade setuptools # 'extras_require' must be a dictionary whose values are strings or lists of strings containing valid project/version requirement specifiers.
else
    echo "not supported os"
    exit 1
fi
