#!/bin/bash

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

# if [ "$(id -u)" != "0" ]; then
#     echo "the script must be run as root" 1>&2
#     exit -1
# fi

SCRIPT_PATH=$(cd `dirname $0`; pwd)

chmod +x ${SCRIPT_PATH}/*.sh

. ${SCRIPT_PATH}/common.sh

function BuildAll
{
    echo `date` >build_time.txt

    cd ${SCRIPT_PATH}
    ./build_xlrd.sh
    if [ $? -ne 0 ]; then
        echo "failed to build xlrd"
        exit 1
    fi

    cd ${SCRIPT_PATH}
    ./build_XlsxWriter.sh
    if [ $? -ne 0 ]; then
        echo "failed to build XlsxWriter"
        exit 1
    fi

    cd ${SCRIPT_PATH}
    ./build_nose.sh
    if [ $? -ne 0 ]; then
        echo "failed to build nose"
        exit 1
    fi

    cd ${SCRIPT_PATH}
    ./build_chardet.sh
    if [ $? -ne 0 ]; then
        echo "failed to build chardet"
        exit 1
    fi

    cd ${SCRIPT_PATH}
    ./build_ConcurrentLogHandler.sh
    if [ $? -ne 0 ]; then
        echo "failed to build ConcurrentLogHandler"
        exit 1
    fi

    cd ${SCRIPT_PATH}
    ./build_websocket_client.sh
    if [ $? -ne 0 ]; then
        echo "failed to build websocket client"
        exit 1
    fi

    cd ${SCRIPT_PATH}
    ./build_requests.sh
    if [ $? -ne 0 ]; then
        echo "failed to build requests"
        exit 1
    fi

    cd ${SCRIPT_PATH}
    ./build_requests_toolbelt.sh
    if [ $? -ne 0 ]; then
        echo "failed to build requests toolbelt"
        exit 1
    fi

    echo `date` >>build_time.txt
}

BuildAll 2>build_all.error.log
