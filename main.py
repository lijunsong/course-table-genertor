#!/usr/bin/env python
# encoding: utf-8

from reader import Reader
from course_table import CourseTable
from gen import Generator
from course_pool import CoursePool
from debug import Debug
import sys

file_name = "test.csv"

# 不要输出调试信息
#Debug.PRINT_MARKER = False

if __name__=='__main__':
    # TODO: 添加参数，控制输入文件，控制输出格式
    if len(sys.argv) == 2:
        file_name = sys.argv[1]

    reader = Reader(file_name)

    course_pool = CoursePool(reader.courses)

    # 初始化生成器
    generator = Generator(course_pool)

    generator.gen()

    generator.print_coursetables()
