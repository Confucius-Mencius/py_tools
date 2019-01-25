#!/bin/bash

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

SCRIPT_PATH=$(cd `dirname $0`; pwd)

# ITEM_LIST=(demo_proj galileo)
ITEM_LIST=(demo_proj)

for i in ${ITEM_LIST[@]}; do
    CSV_FILE_PATH=${SCRIPT_PATH}/${i}_err_code.csv
    OUTPUT_DIR=${SCRIPT_PATH}/output/$i

    python ${SCRIPT_PATH}/main.py ${CSV_FILE_PATH} ${OUTPUT_DIR}
done
