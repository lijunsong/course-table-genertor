#!/usr/bin/env python
# encoding: utf-8

import configure as cfg
import sys

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
        if not self._same_group_p(all_courses):
            sys.exit("[2]construct course table error")

        self.all_courses = all_courses
        self.title = all_courses[0].group
        self.table = [[-1 for i in cfg.DAY] for j in cfg.TIME]
        self.unallocs = []
        self.id_course_dict = {} #专门用于从 id 查询 course 的字典

        # 先摆放预置的课程
        self._init_table_and_course()

        # TODO: 对需要之后分配的课程进行排序
        self._sort_course()

    def _init_table_and_course(self):
        """对那些预置的课程
          - 将它们依次先放到二维表中
          - 同时得到之后需要分配的课程放到 unallocs 里面
          - 同时得到 id->course 的字典"""
        for c in self.all_courses:
            self.id_course_dict[c.cid] = c
            if not c.need_allocate_p():
                self.set(c, c.start_time)
            else:
                self.unallocs.append(c)

    def _sort_course(self):
        """对接下来要进行排课的课程（见unallocs变量）进行排序
        总的来说，是先排有要求的课，再排没有要求的课。
        
        对于有要求的课
        1. 上同一门课的班级越多，这门课最靠前（因为涉及到了不同的课表）
        2. 一门课老师要求越多（比如除了每天时间限制之外，还有星期的限制），越靠前
        3. 对于有相同多要求的，要求范围越窄越靠前
        """
        # 找到
        pass
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

    def eachday_course(self):
        """计算每一天上课的总课程数量
        NOTE：这里是每一个学分一节课，所以这里实际也计算了总的学分数量

        Return: 星期 * 学分的字典
             => (dictof int int)
        """
        lst = zip(*table.table)
        # 过滤出不是 -1 的课
        course_filter = lambda x: x!=-1
        lst2 = map(lambda x: filter(course_filter, x), lst)

        # 构造返回的 星期*学分的字典
        res = {}
        for i, v in enumerate(lst2):
            res[i] = len(v)
        return res

    def conflict_teacher_p(self, courseid, day):
        """判断某课如果安排在某天是否会有教师冲突
        Arguments:
            self-explaination
        Return:
            int * int => boolean
        """
        course_list = zip(*self.table)[day]
        teachers = set(self.id_to_course(courseid).teachers)
        for c in course_list:
            if c != -1:
                ts_set = set(self.id_to_course(c).teachers)
                if not teachers.isdisjoint(ts_set):
                    return True
        return False

    def conflict_course_p(self, course, day):
        """检查 course 如果安排在 day 这一天是否冲突
        
        TODO: 检查是否需要

        Arguments:
            self-explaination
        Return:
            int * int => boolean
        """
        pass

    def _same_group_p(self, courses):
        """所有的课程只能是同一个年级的课程

        Return
            (listof Courses) => boolean
        """
        groups = set([c.group for c in courses])
        return len(groups) == 1

    def id_to_course(self, id):
        """返回ID是 id 的课程

        Arguments:
            id -- 课程 id
        Return:
            int => Course
        """
        return self.id_course_dict[id]

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
                    s += (self.id_to_course(cid).name+"_"*15)[:15]
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
