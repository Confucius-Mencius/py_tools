# -*- coding: utf-8 -*-

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

import os
import sys

sys.path.append('%s/../../py_tools' % os.path.split(os.path.realpath(__file__))[0])  # 导入上级目录中的模块
# print(sys.path)

from base import file_util, xls_util, name_style_util
import xls_head


def output_content(fp, xls_head_, xls_row_grid, xls_col_grid, indent):
    content = '''#include "xx_conf_mgr.h"

namespace xx
{
ConfMgr::ConfMgr() : rwlock_()
{
}

ConfMgr::~ConfMgr()
{
}

int ConfMgr::Load()
{
    AUTO_THREAD_WLOCK(rwlock_);

'''
    fp.write(content.encode('utf-8'))

    table = {'int': '0', 'int64': '0L', 'float': '0.0F', 'double': 0.0, 'bool': 'false', 'string': '""'}

    for xls_row in xls_row_grid.row_list:
        if xls_row.get_cell(xls_head_.conf['group']['col']).content:
            content = '%s%s_group_.clear();%s' % (indent,
                                                  xls_row.get_cell(xls_head_.conf['name']['col']).content,
                                                  os.linesep)
        else:
            content = '%s%s_ = %s;%s' % (indent,
                                         xls_row.get_cell(xls_head_.conf['name']['col']).content,
                                         table[xls_row.get_cell(xls_head_.conf['type']['col']).content],
                                         os.linesep)
        fp.write(content.encode('utf-8'))

    fp.write(os.linesep)

    for xls_row in xls_row_grid.row_list:
        if xls_row.get_cell(xls_head_.conf['group']['col']).content:
            func_name = 'Load%sGroup' % name_style_util.underline_to_camel(
                xls_row.get_cell(xls_head_.conf['name']['col']).content)
        else:
            func_name = 'Load%s' % name_style_util.underline_to_camel(
                xls_row.get_cell(xls_head_.conf['name']['col']).content)

        content = [indent, 'if (', func_name, '() != 0)', os.linesep,
                   indent, '{', os.linesep,
                   indent * 2, 'return -1;', os.linesep,
                   indent, '}', os.linesep * 2]
        fp.write(''.join(content).encode('utf-8'))

    content = '''    return 0;
}
}
'''
    fp.write(content.encode('utf-8'))


def generate_conf_mgr_cpp_file(xls_head_, xls_row_grid, xls_col_grid, output_dir):
    file_path = os.path.join(output_dir, 'xx_conf_mgr.cpp')
    file_util.del_file(file_path)
    file_util.make_dir(output_dir)

    try:
        fp = open(file_path, "wb")

        indent = ' ' * 4
        output_content(fp, xls_head_, xls_row_grid, xls_col_grid, indent)

        fp.close()

        file_util.replace_content(file_path, ["Tcp TCP", "Io IO", "Cpu CPU", "Udp UDP", "Http HTTP", "Tq TQ", "Ws WS", "Wss WSS", "WSs WSS"])
        print('=== generate %s done ===' % file_path)

        return 0
    except Exception as e:
        print('exception: %s' % e)
        return -1


def test_001():
    xls_head_ = xls_head.XlsHead()
    xls_loader = xls_util.XlsLoader('./app_frame_conf.csv', xls_head_.nrows, xls_head_.ncols, xls_head_.col_types)
    assert 0 == xls_loader.load()
    assert 0 == generate_conf_mgr_cpp_file(xls_head_, xls_loader.row_grid, xls_loader.col_grid, './output/app_frame')


if __name__ == "__main__":
    test_001()
