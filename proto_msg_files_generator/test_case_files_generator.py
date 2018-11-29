# -*- coding: utf-8 -*-

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

import os
import sys

sys.path.append('%s/..' % os.path.split(os.path.realpath(__file__))[0])  # 导入上级目录中的模块
# print(sys.path)

from base import file_util, name_style_util
import one_file_msg_mgr


def output_file_content(fp, msg, pkg_name, namespace):
    try:
        content = '''# -*- coding: utf-8 -*-

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

import os
import sys

sys.path.append('%s/../../../../py_tools' % os.path.split(os.path.realpath(__file__))[0])
# print(sys.path)

'''
        fp.write(content.encode('utf-8'))

        content = ['from base.%s_client import *' % namespace, os.linesep * 2,
                   'from test_action.%s.%s import *' % (
                       namespace, name_style_util.camel_to_underline(msg).lower()),
                   os.linesep * 3]
        fp.write(''.join(content).encode('utf-8'))

        action_name = name_style_util.camel_to_underline(msg).lower()

        content = ['def test_001():', os.linesep,
                   '    client = %sClient(conf.demo_server_addr, conf.demo_server_%s_port)' % (
                       namespace.capitalize(), namespace), os.linesep,
                   '    %s = %s(client)' % (action_name, msg), os.linesep,
                   '    ret = %s.%s()' % (action_name, action_name[:-4]), os.linesep,
                   '    assert ret == 0', os.linesep * 3]
        fp.write(''.join(content).encode('utf-8'))

        content = ['if __name__ == \'__main__\':', os.linesep,
                   '    test_001()', os.linesep]
        fp.write(''.join(content).encode('utf-8'))

        return 0
    except Exception as e:
        print('exception: %s' % e)
        return -1


def output_file(msg, output_dir, pkg_name, namespace_list):
    for namespace in namespace_list:
        if 'http' == namespace:
            continue

        file_path = os.path.join(output_dir, namespace,
                                 name_style_util.camel_to_underline(msg).lower().replace('_req', '') + '_test.py')
        file_util.del_file(file_path)
        file_util.make_dir(file_util.file_dir(file_path))

        try:
            fp = open(file_path, 'wb')

            output_file_content(fp, msg, pkg_name, namespace)
            fp.close()

            print('=== generate %s done ===' % file_path)
        except Exception as e:
            print('exception: %s' % e)
            return -1

    return 0


def generate_test_case_file(msg_list_group, output_dir, base_idx, gap, pkg_name, namespace_list):
    for msg_list in msg_list_group:
        if not msg_list or 0 == len(msg_list):
            continue

        for msg in msg_list:
            if msg.endswith('Req'):
                if output_file(msg, output_dir, pkg_name, namespace_list) != 0:
                    return -1
    return 0


def test_001():
    msg_list_group = []
    msg_mgr_ = one_file_msg_mgr.OneFileMsgMgr()

    if msg_mgr_.read_msg('./demo_msg.proto') != 0:
        return -1

    msg_list_group.append(msg_mgr_.msg_list)

    if generate_test_case_file(msg_list_group, './output/demo', None, None, 'com::moon::demo::proto',
                               ['tcp', 'http', 'udp']) != 0:
        return -1

    return 0


if __name__ == '__main__':
    test_001()
