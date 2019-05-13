# -*- coding: utf-8 -*-

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

import os
import sys

sys.path.append('%s/../../py_tools' % os.path.split(os.path.realpath(__file__))[0])  # 导入上级目录中的模块
# print(sys.path)

import types
from base import xls_util


class XlsHead(xls_util.XlsHeadInterface):
    """
    自定义的xls head
    """

    def __init__(self):
        # 格式说明：第0行是表头，从第1行开始是内容。

        # 各列的名字=>列的idx、类型
        self.conf = {'name': {'col': 0, 'type': types.StringType},
                     'value': {'col': 1, 'type': types.IntType},
                     'desc_en': {'col': 2, 'type': types.StringType},
                     'desc_zh': {'col': 3, 'type': types.StringType}}

        # 调用接口XlsHeadInterface中的init方法
        self.init(1, self.conf)


def test_001():
    xls_head_ = XlsHead()
    xls_loader = xls_util.XlsLoader('./demo_proj_err_code.csv', xls_head_.nrows, xls_head_.ncols, xls_head_.col_types)
    assert 0 == xls_loader.load()


if __name__ == "__main__":
    test_001()
