#!/bin/bash

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

SCRIPT_PATH=$(cd `dirname $0`; pwd)
GENERATOR=${SCRIPT_PATH}/gmock_gen.py

if [ $# -lt 2 ]; then
    echo "Usage: ${SCRIPT_PATH}/main.sh <interface file(.h)> <interface[,interface[,interface]...]>"
    exit 0
fi

# 参数2有多个时，即处理一个文件中的多个接口时，要用引号扩起来，以空格分隔
python ${GENERATOR} $1 $2
