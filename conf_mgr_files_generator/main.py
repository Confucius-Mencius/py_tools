# -*- coding: utf-8 -*-

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

import argparse
import os
import sys
import types

sys.path.append('%s/../../py_tools' % os.path.split(os.path.realpath(__file__))[0])  # 导入上级目录中的模块
# print(sys.path)

from base import xls_util
import xls_head

import conf_mgr_cpp_file_generator
import conf_mgr_h_file_generator
import conf_mgr_interface_file_generator
import conf_xpath_define_file_generator


def do(csv_file_path, output_dir):
    xls_head_ = xls_head.XlsHead()
    xls_loader = xls_util.XlsLoader(csv_file_path, xls_head_.nrows, xls_head_.ncols, xls_head_.col_types)

    if xls_loader.load() != 0:
        return -1

    # 修正各种类型的default value。注意这里只使用了row grid，只对row grid做了处理
    table1 = {'int': types.IntType, 'int64': types.LongType, 'float': types.FloatType,
              'double': types.FloatType, 'bool': types.BooleanType, 'string': types.StringType}

    for xls_row in xls_loader.row_grid.row_list:
        int_default_value = '0'
        int64_default_value = '0L'
        float_default_value = '0.0f'
        double_default_value = '0.0'
        bool_default_value = '0'
        string_default_value = '""'

        default = xls_row.get_cell(xls_head_.conf['default']['col']).content
        type_ = xls_row.get_cell(xls_head_.conf['type']['col']).content

        if len(default) > 0:
            if type_ == 'int':
                int_default_value = str(int(default))
            elif type_ == 'int64':
                int64_default_value = default
            elif type_ == 'float':
                float_default_value = default
            elif type_ == 'double':
                double_default_value = float(default)
            elif type_ == 'bool':
                bool_default_value = '1' if int(default) != 0 else '0'
            elif type_ == 'string':
                string_default_value = ('"%s"' % default) if len(default) > 0 else '""'

        table2 = {'int': int_default_value, 'int64': int64_default_value, 'float': float_default_value,
                  'double': double_default_value, 'bool': bool_default_value, 'string': string_default_value}

        xls_row.get_cell(xls_head_.conf['default']['col']).content = table2[type_]

    generator_list = [conf_mgr_cpp_file_generator.generate_conf_mgr_cpp_file,
                      conf_mgr_h_file_generator.generate_conf_mgr_h_file,
                      conf_mgr_interface_file_generator.generate_conf_mgr_interface_file,
                      conf_xpath_define_file_generator.generate_conf_xpath_define_file]

    for generator in generator_list:
        if generator(xls_head_, xls_loader.row_grid, xls_loader.col_grid, output_dir) != 0:
            return -1

    return 0


def test_001():
    csv_file_path = './app_frame_conf_entry.csv'
    output_dir = './output/app_frame'

    ret = do(csv_file_path, output_dir)
    assert 0 == ret


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('csv_file_path', help='csv file path')
    parser.add_argument('output_dir', help='output dir')

    args = parser.parse_args()
    print(args)

    return args


if __name__ == "__main__":
    args = parse_args()

    csv_file_path = os.path.realpath(args.csv_file_path)
    output_dir = os.path.realpath(args.output_dir)

    if not os.path.exists(csv_file_path):
        print('csv file %s not exist' % csv_file_path)
        sys.exit(-1)

    if do(csv_file_path, output_dir) != 0:
        sys.exit(-1)
