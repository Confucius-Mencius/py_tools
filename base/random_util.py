# -*- coding: UTF-8 -*-

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

import random
import string


def rand_str(len_):
    random.seed()
    return ''.join(random.sample(string.ascii_letters + string.digits, len_))


def rand_digit(len):
    random.seed()
    return int(''.join(random.sample(string.digits, len)))


def demo001():
    print(rand_str(10))
    print(rand_digit(10))


if __name__ == '__main__':
    demo001()
