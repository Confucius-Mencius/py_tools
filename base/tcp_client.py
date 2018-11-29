# -*- coding: UTF-8 -*-

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

import socket
import struct
import msg_codec


class TcpClient(object):
    def __init__(self, server_addr, server_port, timeout=None, linger=False):
        """
        创建tcp socket并连接指定服务器。
        :param server_addr:
        :param server_port:
        :param timeout:
        :param linger:
        :return:
        """

        self.server_addr = server_addr
        self.server_port = server_port
        self.sock = None

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            if timeout:
                sock.settimeout(timeout)

            # 降低限制(仅测试用)
            if linger:
                l_onoff = 1
                l_linger = 0
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', l_onoff, l_linger))

            sock.connect((self.server_addr, self.server_port))

            print('connect to %s:%d ok' % (self.server_addr, self.server_port))
            self.sock = sock
        except Exception as e:
            print('exception: %s' % e)

    def __del__(self):
        """
        关闭socket。
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
            # start_time = datetime.datetime.now()
            # LogInfo('send begin time: %s' % start_time)

            data = msg_codec.encode(msg_head, msg_body, msg_body_len, do_checksum)
            if not data:
                print('no data')
                return -1

            self.sock.send(data)

            # end_time = datetime.datetime.now()
            # LogInfo('send end time: %s' % end_time)
            # LogInfo('pure, send-begin ~ send-end time used: %d, %d' % (
            #     (end_time - start_time).seconds, (end_time - start_time).microseconds))

            return 0
        except Exception as e:
            print('exception: %s' % e)
            return -1

    def __recv_a_complete_msg(self):
        """
        从socket中接收一个完整的消息，如果还有剩余的字节，则放在sock里面不读。
        :return: total_msg_buf, total_msg_len。其中total_msg_buf包含checksum, msg_head, msg_body。
        """

        try:
            msg_len_data_list = []
            read_len = 0

            while read_len < msg_codec.TOTAL_MSG_LEN_FIELD_LEN:
                data = self.sock.recv(msg_codec.TOTAL_MSG_LEN_FIELD_LEN - read_len)
                data_len = len(data)

                if 0 == data_len:
                    print('read len: %d, data len: %d, data: "%s"' % (read_len, data_len, data))
                    break

                read_len += data_len
                msg_len_data_list.append(data)

            if read_len < msg_codec.TOTAL_MSG_LEN_FIELD_LEN:
                print('read len: %d' % read_len)
                return None, 0

            msg_len_field_buf = ''.join(msg_len_data_list)
            total_msg_len, = struct.unpack('!i', msg_len_field_buf)

            total_msg_data_list = []
            read_len = 0

            while read_len < total_msg_len:
                data = self.sock.recv(total_msg_len - read_len)
                data_len = len(data)

                if 0 == data_len:
                    print('read len: %d, data len: %d, data: "%s"' % (read_len, data_len, data))
                    break

                read_len += data_len
                total_msg_data_list.append(data)
        except Exception as e:
            print('exception: %s' % e)
            return None, 0

        if read_len < total_msg_len:
            print('read len: %d, total msg len: %d' % (read_len, total_msg_len))
            return None, 0

        total_msg_buf = ''.join(total_msg_data_list)
        return total_msg_buf, total_msg_len

    def recv(self, do_checksum):
        """
        从socket中接收一个完整的消息并解包。
        :param do_checksum:
        :return: ret, rsp msg head, rsp msg body
        """

        try:
            total_msg_buf, total_msg_len = self.__recv_a_complete_msg()
            if 0 == total_msg_len or total_msg_len != len(total_msg_buf):
                print('total msg len: %d' % total_msg_len)
                return -1, None, None

            return msg_codec.decode(total_msg_buf, total_msg_len, do_checksum)
        except Exception as e:
            print('exception: %s' % e)
            return -1, None, None
