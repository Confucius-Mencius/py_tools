# -*- coding: UTF-8 -*-

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

###############################################################################
# 注意：由于不存在全局初始化的逻辑，本文件未被引用。
###############################################################################

#
# 注意：nose会自动搜索名字含有"test"字样的函数和类作为用例来运行，
# 自己定义的消息名（协议中）不要含有test字样，否则会被nose当做用例而报如下错误：
# Failure: TypeError (__init__() takes exactly 2 arguments (1 given)) ... ERROR
# ----------------------------------------------------------------------
# Traceback (most recent call last):
#   File "/usr/local/lib/python2.7/dist-packages/nose-1.3.7-py2.7.egg/nose/loader.py", line 523, in makeTest
#     return self._makeTest(obj, parent)
#   File "/usr/local/lib/python2.7/dist-packages/nose-1.3.7-py2.7.egg/nose/loader.py", line 582, in _makeTest
#     return MethodTestCase(obj)
#   File "/usr/local/lib/python2.7/dist-packages/nose-1.3.7-py2.7.egg/nose/case.py", line 345, in __init__
#     self.inst = self.cls()
# TypeError: __init__() takes exactly 2 arguments (1 given)


from nose import with_setup


def setup_module():
    print('setup_module执行于一切开始之前')


def teardown_module():
    print('teardown_module执行于一切结束之后')


def setup_001():
    print('setup_001将用于with_setup')


def teardown_001():
    print('teardown_001也将用于with_setup')


@with_setup(setup_001, teardown_001)
def test_001():
    print('in test_001')
    assert 3 * 4 == 12


# 以test开头的函数会被nose识别并执行。
def test_002():
    print('in test_002')
    assert 3 * 4 == 12


# 以Test开头的类会被nose识别并执行其中以test开头或结尾的成员函数。
class TestDemo(object):
    def setup(self):
        print('setup执行于本类中每条用例之前')

    def teardown(self):
        print('teardown执行于本类中每条用例之后')

    @classmethod
    def setup_class(cls):
        print('setup_class执行于本类中任何用例开始之前，且仅执行一次')

    @classmethod
    def teardown_class(cls):
        print('teardown_class执行于本类中所有用例结束之后，且仅执行一次')

    def test_001(self):
        print('in test_001')
        assert 'a' + str(3) == 'a3'

    def test_002(self):
        print('in test_002')
        assert 'a' + str(3) == 'a3'

# 执行nosetests -v --nocapture test_util.py
# 输出如下：
# setup_module执行于一切开始之前
# setup_class执行于本类中任何用例开始之前，且仅执行一次
# base.test_util.TestDemo.test_001 ... setup执行于本类中每条用例之前
# in test_001
# teardown执行于本类中每条用例之后
# ok
# base.test_util.TestDemo.test_002 ... setup执行于本类中每条用例之前
# in test_002
# teardown执行于本类中每条用例之后
# ok
# teardown_class执行于本类中所有用例结束之后，且仅执行一次
# base.test_util.test_001 ... setup_001将用于with_setup
# in test_001
# teardown_001也将用于with_setup
# ok
# base.test_util.test_002 ... in test_002
# ok
# teardown_module执行于一切结束之后
#
# ----------------------------------------------------------------------
# Ran 4 tests in 0.006s
#
# OK
