# -*- coding: utf-8 -*-

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

import re


class OneFileMsgMgr(object):
    def __init__(self):
        self.msg_list = []

    def read_msg(self, msg_proto_file):
        try:
            with open(msg_proto_file) as f:
                for line in f:
                    if re.match(r'^/{0,2}message \w+(Req|Rsp|Nfy) {$', line):
                        msg_list = re.findall(r'^/{0,2}message (.+?) {$', line)
                        self.msg_list.append(msg_list[0])
                        continue

                    if re.match(r'^/{0,2}message \w+(Req|Rsp|Nfy)$', line):
                        msg_list = re.findall(r'^/{0,2}message (.+?)$', line)
                        self.msg_list.append(msg_list[0])

            return 0
        except Exception as e:
            print('exception: %s' % e)
            return -1

    def show_msg(self):
        for msg in self.msg_list:
            print(msg)


def test_001():
    one_file_msg_mgr_ = OneFileMsgMgr()
    one_file_msg_mgr_.read_msg('./demo_msg.proto')
    one_file_msg_mgr_.show_msg()


if __name__ == '__main__':
    test_001()
