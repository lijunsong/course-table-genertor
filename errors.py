#!/usr/bin/env python
# encoding: utf-8

# 这个文件定义了排课程序中可能出现的错误

class Error(Exception):
    "基本错误"
    pass

# 读取过程中出现的错误
class TimeFormatError(Error):
    """时间格式错误

    Attributes:
        msg -- 错误的时间格式
    """
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

class MissingColumnError(Error):
    """CSV 文件中少列的错误

    Attributes:
        line -- 出现错误的行
    """
    def __init__(self, line)
        self.line = line
    def __str__(self):
        return self.line
