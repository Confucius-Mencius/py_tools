# -*- coding: utf-8 -*-

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################


import types


def empty_str(arg):
    """
    判断参数字符串是否为空。
    :param arg:
    :return:
    """

    return 0 == len(arg)


def empty_int(arg):
    """
    判断参数整数是否为空，即等于0。
    :param arg:
    :return:
    """

    return 0 == arg


def empty_float(arg):
    """
    判断参数浮点数是否为空，即等于0。
    :param arg:
    :return:
    """

    return 0 == arg


def empty_bool(arg):
    """
    判断参数布尔值是否为空，即等于False。
    :param arg:
    :return:
    """

    return not arg


def empty(type_):
    """
    根据type_获取判断参数值是否为空的函数。
    :param type_:
    :return:
    """
    if types.StringType == type_:
        return empty_str
    elif types.IntType == type_:
        return empty_int
    elif types.FloatType == type_:
        return empty_float
    elif types.BooleanType == type_:
        return empty_bool
    else:
        print('not supported type: %s' % type_)
        return None


def value_str(arg):
    """
    返回参数字符串，如果为空则返回空字符串。
    :param arg:
    :return:
    """

    if not arg or 0 == len(arg):
        return ''
    else:
        return arg


def value_int(arg):
    """
    将参数字符串转换成整数返回，如果为空则返回0。
    :param arg:
    :return:
    """

    if not arg or 0 == len(arg):
        return 0
    else:
        return int(arg)


def value_float(arg):
    """
    将参数字符串转换成浮点数返回，如果为空则返回0。
    :param arg:
    :return:
    """

    if not arg or 0 == len(arg):
        return 0
    else:
        return float(arg)


def value_bool(arg):
    """
    将参数字符串转换成布尔值返回，如果为空则返回False。
    :param arg: ‘0’或‘1’
    :return: 如果字符串为‘0’返回False，否则返回True。
    """
    if not arg or 0 == len(arg):
        return False
    else:
        return int(arg) != 0


def value(type_):
    """
    根据type_获取将string转换成其类型值的函数。
    :param type_:
    :return:
    """

    if types.StringType == type_:
        return value_str
    elif types.IntType == type_:
        return value_int
    elif types.FloatType == type_:
        return value_float
    elif types.BooleanType == type_:
        return value_bool
    else:
        print('not supported type: %s' % type_)
        return None


def demo001():
    assert empty_str == empty(types.StringType)
    assert empty_int == empty(types.IntType)
    assert empty_float == empty(types.FloatType)
    assert empty_bool == empty(types.BooleanType)
    assert not empty(types.ClassType)


def demo002():
    assert value_str == value(types.StringType)
    assert value_int == value(types.IntType)
    assert value_float == value(types.FloatType)
    assert value_bool == value(types.BooleanType)
    assert not value(types.ClassType)


if __name__ == '__main__':
    demo001()
    demo002()
