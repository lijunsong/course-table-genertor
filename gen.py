#!/usr/bin/env python
# encoding: utf-8

import configure as cfg
import debug
import sys

d = debug.Debug('generator')

class Generator:
    """排课程的类

    Attributes:
    """
    def __init__(self, course_pool):
        self.course_pool = course_pool
        self.sorted_course = course_pool.sort_course()
        self.tables = tables

    def set_course(self, courseid):
        "在相应的课表上找最佳位置摆放"
        # 1. 得到与之相关的所有课表
        tables = self.course_to_table(courseid)
        # 2. 在相关的几个课表上，找到一个 *都空着的* *最佳* 位置
        # 2.1 首先几个课表有的满，有的空。先从满的开始找位置（如果比较
        #     满的课表找不到位置，就肯定找不到位置了
        max_table = self.find_max_course_num(tables)
        # 2.2 找到了最满的课，开始找一个最佳位置

        # 3. 放到这个位置上

    #-----------辅助函数------------

    #-----------对 course_pool 进行包装 -----------------
    def course_to_table(self, courseid):
        return self.course_pool.course_to_table(courseid)
    def find_max_course_num(self, tables):
        return self.course_pool.find_max_course_num(tables)
    ## 主要函数 ##
    def gen(self):
        for course in self.sorted_course:
            self.set_course(course.cid)

if __name__=='__main__':
    from reader import Reader
    from course_table import CourseTable
    from course_pool import CoursePool

    reader = Reader('test.csv')
    course_pool = CoursePool(reader.courses)

    generator = Generator(course_pool)

    new_tables = generator.gen()

    print new_tables[0].pretty_str()
