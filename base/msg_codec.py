# -*- coding: UTF-8 -*-

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

import binascii
import struct

TOTAL_MSG_LEN_FIELD_LEN = 4
CHECKSUM_FIELD_LEN = 4
PASSBACK_FIELD_LEN = 4
MSG_ID_FIELD_LEN = 4
MIN_TOTAL_MSG_LEN = 12  # checksum, msg head


class MsgHead:
    def __init__(self):
        self.passback = 0
        self.msg_id = 0


def crc32(data, old_crc=0):
    """
    计算data的crc32值。
    :param data:
    :param old_crc: 分多次累进时，上一次计算的crc32。
    :return:
    """

    return binascii.crc32(data, old_crc) & 0xffffffff


def encode(msg_head, msg_body, msg_body_len, do_checksum):
    """
    将参数打包成二进制消息。
    :param msg_head:
    :param msg_body:
    :param msg_body_len:
    :param do_checksum:
    :return: 二进制buf，包含total_msg_len_field, checksum, msg head, msg body。
    """

    try:
        total_msg_len_field = struct.pack('!i', MIN_TOTAL_MSG_LEN + msg_body_len)

        if not msg_body:
            msg_part = struct.pack('!ii', msg_head.passback, msg_head.msg_id)
        else:
            msg_part = struct.pack('!ii', msg_head.passback, msg_head.msg_id) + msg_body

        checksum_part = struct.pack('!I', crc32(msg_part) if do_checksum else 0)

        return total_msg_len_field + checksum_part + msg_part
    except Exception as e:
        print('exception: %s' % e)
        return None


def decode(total_msg_buf, total_msg_len, do_checksum):
    """
    从二进制buf中解包。
    :param total_msg_buf: 二进制buf，包含checksum, msg head, msg_body
    :param total_msg_len: 二进制buf的长度。
    :param do_checksum:
    :return: ret, rsp msg head, rsp msg body
    """
    try:
        checksum_peer, = struct.unpack('!I', total_msg_buf[0:TOTAL_MSG_LEN_FIELD_LEN])
        checksum_self = crc32(total_msg_buf[TOTAL_MSG_LEN_FIELD_LEN:])

        if do_checksum and checksum_self != checksum_peer:
            print('checksum not match, self checksum: %u, peer checksum: %u' % (checksum_self, checksum_peer))
            return -1, None, None

        msg_head = MsgHead()
        msg_head.passback, msg_head.msg_id = struct.unpack('!ii',
                                                           total_msg_buf[TOTAL_MSG_LEN_FIELD_LEN:MIN_TOTAL_MSG_LEN])

        print('total msg len: %d, checksum: %u, passback: %d, msg_id: %d'
              % (total_msg_len, checksum_peer, msg_head.passback, msg_head.msg_id))

        if total_msg_len > MIN_TOTAL_MSG_LEN:
            return 0, msg_head, total_msg_buf[MIN_TOTAL_MSG_LEN:]
        else:
            return 0, msg_head, None
    except Exception as e:
        print('exception: %s' % e)
        return -1, None, None
