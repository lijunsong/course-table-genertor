#!/usr/bin/env python
# encoding: utf-8

import configure as cfg

class CourseTable:
    """课程表
    二维数组表示。每个年级只有一张课程表

    Attributes:
        all_courses -- 代表本张课程表上的所有的课程
        title       -- 表名（年级名）
        table       -- 表格，int 类型的二维数组
        unallocs    -- 所有课程中还没有预置的课程
    """
    def __init__(self, all_courses):
        # 所有课程应该是同一个年级的所有课程
        if not _same_grade_p(all_courses):
            sys.exit("[2]construct course table error")
            
        self.all_courses = all_courses
        self.title = all_courses[0].grade
        self.table = [[-1 for i in cfg.DAY] for j in cfg.TIME]
        self.unallocs = self._get_unallocs()

    def _same_grade_p(self, courses):
        """所有的课程只能是同一个年级的课程

        Return
            (listof Courses) => boolean
        """
        grades = set([c.grade for c in courses])
        return len(grades) == 1

    def _get_unallocs(self):
        f = lambda c: c.need_allocate_p()
        return filter(f, self.all_courses)

if __name__=='__main__':
    from reader import Reader
    r = Reader('test.csv')
    cs = r.filter_courses('Grads 2012 Fall')
    table = CourseTable(cs)
