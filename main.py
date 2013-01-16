#!/usr/bin/env python
# encoding: utf-8

from reader import Reader
from course_table import CourseTable
from generator import Generator
from debug import Debug
file_name = "test.csv"

# 不要输出调试信息
Debug.PRINT_MARKER = False

if __name__=='__main__':
    reader = Reader(file_name)

    #得到年级与相应课程的映射
    grad_course = reader.get_grades_courses()

    # 初始化课程表
    tables = []
    for k in grad_course:
        tables.append(CourseTable(grad_course[k]))

    # debug
    #for table in tables:
    #    print table.pretty_str()
    # 初始化生成器
    generator = Generator(tables)

    new_tables = generator.generate()

    # 得到最终结果
    for table in new_tables:
        print "GRADE: %s" % table.title
        print table.pretty_str()
