#!/usr/bin/env python
# encoding: utf-8

import utils

class Course:
    def __init__(self, cid, name, credit, groups, teachers, week, time):
        """课程

        Attributes:
                cid -- 每个课程有唯一的一个 id
               name -- 课程名字
             credit -- 学分
              group -- 用于年级名称或者班的名称
           teachers -- 这门课的老师，可能多个
         start_time -- 这门课的上课时间。
                       如果没有预置上课，这里是 None
                       如果预置上课时间，是(时间，星期)的 tuple
              share -- 上这门课的班级的列表
        """
        self.cid = cid
        self.name = name
        self.credit = int(credit)
        self.groups = groups
        self.teachers = teachers
        #将 week, time 转化为二维数组的坐标[time, week]
        self.start_time = utils.to_pos(week, time)

    def __str__(self):
        return self.name

    def need_allocate_p(self):
        return self.start_time == None
