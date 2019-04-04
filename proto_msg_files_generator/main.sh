#!/bin/bash

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

SCRIPT_PATH=$(cd `dirname $0`; pwd)

PROTO_LIST=(cs ss) # 如果cs协议有多个proto文件，用逗号分隔，例如：cs1,cs2。
OUTPUT_DIR_LIST=(demo demo)
BASE_IDX_LIST=(1000 2000)
GAP_LIST=(50 50)
NAMESPACE_LIST=(com.moon.demo.cs com.moon.demo.ss)

for i in "${!PROTO_LIST[@]}"; do
    PROTOS=${PROTO_LIST[$i]}

    OUTPUT_DIR=${SCRIPT_PATH}/output/${OUTPUT_DIR_LIST[$i]}
    BASE_IDX=${BASE_IDX_LIST[$i]}
    GAP=${GAP_LIST[$i]}
    NAMESPACE=${NAMESPACE_LIST[$i]}
    MSG_PROTO_FILE_LIST=""

    # 如果有逗号的话，将逗号替换为空格
    if [[ ${PROTOS} =~ "," ]]; then
        PROTOS=${PROTOS//,/ }
        for ITEM in ${PROTOS}; do
            if [ "${MSG_PROTO_FILE_LIST}" = "" ]; then
                MSG_PROTO_FILE_LIST=${SCRIPT_PATH}/${ITEM}_msg.proto
            else
                MSG_PROTO_FILE_LIST=${MSG_PROTO_FILE_LIST}","${SCRIPT_PATH}/${ITEM}_msg.proto
            fi
        done
    else
        MSG_PROTO_FILE_LIST=${SCRIPT_PATH}/${PROTOS}_msg.proto
    fi

    echo ${MSG_PROTO_FILE_LIST}
    python ${SCRIPT_PATH}/main.py ${MSG_PROTO_FILE_LIST} ${OUTPUT_DIR} ${BASE_IDX} ${GAP} ${NAMESPACE} proto_tcp # 有多个namespace用逗号分隔
done
