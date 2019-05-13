# -*- coding: utf-8 -*-

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

import os
import sys

sys.path.append('%s/../..' % os.path.split(os.path.realpath(__file__))[0])  # 导入上级目录中的模块
# print(sys.path)

from base import file_util, xls_util
import xls_head


def output_basenames(fp, xls_head_, xls_row_grid, xls_col_grid, indent):
    for xls_row in xls_row_grid.row_list:
        if not xls_row.get_cell(xls_head_.conf['use']['col']).content:
            continue

        content = [indent, xls_row.get_cell(xls_head_.conf['key']['col']).content, '_BASENAME=',
                   xls_row.get_cell(xls_head_.conf['basename']['col']).content, os.linesep]
        fp.write(''.join(content).encode('utf-8'))

    fp.write(os.linesep)


def output_src_dirs(fp, xls_head_, xls_row_grid, xls_col_grid, indent):
    for xls_row in xls_row_grid.row_list:
        if not xls_row.get_cell(xls_head_.conf['use']['col']).content:
            continue

        content = [indent, xls_row.get_cell(xls_head_.conf['key']['col']).content, '_SRC_DIR=${ARCHIVES_DIR}/${',
                   xls_row.get_cell(xls_head_.conf['key']['col']).content, '_BASENAME}', os.linesep]
        fp.write(''.join(content).encode('utf-8'))

    fp.write(os.linesep)


def output_unzip_function(fp, xls_head_, xls_row_grid, xls_col_grid, indent):
    content = '%sfunction UnzipAll%s%s{' % (indent, os.linesep, indent)
    fp.write(content.encode('utf-8'))

    for xls_row in xls_row_grid.row_list:
        if not xls_row.get_cell(xls_head_.conf['use']['col']).content:
            continue

        ext = xls_row.get_cell(xls_head_.conf['ext']['col']).content
        file_path = ''.join(['${ARCHIVES_DIR}/${', xls_row.get_cell(xls_head_.conf['key']['col']).content,
                             '_BASENAME}.', ext])

        if 'zip' == ext:
            content = '%s%s    unzip -o %s -d ${ARCHIVES_DIR}%s' % (os.linesep, indent * 2, file_path, os.linesep)
        else:
            content = '%s%s    tar -C ${ARCHIVES_DIR} -xvf %s%s' % (os.linesep, indent * 2, file_path, os.linesep)

        fp.write(content.encode('utf-8'))

        content = [indent * 2, '    if [ $? -ne 0 ]; then', os.linesep,
                   indent * 2, '        echo "failed to unzip" ', file_path, os.linesep,
                   indent * 2, '        exit 1', os.linesep,
                   indent * 2, '    fi', os.linesep]
        fp.write(''.join(content).encode('utf-8'))

    content = '}%s' % os.linesep
    fp.write(content.encode('utf-8'))


def generate_common_define_sh_file(xls_head_, xls_row_grid, xls_col_grid, output_dir):
    file_path = os.path.join(output_dir, 'common_define.sh')
    file_util.del_file(file_path)
    file_util.make_dir(output_dir)

    try:
        fp = open(file_path, "wb")

        content = '''#!/bin/bash

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

'''
        fp.write(content.encode('utf-8'))

        output_basenames(fp, xls_head_, xls_row_grid, xls_col_grid, '')
        output_src_dirs(fp, xls_head_, xls_row_grid, xls_col_grid, '')
        output_unzip_function(fp, xls_head_, xls_row_grid, xls_col_grid, '')

        fp.close()
        print('=== generate %s done ===' % file_path)

        return 0
    except Exception as e:
        print('exception: %s' % e)
        return -1


def test_001():
    xls_head_ = xls_head.XlsHead()
    xls_loader = xls_util.XlsLoader('./third_party.csv', xls_head_.nrows, xls_head_.ncols, xls_head_.col_types)
    assert 0 == xls_loader.load()
    assert 0 == generate_common_define_sh_file(xls_head_, xls_loader.row_grid, xls_loader.col_grid, './output')


if __name__ == "__main__":
    test_001()
