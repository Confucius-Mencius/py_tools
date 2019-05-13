# -*- coding: utf-8 -*-

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

import codecs;
import chardet
import os
import sys


def script_dir():
    """
    获取调用该函数的脚本文件自身所在的绝对目录。
    """

    return os.path.split(os.path.realpath(__file__))[0]


def file_dir(file_path):
    """
    获取文件所在的目录。
    :param file_path:
    :return:
    """

    return os.path.split(os.path.realpath(file_path))[0]


def base_filename(file_path):
    """
    获取不带目录和扩展名的文件名。
    :param file_path:
    :return:
    """

    return os.path.splitext(os.path.basename(file_path))[0]


def filename_ext(file_path):
    """
    获取文件的扩展名。
    :param file_path:
    :return:
    """

    return os.path.splitext(file_path)[1]


def make_dir(dir_):
    """
    创建多级目录。
    :param dir_:
    :return: =0表示成功，否则失败。
    """

    try:
        if not os.path.exists(dir_):
            os.makedirs(dir_)
        return 0
    except Exception as e:
        print('failed to make dir %s: %s' % (dir_, e))
        return -1


def create_file(file_path):
    if os.path.exists(file_path):
        return 0

    dir_ = file_dir(file_path)
    if not os.path.exists(dir_):
        make_dir(dir_)

    try:
        os.mknod(file_path, 0664)
    except Exception as e:
        print('failed to create file %s: %s' % (file_path, e))
        return -1


def del_file(file_path):
    """
    删除文件/目录，如果目录中有文件则一起删除。
    :param file_path:
    :return: =0表示成功，否则失败。
    """

    if not os.path.exists(file_path):
        return 0

    if os.path.isfile(file_path):
        try:
            os.remove(file_path)
            return 0
        except Exception as e:
            print('failed to del file %s: %s' % (file_path, e))
            return -1
    else:
        for f in os.listdir(file_path):
            sub_file_path = os.path.join(file_path, f)
            del_file(sub_file_path)

        try:
            os.rmdir(file_path)
            return 0
        except Exception as e:
            print('failed to del dir %s: %s' % (file_path, e))
            return -1


def file_paths_with_ext_in_dir(dir_, filename_ext_list=None):
    """
    获取目录下指定扩展名的全部文件，返回文件路径列表
    :param dir_:
    :param filename_ext_list: 文件扩展名列表，为None表示所有文件
    :return: 返回文件路径列表
    """

    file_path_list = []

    for dirpath, dirnames, filenames in os.walk(dir_):
        # print('dir: %s' % dirpath)

        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            # print('file: %s' % file_path)

            if filename_ext_list and len(filename_ext_list) > 0:
                if filename_ext(file_path) in filename_ext_list:
                    file_path_list.append(os.path.realpath(file_path))
            else:
                file_path_list.append(os.path.realpath(file_path))

    return file_path_list


def replace_content(file_path, text_list):
    """
    替换文件内容中的关键字。
    :param file_path:
    :param text_list: 形如["old_text_1 new_text_1", "old_text_2 new_text_2"]的列表。
    :return: =0表示成功，否则失败。
    """

    old_text_list = []
    new_text_list = []

    for text in text_list:
        old_text, new_text = text.split()
        old_text_list.append(old_text)
        new_text_list.append(new_text)

    try:
        tmp_file = file('%s.tmp' % file_path, 'wb')

        with open(file_path, 'rb') as orig_file:
            for line in orig_file:
                for i in range(0, len(old_text_list)):
                    line = line.replace(old_text_list[i], new_text_list[i])

                tmp_file.write(line)

        tmp_file.close()

        os.rename(file_path, '%s.bak' % file_path)
        os.rename('%s.tmp' % file_path, file_path)

        return 0
    except Exception as e:
        print('exception: %s' % e)
        return -1


def convert_to_utf8(from_file_path, to_file_path, add_bom=False):
    try:
        from_file = open(from_file_path, 'rb')
        from_file_content = from_file.read()
        from_file.close()

        from_file_encoding = chardet.detect(from_file_content)['encoding']
        print('from file path: %s(%s)' % (from_file_path, from_file_encoding))

        # (1) ascii是utf-8的子集，不用转
        # (2) utf - 8 不用转，如果没有bom头就加上
        if 0 == from_file_encoding.lower().find('ascii'):
            return 0
        elif -1 == from_file_encoding.lower().find('utf-8'):
            if not os.path.exists(to_file_path):
                create_file(to_file_path)

        to_file = open(to_file_path, 'wb')

        if 0 == from_file_encoding.lower().find('utf-8'):
            fcontent = from_file_content
        else:
            fcontent = from_file_content.decode(from_file_encoding).encode('utf-8')

        if add_bom and fcontent[:3] != codecs.BOM_UTF8:
            new_fcontent = codecs.BOM_UTF8
            new_fcontent += fcontent
        else:
            new_fcontent = fcontent

        to_file.write(new_fcontent)
        to_file.close()

        print('=== convert %s(%s) to %s(utf8) done ===' % (from_file_path, from_file_encoding, to_file_path))

        return 0
    except Exception as e:
        print('exception: %s' % e)
        return -1


def demo001():
    print os.getcwd()
    print sys.path[0]  # 脚本文件自身所在的绝对目录，注意：这里的脚本文件指的是启动的那个脚本文件
    print script_dir()
    assert sys.path[0] == script_dir()
    assert '/tmp' == file_dir('/tmp/my_app.log')
    assert os.getcwd() == file_dir('./my_app.log')
    assert 'my_app' == base_filename('/tmp/my_app.log')
    assert 'my_app' == base_filename('./my_app.log')
    assert '.log' == filename_ext('/tmp/my_app.log')
    assert '.log' == filename_ext('./my_app.log')


def demo002():
    print(file_paths_with_ext_in_dir('.', ['.py']))
    print(file_paths_with_ext_in_dir('.'))


def demo003():
    ret = replace_content(sys.path[0] + '/../data/xx_conf_mgr.h', ["Tcp TCP", "Io IO", "Cpu CPU", "Udp UDP"])
    assert 0 == ret


def demo004():
    gb2312_file = sys.path[0] + '/../data/AboutLayer.h'
    utf8_file1 = sys.path[0] + '/../data/AboutLayer.h'
    assert 0 == convert_to_utf8(gb2312_file, utf8_file1)

    utf8_file = sys.path[0] + '/../data/utf8_file'
    assert 0 == convert_to_utf8(utf8_file, None)


def demo005():
    convert_to_utf8("/home/sunlands/workspace/rtmp_pusher/main.cpp", "/home/sunlands/workspace/rtmp_pusher/main.cpp",
                    True)


if __name__ == '__main__':
    demo005()
    # demo002()
    # demo003()
    # demo004()
