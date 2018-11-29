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
    content = '''#ifndef XX_CONF_MGR_INTERFACE_H_
#define XX_CONF_MGR_INTERFACE_H_

namespace xx
{
class XXConfMgrInterface
{
public:
    virtual ~XXConfMgrInterface()
    {
    }

'''
    fp.write(content.encode('utf-8'))

    for xls_row in xls_row_grid.row_list:
        if not xls_row.get_cell(xls_head_.conf['virtual']['col']).content:
            continue

        if xls_row.get_cell(xls_head_.conf['type']['col']).content == 'int':
            if not xls_row.get_cell(xls_head_.conf['group']['col']).content:
                return_type = 'int'
                func_name = 'Get%s' % (
                    name_style_util.underline_to_camel(xls_row.get_cell(xls_head_.conf['name']['col']).content))
            else:
                return_type = 'IntGroup'
                func_name = 'Get%sGroup' % (
                    name_style_util.underline_to_camel(xls_row.get_cell(xls_head_.conf['name']['col']).content))
        elif xls_row.get_cell(xls_head_.conf['type']['col']).content == 'int64':
            if not xls_row.get_cell(xls_head_.conf['group']['col']).content:
                return_type = 'int64_t'
                func_name = 'Get%s' % (
                    name_style_util.underline_to_camel(xls_row.get_cell(xls_head_.conf['name']['col']).content))
            else:
                return_type = 'Int64Group'
                func_name = 'Get%sGroup' % (
                    name_style_util.underline_to_camel(xls_row.get_cell(xls_head_.conf['name']['col']).content))
        elif xls_row.get_cell(xls_head_.conf['type']['col']).content == 'float':
            if not xls_row.get_cell(xls_head_.conf['group']['col']).content:
                return_type = 'float'
                func_name = 'Get%s' % (
                    name_style_util.underline_to_camel(xls_row.get_cell(xls_head_.conf['name']['col']).content))
            else:
                return_type = 'FloatGroup'
                func_name = 'Get%sGroup' % (
                    name_style_util.underline_to_camel(xls_row.get_cell(xls_head_.conf['name']['col']).content))
        elif xls_row.get_cell(xls_head_.conf['type']['col']).content == 'double':
            if not xls_row.get_cell(xls_head_.conf['group']['col']).content:
                return_type = 'double'
                func_name = 'Get%s' % (
                    name_style_util.underline_to_camel(xls_row.get_cell(xls_head_.conf['name']['col']).content))
            else:
                return_type = 'DoubleGroup'
                func_name = 'Get%sGroup' % (
                    name_style_util.underline_to_camel(xls_row.get_cell(xls_head_.conf['name']['col']).content))
        elif xls_row.get_cell(xls_head_.conf['type']['col']).content == 'bool':
            if not xls_row.get_cell(xls_head_.conf['group']['col']).content:
                return_type = 'bool'
                func_name = '%s' % (
                    name_style_util.underline_to_camel(xls_row.get_cell(xls_head_.conf['name']['col']).content))
            else:
                return_type = 'BoolGroup'
                func_name = '%sGroup' % (
                    name_style_util.underline_to_camel(xls_row.get_cell(xls_head_.conf['name']['col']).content))
        elif xls_row.get_cell(xls_head_.conf['type']['col']).content == 'string':
            if not xls_row.get_cell(xls_head_.conf['group']['col']).content:
                return_type = 'std::string'
                func_name = 'Get%s' % (
                    name_style_util.underline_to_camel(xls_row.get_cell(xls_head_.conf['name']['col']).content))
            else:
                return_type = 'StrGroup'
                func_name = 'Get%sGroup' % (
                    name_style_util.underline_to_camel(xls_row.get_cell(xls_head_.conf['name']['col']).content))

        content = '%svirtual %s %s() = 0;%s' % (indent, return_type, func_name, os.linesep)
        fp.write(content.encode('utf-8'))

    content = '''};
}

#endif // XX_CONF_MGR_INTERFACE_H_
'''
    fp.write(content.encode('utf-8'))


def generate_conf_mgr_interface_file(xls_head_, xls_row_grid, xls_col_grid, output_dir):
    file_path = os.path.join(output_dir, 'xx_conf_mgr_interface.h')
    file_util.del_file(file_path)
    file_util.make_dir(output_dir)

    try:
        fp = open(file_path, "wb")

        indent = ' ' * 4
        output_content(fp, xls_head_, xls_row_grid, xls_col_grid, indent)

        fp.close()

        # file_util.replace_content(file_path, ["Tcp TCP", "Io IO", "Cpu CPU", "Udp UDP"])
        print('=== generate %s done ===' % file_path)

        return 0
    except Exception as e:
        print('exception: %s' % e)
        return -1


def test_001():
    xls_head_ = xls_head.XlsHead()
    xls_loader = xls_util.XlsLoader('./app_frame_conf.csv', xls_head_.nrows, xls_head_.ncols, xls_head_.col_types)
    assert 0 == xls_loader.load()
    assert 0 == generate_conf_mgr_interface_file(xls_head_, xls_loader.row_grid, xls_loader.col_grid,
                                                 './output/app_frame')


if __name__ == "__main__":
    test_001()
