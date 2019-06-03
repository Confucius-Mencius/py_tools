#!/bin/bash

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

SCRIPT_PATH=$(cd `dirname $0`; pwd)

# 删除当前目录中的子目录. -path '*/*'可以忽略.和..
cd ${SCRIPT_PATH}/../archives
find . -maxdepth 1 -type d -path '*/*' | xargs sudo rm -rf
cd ${SCRIPT_PATH}
