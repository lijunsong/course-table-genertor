#!/usr/bin/env python
# encoding: utf-8

import configure as cfg

class Generator:
    """排课程的类

    Attributes:
        tables -- 所有的初始化过的课程表
    """
    def __init__(self, tables):
        self.tables = tables
        self.total = len(tables)

    def get_course_pos(self, table, course):
        """根据现有情况，得到下一门课安排在什么地方

        1. 选择课少的一天
        2. 上下午时间尽量均匀
        3. 同一个老师尽量不在一天上课
        """
        credits_lst = self._compute_eachday_credits(table)
        return (1, 1)

    def _compute_eachday_credits(self, table):
        lst = zip(*table.table) # 每列分别作为一个list保存起来

        # 每一个 list 找出不为 -1 的数
        f = lambda x: x != -1
        lst2 = filter(f, lst)

        # TODO: 转换为 credit，目前先求课程数量
        # 对每个list再求长度
        res = (map len lst2)





    def generate(self):
        """排课主程序。只需要找到一个解

        Return:
            => (listof CourseTable)
        """
        # 遍历试一试
        for table in self.tables:
            for course in table.unallocs:
                pos = self.get_course_pos(table, course):
                table.set(course, pos)
        return self.tables
