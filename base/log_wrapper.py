# -*- coding: UTF-8 -*-

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

import logging
from logging.handlers import RotatingFileHandler


class LogWrapper(object):
    def __init__(self, logger_name, log_file_path, log_level=logging.DEBUG):
        """
        定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M。
        :param logger_name:
        :param log_file_path:
        :param log_level: logging.ERROR > logging.WARNING > logging.INFO > logging.DEBUG
        """

        self.logger_name = logger_name

        rt_handler = RotatingFileHandler(log_file_path, maxBytes=10 * 1024 * 1024, backupCount=5)
        rt_handler.setLevel(log_level)

        log_format = '[%(levelname)s %(name)s %(thread)d %(asctime)s %(filename)s:%(lineno)d] %(message)s'
        formatter = logging.Formatter(log_format)
        rt_handler.setFormatter(formatter)

        logging.getLogger(logger_name).addHandler(rt_handler)
        logging.getLogger(logger_name).setLevel(log_level)


def demo001():
    # log util
    log_wrapper = LogWrapper('my_app', './my_app.log')

    LOG_DEBUG = logging.getLogger(log_wrapper.logger_name).debug
    LOG_INFO = logging.getLogger(log_wrapper.logger_name).info
    LOG_WARN = logging.getLogger(log_wrapper.logger_name).warning
    LOG_ERROR = logging.getLogger(log_wrapper.logger_name).error

    LOG_DEBUG('hello')
    LOG_DEBUG('hello %s' % 'world')


if __name__ == '__main__':
    demo001()
