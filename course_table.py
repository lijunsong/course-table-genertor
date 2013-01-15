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
        if not self._same_grade_p(all_courses):
            sys.exit("[2]construct course table error")

        self.all_courses = all_courses
        self.title = all_courses[0].grade
        self.table = [[-1 for i in cfg.DAY] for j in cfg.TIME]
        self.unallocs = []

        # 先摆放预置的课程
        self._init_table()

        # TODO: 对需要之后分配的课程进行排序
        

    def _init_table(self):
        "对那些预置的课程，将它们依次先放到二维表中"
        for c in self.all_courses:
            if not c.need_allocate_p():
                self.set(c, c.start_time)
            else:
                self.unallocs.append(c)

    def set(self, course, pos):
        """摆放课程的ID在课表上

        NOTE:
            需要根据学分来判断摆放几个位置

        Arguments:
            course -- 要被摆放的课程
            pos    -- 要摆放的位置(时间，星期)
        """
        credit = course.credit
        i, j = pos
        for k in xrange(credit):
            self.table[i+k][j] = course.cid

    def _same_grade_p(self, courses):
        """所有的课程只能是同一个年级的课程

        Return
            (listof Courses) => boolean
        """
        grades = set([c.grade for c in courses])
        return len(grades) == 1

    def _id_to_course(self, id):
        """返回ID是 id 的课程

        Arguments:
            id -- 课程 id
        Return:
            int => Course
        """
        for c in self.all_courses:
            if id == c.cid:
                return c

    def pretty_str(self):
        "返回课程表具体内容"
        s = ""
        for i in xrange(len(cfg.TIME)):
            s += cfg.TIME[i] + ' '
            for j in range(len(cfg.DAY)):
                cid = self.table[i][j]
                if cid == -1:
                    s += '_'*15
                else:
                    s += (self._id_to_course(cid).name+"_"*15)[:15]
                s += '  '
            s += '\n'
        return s

    def __str__(self):
        "返回二维数组"
        res = []
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
