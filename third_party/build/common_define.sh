#!/bin/bash

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

XLRD_BASENAME=xlrd-1.1.0
XLSXWRITER_BASENAME=XlsxWriter-1.1.2
NOSE_BASENAME=nose-1.3.7
CHARDET_BASENAME=chardet-3.0.4
CONCURRENT_LOG_HANDLER_BASENAME=ConcurrentLogHandler-0.9.1

XLRD_SRC_DIR=${ARCHIVES_DIR}/${XLRD_BASENAME}
XLSXWRITER_SRC_DIR=${ARCHIVES_DIR}/${XLSXWRITER_BASENAME}
NOSE_SRC_DIR=${ARCHIVES_DIR}/${NOSE_BASENAME}
CHARDET_SRC_DIR=${ARCHIVES_DIR}/${CHARDET_BASENAME}
CONCURRENT_LOG_HANDLER_SRC_DIR=${ARCHIVES_DIR}/${CONCURRENT_LOG_HANDLER_BASENAME}

function UnzipAll
{
    tar -C ${ARCHIVES_DIR} -xvf ${ARCHIVES_DIR}/${XLRD_BASENAME}.tar.gz
    if [ $? -ne 0 ]; then
        echo "failed to unzip " ${ARCHIVES_DIR}/${XLRD_BASENAME}.tar.gz
        exit 1
    fi

    tar -C ${ARCHIVES_DIR} -xvf ${ARCHIVES_DIR}/${XLSXWRITER_BASENAME}.tar.gz
    if [ $? -ne 0 ]; then
        echo "failed to unzip " ${ARCHIVES_DIR}/${XLSXWRITER_BASENAME}.tar.gz
        exit 1
    fi

    tar -C ${ARCHIVES_DIR} -xvf ${ARCHIVES_DIR}/${NOSE_BASENAME}.tar.gz
    if [ $? -ne 0 ]; then
        echo "failed to unzip " ${ARCHIVES_DIR}/${NOSE_BASENAME}.tar.gz
        exit 1
    fi

    tar -C ${ARCHIVES_DIR} -xvf ${ARCHIVES_DIR}/${CHARDET_BASENAME}.tar.gz
    if [ $? -ne 0 ]; then
        echo "failed to unzip " ${ARCHIVES_DIR}/${CHARDET_BASENAME}.tar.gz
        exit 1
    fi

    tar -C ${ARCHIVES_DIR} -xvf ${ARCHIVES_DIR}/${CONCURRENT_LOG_HANDLER_BASENAME}.tar.gz
    if [ $? -ne 0 ]; then
        echo "failed to unzip " ${ARCHIVES_DIR}/${CONCURRENT_LOG_HANDLER_BASENAME}.tar.gz
        exit 1
    fi
}
