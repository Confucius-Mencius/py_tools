# -*- coding: UTF-8 -*-

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

# 将指定目录下指定扩展名的文件编码转换成utf8格式，包含子目录

import argparse
import math
import multiprocessing
import os
import file_util
import multitask_util


def process_routine(file_path_list):
    """
    转换前请备份原始文件，转换后的文件会覆盖原文件。
    """

    # print(file_path_list)

    for file_path in file_path_list:
        file_util.convert_to_utf8(file_path, file_path, True)


def partition(file_path_list):
    cpu_count = multiprocessing.cpu_count()
    file_count = len(file_path_list)
    # print('cpu count: %d, file count: %d' % (cpu_count, file_count))

    if file_count <= cpu_count:
        step = 1
    else:
        step = int(math.ceil(float(file_count) / cpu_count))

    # print(step)

    p = [file_path_list[i:i + step] for i in range(0, len(file_path_list), step)]
    return p


def do(dir_, filename_ext_list):
    file_path_list = file_util.file_paths_with_ext_in_dir(dir_, filename_ext_list)
    p = partition(file_path_list)
    # print(p)

    args_list = []

    for i in p:
        args_list.append((i,))

    multitask_util.run_multi_process(len(p), process_routine, args_list)


def partition_aux(n):
    a = []

    for i in range(0, n):
        a.append(i)

    return partition(a)


def demo001():
    for i in range(1, 21):
        print(partition_aux(i))


def demo002():
    do(sys.path[0] + '/../data', ['.h'])


def demo003():
    do('/home/hgc/workspace/mine/hilton/sh_tools/base/LuaFramework_UGUI/', ['.cs', '.lua', '.txt', '.md'])


def parse_args():
    """
    python utf8_convertor.py ../data .h .cpp
    """

    parser = argparse.ArgumentParser()

    parser.add_argument('dir', help='dir')
    parser.add_argument('filename_ext_list', metavar='ext', help='filename ext list, eg: .h .cpp', nargs='*')

    args = parser.parse_args()
    # print(args)

    return args


if __name__ == '__main__':
    args = parse_args()
    do(os.path.realpath(args.dir), args.filename_ext_list)
