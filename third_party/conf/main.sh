#!/bin/bash

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

SCRIPT_PATH=$(cd `dirname $0`; pwd)

CSV_FILE_PATH=${SCRIPT_PATH}/third_party.csv
OUTPUT_DIR=${SCRIPT_PATH}/output

python ${SCRIPT_PATH}/main.py ${CSV_FILE_PATH} ${OUTPUT_DIR}

cp -rf ${OUTPUT_DIR}/common_define.sh ${SCRIPT_PATH}/../build/
