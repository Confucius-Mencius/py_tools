#!/bin/bash

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

SCRIPT_PATH=$(cd `dirname $0`; pwd)

. ${SCRIPT_PATH}/common.sh

echo "build requests toolbelt..."

cd ${REQUESTS_TOOLBELT_SRC_DIR}
python setup.py build
sudo python setup.py install
