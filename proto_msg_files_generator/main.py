# -*- coding: utf-8 -*-

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

import argparse
import os
import sys

sys.path.append('%s/../../py_tools' % os.path.split(os.path.realpath(__file__))[0])  # 导入上级目录中的模块
# print(sys.path)

import msg_id_proto_file_generator
import cpp_msg_handler_files_generator
import test_action_files_generator
import test_case_files_generator
import csharp_msg_handler_file_generator

import one_file_msg_mgr


def do(msg_proto_file_list, output_dir, base_idx, gap, pkg_name, namespace_list):
    msg_list_group = []

    for msg_proto_file in msg_proto_file_list:
        one_file_msg_mgr_ = one_file_msg_mgr.OneFileMsgMgr()

        if one_file_msg_mgr_.read_msg(msg_proto_file) != 0:
            return -1

        msg_list_group.append(one_file_msg_mgr_.msg_list)

    generator_list = [msg_id_proto_file_generator.generate_msg_id_proto_file,
                      cpp_msg_handler_files_generator.generate_cpp_msg_handler_file,
                      test_action_files_generator.generate_test_action_file,
                      test_case_files_generator.generate_test_case_file,
                      csharp_msg_handler_file_generator.generate_csharp_msg_handler_file]

    for generator in generator_list:
        if generator(msg_list_group, output_dir, base_idx, gap, pkg_name, namespace_list) != 0:
            return -1

    return 0


def test_001():
    if do(['./demo_msg.proto'], './output/demo', 1000, 50, 'com.moon.demo.proto', ['tcp', 'http', 'udp']) != 0:
        return -1

    return 0


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('msg_proto_file_list', help='msg proto file list')
    parser.add_argument('output_dir', help='output dir')
    parser.add_argument('base_idx', help='base idx')
    parser.add_argument('gap', help='gap')
    parser.add_argument('pkg_name', help='pkg name')
    parser.add_argument('namespace_list', help='namespace list')

    args = parser.parse_args()
    print(args)

    return args


if __name__ == "__main__":
    args = parse_args()

    msg_proto_file_list = args.msg_proto_file_list.split(',')
    output_dir = os.path.realpath(args.output_dir)
    base_idx = int(args.base_idx)
    gap = int(args.gap)
    pkg_name = args.pkg_name
    namespace_list = args.namespace_list.split(',')

    for f in msg_proto_file_list:
        if not os.path.exists(f):
            print('msg proto file %s not exist' % f)
            sys.exit(-1)

    if do(msg_proto_file_list, output_dir, base_idx, gap, pkg_name, namespace_list) != 0:
        sys.exit(-1)
