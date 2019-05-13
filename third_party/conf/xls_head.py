# -*- coding: utf-8 -*-

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

import os
import sys

sys.path.append('%s/../..' % os.path.split(os.path.realpath(__file__))[0])  # 导入上级目录中的模块
# print(sys.path)

import types
from base import xls_util


class XlsHead(xls_util.XlsHeadInterface):
    """
    自定义的xls head
    """

    def __init__(self):
        # 格式说明：第0行是表头，从第1行开始是内容；最后一列是note，不读。

        # 各列的名字=>列的idx、类型
        self.conf = {'key': {'col': 0, 'type': types.StringType},
                     'basename': {'col': 1, 'type': types.StringType},
                     'ext': {'col': 2, 'type': types.StringType},
                     'use': {'col': 3, 'type': types.BooleanType}}

        # 调用接口XlsHeadInterface中的方法
        self.init(1, self.conf)


def test_001():
    xls_head_ = XlsHead()
    xls_loader = xls_util.XlsLoader('./third_party.csv', xls_head_.nrows, xls_head_.ncols, xls_head_.col_types)
    assert 0 == xls_loader.load()


if __name__ == "__main__":
    test_001()
