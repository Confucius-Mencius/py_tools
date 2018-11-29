# -*- coding: utf-8 -*-

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

import argparse
import os
import sys

sys.path.append('%s/../../py_tools' % os.path.split(os.path.realpath(__file__))[0])  # 导入上级目录中的模块
# print(sys.path)

from base import xls_util
import xls_head

import err_code_h_file_generator
import err_code_cpp_file_generator
import err_code_json_file_generator
import err_code_py_file_generator
import err_code_csharp_file_generator


def do(csv_file_path, output_dir):
    xls_head_ = xls_head.XlsHead()
    xls_loader = xls_util.XlsLoader(csv_file_path, xls_head_.nrows, xls_head_.ncols, xls_head_.col_types)

    if xls_loader.load() != 0:
        return -1

    generator_list = [err_code_h_file_generator.generate_err_code_h_file,
                      err_code_cpp_file_generator.generate_err_code_cpp_file,
                      err_code_json_file_generator.generate_err_code_json_file,
                      err_code_py_file_generator.generate_err_code_py_file,
                      err_code_csharp_file_generator.generate_err_code_csharp_file]

    for generator in generator_list:
        if generator(xls_head_, xls_loader.row_grid, xls_loader.col_grid, output_dir) != 0:
            return -1

    return 0


def test_001():
    csv_file_path = './demo_proj_err_code.csv'
    output_dir = './output/demo_server'

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
