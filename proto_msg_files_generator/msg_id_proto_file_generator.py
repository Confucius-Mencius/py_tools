# -*- coding: utf-8 -*-

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

import os
import sys

sys.path.append('%s/../../py_tools' % os.path.split(os.path.realpath(__file__))[0])  # 导入上级目录中的模块
# print(sys.path)

from base import file_util, name_style_util
import one_file_msg_mgr


def output_content(fp, msg_list_group, base_idx, gap, pkg_name):
    try:
        content = ['syntax = "proto3";', os.linesep,
                   'package %s;' % pkg_name, os.linesep,
                   os.linesep,
                   'enum MsgID {', os.linesep,
                   '    PLACE_HOLDER = 0;', os.linesep]
        fp.write(''.join(content).encode('utf-8'))

        group_base_idx = base_idx

        for msg_list in msg_list_group:
            if not msg_list or 0 == len(msg_list):
                continue

            if group_base_idx != base_idx:
                content = '    ////////////////////////////////////////////////////////////////////////////////%s' \
                          % os.linesep
                fp.write(content.encode('utf-8'))

            idx = group_base_idx
            for msg in msg_list:
                content = '    MSG_ID_%s = %d;%s' % (name_style_util.camel_to_underline(msg).upper(), idx, os.linesep)
                fp.write(content.encode('utf-8'))
                idx += 1

            group_base_idx += gap

        content = '}%s' % os.linesep
        fp.write(content.encode('utf-8'))

        return 0
    except Exception as e:
        print('exception: %s' % e)
        return -1


def generate_msg_id_proto_file(msg_proto_file, msg_list_group, output_dir, base_idx, gap, pkg_name, namespace_list):
    file_name = file_util.base_filename(msg_proto_file)
    file_path = os.path.join(output_dir, file_name[:len(file_name) - len('_msg')] + '_msg_id.proto')
    file_util.del_file(file_path)
    file_util.make_dir(output_dir)

    try:
        fp = open(file_path, "wb")
        output_content(fp, msg_list_group, base_idx, gap, pkg_name)
        fp.close()

        print('=== generate %s done ===' % file_path)
        return 0
    except Exception as e:
        print('exception: %s' % e)
        return -1


def test_001():
    msg_list_group = []
    one_file_msg_mgr_ = one_file_msg_mgr.OneFileMsgMgr()

    msg_proto_file = 'demo_msg.proto'
    if one_file_msg_mgr_.read_msg(msg_proto_file) != 0:
        return -1

    msg_list_group.append(one_file_msg_mgr_.msg_list)

    if generate_msg_id_proto_file(msg_proto_file, msg_list_group, './output/demo', 1000, 50,
                                  'com.moon.demo.proto', None) != 0:
        return -1

    return 0


if __name__ == '__main__':
    test_001()
