# -*- coding: utf-8 -*-

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################


def camel_to_underline(camel_name):
    """
    驼峰法命名格式转下划线命名格式。
    :param camel_name:
    :return:
    """

    underline_name = ''

    for ch in camel_name:
        if ch.isdigit():
            underline_name += ch
        else:
            underline_name += ch if ch.islower() else '_' + ch.lower()

    if '_' == underline_name[0]:
        return underline_name[1:]
    else:
        return underline_name


def underline_to_camel(underline_name):
    """
    下划线命名格式驼峰法命名格式。
    :param underline_name:
    :return:
    """

    orig_token_list = underline_name.split('_')
    capitalize_token_list = []

    for token in orig_token_list:
        capitalize_token_list.append(token.capitalize())

    camel_name = ''.join(capitalize_token_list)
    return camel_name


def demo001():
    assert 'demo100_req' == camel_to_underline('Demo100Req')
    assert 'hello_world' == camel_to_underline('HelloWorld')
    assert 'hello_world' == camel_to_underline('helloWorld')
    assert 'HelloWorld' == underline_to_camel('hello_world')
    assert 'Demo100Req' == underline_to_camel('demo100_req')


if __name__ == '__main__':
    demo001()
