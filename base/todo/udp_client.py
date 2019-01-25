# -*- coding: UTF-8 -*-

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

import socket
import msg_codec


class UdpClient(object):
    def __init__(self, server_addr, server_port, timeout=None):
        """
        创建udp socket并记录服务器的地址和端口。
        :param server_addr:
        :param server_port:
        :param timeout
        """

        self.server_addr = server_addr
        self.server_port = server_port
        self.sock = None

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            if timeout:
                sock.settimeout(timeout)

            self.sock = sock
        except Exception as e:
            print('exception: %s' % e)

    def __del__(self):
        """
        关闭socket。
        :return:
        """

        try:
            self.sock.close()
            self.sock = None
        except Exception as e:
            print('exception: %s' % e)

    def server(self):
        return '%s:%d' % (self.server_addr, self.server_port)

    def send(self, msg_head, msg_body, msg_body_len, do_checksum):
        """
        将参数打包成二进制消息并通过socket发送出去。
        :param msg_head:
        :param msg_body:
        :param msg_body_len:
        :param do_checksum:
        :return: =0表示成功，否则失败。
        """

        try:
            data = msg_codec.encode(msg_head, msg_body, msg_body_len, do_checksum)
            self.sock.sendto(data, (self.server_addr, self.server_port))
            return 0
        except Exception as e:
            print('exception: %s' % e)
            return -1

    def recv(self, max_msg_len, do_checksum):
        """
        从socket中接收一个完整的消息并解包。
        :param max_msg_len:
        :param do_checksum:
        :return: ret, rsp msg head, rsp msg body
        """
        try:
            buf, addr = self.sock.recvfrom(max_msg_len)

            if not buf or len(buf) < msg_codec.TOTAL_MSG_LEN_FIELD_LEN:
                print('not a whole msg')
                return -1, None, None

            return msg_codec.decode(buf[msg_codec.TOTAL_MSG_LEN_FIELD_LEN:],
                                    len(buf) - msg_codec.TOTAL_MSG_LEN_FIELD_LEN, do_checksum)
        except Exception as e:
            print('exception: %s' % e)
            return -1, None, None
