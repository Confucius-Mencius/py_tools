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


def output_file_content(fp, msg, pkg_name):
    try:
        msg_instance = msg[0].lower() + msg[1:]
        tab_blank = ' ' * 4

        content = ['using System;', os.linesep,
                   'using UnityEngine;', os.linesep,
                   'using %s.cs;' % pkg_name.replace('::', '.'), os.linesep * 2,
                   'public class %sHandler : MsgHandler' % msg, os.linesep,
                   '{', os.linesep,
                   '%spublic int GetMsgId()' % tab_blank, os.linesep,
                   '%s{' % tab_blank, os.linesep,
                   '%sreturn (int) MsgId.MSG_ID_%s;' % (tab_blank * 2, name_style_util.camel_to_underline(msg).upper()),
                   os.linesep,
                   '%s}' % tab_blank, os.linesep * 2,
                   '%spublic void OnMsg(TcpMsg msg)' % tab_blank, os.linesep,
                   '%s{' % tab_blank, os.linesep,
                   '%stry' % (tab_blank * 2), os.linesep,
                   '%s{' % (tab_blank * 2), os.linesep,
                   '%s%s %s = TcpMsg.Deserialize<%s>(msg.MsgBody);' % (tab_blank * 3, msg, msg_instance, msg),
                   os.linesep * 2]
        fp.write(''.join(content).encode('utf-8'))

        if msg.endswith('Rsp'):
            content = ['%sif (%s.err_ctx.err_code != 0)' % (tab_blank * 3, msg_instance), os.linesep,
                       '%s{' % (tab_blank * 3), os.linesep,
                       '%sGameCtrl.Instance.TipsCtrl.AppendTips(ErrCode.Instance.GetErrDesc(%s.err_ctx.err_code));' % (
                           tab_blank * 4, msg_instance), os.linesep,
                       '%sreturn;' % (tab_blank * 4), os.linesep,
                       '%s}' % (tab_blank * 3), os.linesep * 2]
            fp.write(''.join(content).encode('utf-8'))

        content = ['%s}' % (tab_blank * 2), os.linesep,
                   '%scatch (Exception e)' % (tab_blank * 2), os.linesep,
                   '%s{' % (tab_blank * 2), os.linesep,
                   '%sDebug.Log(e.ToString());' % (tab_blank * 3), os.linesep,
                   '%s}' % (tab_blank * 2), os.linesep,
                   '%s}' % tab_blank, os.linesep,
                   '}', os.linesep]
        fp.write(''.join(content).encode('utf-8'))

        return 0
    except Exception as e:
        print('exception: %s' % e)
        return -1


def output_file(msg, output_dir, pkg_name):
    file_path = os.path.join(output_dir, msg + 'Handler.cs')
    file_util.del_file(file_path)
    file_util.make_dir(file_util.file_dir(file_path))

    try:
        fp = open(file_path, 'wb')

        output_file_content(fp, msg, pkg_name)
        fp.close()

        print('=== generate %s done ===' % file_path)
    except Exception as e:
        print('exception: %s' % e)
        return -1

    return 0


def generate_csharp_msg_handler_file(msg_list_group, output_dir, base_idx, gap, pkg_name, namespace_list):
    for msg_list in msg_list_group:
        if not msg_list or 0 == len(msg_list):
            continue

        for msg in msg_list:
            if msg.endswith('Rsp') or msg.endswith('Nfy'):
                if output_file(msg, output_dir, pkg_name) != 0:
                    return -1
    return 0


def test_001():
    msg_list_group = []
    msg_mgr_ = one_file_msg_mgr.OneFileMsgMgr()

    if msg_mgr_.read_msg('./demo_msg.proto') != 0:
        return -1

    msg_list_group.append(msg_mgr_.msg_list)

    if generate_csharp_msg_handler_file(msg_list_group, './output/demo', None, None, 'com::moon::demo::proto::cs',
                                        None) != 0:
        return -1

    return 0


if __name__ == '__main__':
    test_001()
