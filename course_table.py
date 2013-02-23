#!/usr/bin/env python
# encoding: utf-8

import configure as cfg
import sys

class CourseTable:
    """表示课程表的数据结构
    二维数组表示。每个年级只有一张课程表

    Attributes:
        title       -- 表名（年级名）
        table       -- 表格，int 类型的二维数组
        eachday_course -- 每天各有多少课程
    """
    def __init__(self, title):
        self.title = title
        self.table = [[-1 for i in cfg.DAY] for j in cfg.TIME]
        self.eachday_course = [0 for i in cfg.DAY]

    def get_course_num(self):
        "得到当前课表已经设置了多少门课了"
        return sum(self.eachday_course)

    def set(self, course, pos, course_pool):
        """在课表上的 pos 位置放置 course

        NOTE: 同时对每天的课程进行统计

        Argument:
            course -- Course 类型的课程
            pos    -- 放置的位置，(tupleof int int)
        """
        credit = course.credit
        cid = course.cid
        time, day = pos
        for i in xrange(credit):
            self.table[time + i][day] = cid
            self.eachday_course[day] += 1
        teachers = course.teachers
        for t in teachers:
            ec = [0 for i in cfg.DAY]
            if t in course_pool._eachday_course_of_teacher:
                ec = course_pool._eachday_course_of_teacher[t]
            ec[day] += credit
            course_pool._eachday_course_of_teacher[t] = ec
            
    def __str__(self):
        "返回二维数组"
        res = ['TITLE: %s\n' % self.title]
        for i in xrange(len(cfg.TIME)):
            for j in xrange(len(cfg.DAY)):
                res.append(str(self.table[i][j]))
                res.append('  ')
            res.append('\n')
        return "".join(res)



if __name__=='__main__':
    from reader import Reader
    r = Reader('test.csv')
    cs = r.filter_courses('Grads 2012 Fall')
    table = CourseTable(cs)
