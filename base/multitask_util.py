# -*- coding: UTF-8 -*-

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

import multiprocessing
import threading


def run_multi_process(n, routine, args_list=None):
    """
    启动n个进程执行routine函数。
    :param n: 进程数，>0
    :param routine: 进程函数
    :param args_list: 形如[(a, b, c), (1, 2, 3)]，列表的n个元素分别对应第n个进程的参数
    :return:
    """

    if args_list and len(args_list) != n:
        return

    process_list = []

    for i in range(0, n):
        if args_list:
            process = multiprocessing.Process(target=routine, name='process-%d' % i, args=args_list[i])
        else:
            process = multiprocessing.Process(target=routine, name='process-%d' % i)

        process_list.append(process)
        process.start()
        # print('start: %d' % i + 1)

    c = 0
    for process in process_list:
        process.join()
        c = c + 1
        # print('end: %d' % c)


def process_routine_001():
    process = multiprocessing.current_process()
    print(process.name)


def demo_multi_process_001():
    run_multi_process(10, process_routine_001)


def process_routine_002(i):
    print(i)
    process = multiprocessing.current_process()
    print(process.name)


def demo_multi_process_002():
    args_list = []
    for i in range(0, 10):
        args_list.append((i,))

    run_multi_process(10, process_routine_002, args_list)


def run_multi_thread(n, routine, args_list=None):
    """
    启动n个线程执行routine函数。
    :param n: 线程数，>0
    :param routine: 线程函数
    :param args_list: 形如[(a, b, c), (1, 2, 3)]，列表的n个元素分别对应第n个线程的参数
    :return:
    """

    if args_list and len(args_list) != n:
        return

    thread_list = []

    for i in range(0, n):
        if args_list:
            thread = threading.Thread(target=routine, name='thread-%d' % i, args=args_list[i])
        else:
            thread = threading.Thread(target=routine, name='thread-%d' % i)

        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()


def thread_routine_001():
    thread = threading.currentThread()
    print(thread.getName())


def demo_multi_thread_001():
    run_multi_thread(10, thread_routine_001)


def thread_routine_002(i):
    print(i)
    thread = threading.currentThread()
    print(thread.getName())


def demo_multi_thread_002():
    args_list = []
    for i in range(0, 10):
        args_list.append((i,))

    run_multi_thread(10, thread_routine_002, args_list)


if __name__ == '__main__':
    demo_multi_process_001()
    demo_multi_process_002()
    demo_multi_thread_001()
    demo_multi_thread_002()
