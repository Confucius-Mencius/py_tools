# -*- coding: UTF-8 -*-

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

import logging
import cloghandler


class ConcurrentLogWrapper(object):
    def __init__(self, logger_name, log_file_path, log_level=logging.DEBUG):
        """
        定义一个支持多进程访问的RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M。
        :param logger_name:
        :param log_file_path:
        :param log_level: logging.ERROR > logging.WARNING > logging.INFO > logging.DEBUG
        """

        self.logger_name = logger_name

        crt_handler = cloghandler.ConcurrentRotatingFileHandler(log_file_path, mode='a', maxBytes=10 * 1024 * 1024,
                                                                backupCount=5, encoding="utf-8", debug=False, delay=1)
        crt_handler.setLevel(log_level)

        log_format = '[%(levelname)s %(name)s %(thread)d %(asctime)s %(filename)s:%(lineno)d] %(message)s'
        formatter = logging.Formatter(log_format)
        crt_handler.setFormatter(formatter)

        logging.getLogger(logger_name).addHandler(crt_handler)
        logging.getLogger(logger_name).setLevel(log_level)


# base目录下的测试不要以test开头，否则会被外部使用者跑测试时一起跑
def demo001():
    # log util
    clog_wrapper = ConcurrentLogWrapper('my_app', './my_app.log')

    LOG_DEBUG = logging.getLogger(clog_wrapper.logger_name).debug
    LOG_INFO = logging.getLogger(clog_wrapper.logger_name).info
    LOG_WARN = logging.getLogger(clog_wrapper.logger_name).warning
    LOG_ERROR = logging.getLogger(clog_wrapper.logger_name).error

    LOG_DEBUG('hello')
    LOG_DEBUG('hello %s' % 'world')


if __name__ == '__main__':
    demo001()
