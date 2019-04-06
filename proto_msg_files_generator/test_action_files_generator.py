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

from util.proto_msg_codec import *
import conf
from data.err_code import *

'''
        fp.write(content.encode('utf-8'))

        content = ['from %s import cs_msg_id_pb2' % pkg_name.replace('::', '.'), os.linesep,
                   'from %s import cs_msg_pb2' % pkg_name.replace('::', '.'), os.linesep * 3]
        fp.write(''.join(content).encode('utf-8'))

        content = ['class %s(object):' % msg, os.linesep,
                   '    def __init__(self, client):', os.linesep,
                   '        self.client = client', os.linesep * 2]
        fp.write(''.join(content).encode('utf-8'))

        if msg.endswith('Req'):
            content = ['    # TODO', os.linesep,
                       '    def set_xx(self, xx):', os.linesep,
                       '        self.xx = xx', os.linesep * 2]
            fp.write(''.join(content).encode('utf-8'))

            req_instance = name_style_util.camel_to_underline(msg).lower()
            content = ['    def __make_%s(self):' % req_instance, os.linesep,
                       '        %s = cs_msg_pb2.%s()' % (req_instance, msg), os.linesep,
                       '        # TODO', os.linesep * 2,
                       '        LOG_DEBUG(\'%%s%%s\' %% (os.linesep, %s))' % req_instance, os.linesep,
                       '        return %s' % req_instance, os.linesep * 2]
            fp.write(''.join(content).encode('utf-8'))

            rsp_instance = name_style_util.camel_to_underline(msg).lower().replace('req', 'rsp')
            content = ['    def __make_%s(self, rsp_msg_body):' % rsp_instance, os.linesep,
                       '        %s = cs_msg_pb2.%s()' % (rsp_instance, msg.replace('Req', 'Rsp')), os.linesep,
                       '        %s.ParseFromString(rsp_msg_body)' % rsp_instance, os.linesep * 2,
                       '        LOG_DEBUG(\'%%s%%s\' %% (os.linesep, %s))' % rsp_instance, os.linesep,
                       '        return %s' % rsp_instance, os.linesep * 2]
            fp.write(''.join(content).encode('utf-8'))

            content = ['    def %s(self):' % req_instance.replace('_req', ''), os.linesep,
                       '        LOG_DEBUG(\'----- %s -----\')' % req_instance, os.linesep * 2,
                       '        %s_msg_head = MsgHead()' % req_instance, os.linesep,
                       '        %s_msg_head.msg_id = cs_msg_id_pb2.MSG_ID_%s' % (
                           req_instance, name_style_util.camel_to_underline(msg).upper()), os.linesep * 2,
                       '        %s = self.__make_%s()' % (req_instance, req_instance), os.linesep * 2]
            fp.write(''.join(content).encode('utf-8'))

            if 'proto_tcp' == namespace:
                content = [
                    '        ret = self.client.send(%s_msg_head, %s.SerializeToString(), %s.ByteSize(), conf.proto_tcp_do_checksum)' % (
                        req_instance, req_instance, req_instance), os.linesep]
            fp.write(''.join(content).encode('utf-8'))

            content = ['        if ret != 0:', os.linesep,
                       '            LOG_ERROR(\'failed to send to server %s\' % self.client.server())', os.linesep,
                       '            return -1', os.linesep * 2]
            fp.write(''.join(content).encode('utf-8'))

            if 'proto_tcp' == namespace:
                content = ['        %s_msg_head = MsgHead()' % rsp_instance, os.linesep * 2,
                           '        ret, %s_msg_head, %s_msg_body = self.client.recv(conf.proto_tcp_do_checksum)' % (
                               rsp_instance, rsp_instance), os.linesep]
            fp.write(''.join(content).encode('utf-8'))

            rsp_msg_head = '%s_msg_head' % rsp_instance
            content = ['        if ret != 0:', os.linesep,
                       '            LOG_ERROR(\'ret: %d\' % ret)', os.linesep,
                       '            return -1', os.linesep * 2,
                       '        if %s.msg_id != cs_msg_id_pb2.MSG_ID_%s:' % (
                           rsp_msg_head, name_style_util.camel_to_underline(msg).upper().replace('REQ', 'RSP')),
                       os.linesep,
                       '            LOG_ERROR(\'error rsp msg id: %d\' % ' + rsp_msg_head + '.msg_id)', os.linesep,
                       '            return -1', os.linesep * 2,
                       '        %s = self.__make_%s(%s_msg_body)' % (rsp_instance, rsp_instance, rsp_instance),
                       os.linesep * 2,
                       '        err_code = %s.err_ctx.err_code' % rsp_instance, os.linesep,
                       '        if err_code != 0:', os.linesep,
                       '            LOG_ERROR(\'failed err code: %d\' % err_code)', os.linesep,
                       '            return err_code', os.linesep * 2,
                       '        return 0', os.linesep]
            fp.write(''.join(content).encode('utf-8'))
        else:
            nfy_instance = name_style_util.camel_to_underline(msg).lower()
            content = ['    def __make_%s(self, nfy_msg_body):' % nfy_instance, os.linesep,
                       '        %s = cs_msg_pb2.%s()' % (nfy_instance, msg), os.linesep,
                       '        %s.ParseFromString(nfy_msg_body)' % nfy_instance, os.linesep * 2,
                       '        LOG_DEBUG(\'%%s%%s\' %% (os.linesep, %s))' % nfy_instance, os.linesep,
                       '        return %s' % nfy_instance, os.linesep * 2]
            fp.write(''.join(content).encode('utf-8'))

            content = ['    def %s(self):' % nfy_instance.replace('_nfy', ''), os.linesep,
                       '        LOG_DEBUG(\'----- %s -----\')' % nfy_instance, os.linesep * 2]
            fp.write(''.join(content).encode('utf-8'))

            nfy_msg_head = '%s_msg_head' % nfy_instance

            if 'proto_tcp' == namespace:
                content = ['        %s = MsgHead()' % nfy_msg_head, os.linesep * 2,
                           '        ret, %s, %s_msg_body = self.client.recv(conf.proto_tcp_do_checksum)' % (
                               nfy_msg_head, nfy_instance), os.linesep]
            fp.write(''.join(content).encode('utf-8'))

            content = ['        if ret != 0:', os.linesep,
                       '            LOG_ERROR(\'ret: %d\' % ret)', os.linesep,
                       '            return -1', os.linesep * 2,
                       '        if %s.msg_id != cs_msg_id_pb2.MSG_ID_%s:' % (
                           nfy_msg_head, name_style_util.camel_to_underline(msg).upper()), os.linesep,
                       '            LOG_ERROR(\'error nfy msg id: %d\' % ' + nfy_msg_head + '.msg_id)', os.linesep,
                       '            return -1', os.linesep * 2,
                       '        %s = self.__make_%s(%s_msg_body)' % (nfy_instance, nfy_instance, nfy_instance),
                       os.linesep * 2,
                       '        return 0', os.linesep]
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
                                 name_style_util.camel_to_underline(msg).lower() + '.py')
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


def generate_test_action_file(msg_proto_file, msg_list_group, output_dir, base_idx, gap, pkg_name, namespace_list):
    for msg_list in msg_list_group:
        if not msg_list or 0 == len(msg_list):
            continue

        for msg in msg_list:
            if msg.endswith('Req') or msg.endswith('Nfy'):
                if output_file(msg, output_dir, pkg_name, namespace_list) != 0:
                    return -1
    return 0


def test_001():
    msg_list_group = []
    msg_mgr_ = one_file_msg_mgr.OneFileMsgMgr()

    msg_proto_file = 'demo_msg.proto'
    if msg_mgr_.read_msg(msg_proto_file) != 0:
        return -1

    msg_list_group.append(msg_mgr_.msg_list)

    if generate_test_action_file(msg_proto_file, msg_list_group, './output/demo', None, None, 'com::moon::demo',
                                 ['proto_tcp']) != 0:
        return -1

    return 0


if __name__ == '__main__':
    test_001()
