#!/usr/bin/env python
# encoding: utf-8

import utils

class Course:
    def __init__(self, cid, name, credit, grade, teachers, week, time):
        """course_info 对应
        cid, name, credit, grade, teachers, week, time
        """
        self.cid = cid
        self.name = name
        self.credit = credit
        self.grade_name = grade
        self.teachers = teachers
        #将 week, time 转化为二维数组的坐标[time, week]
        self.start_time = utils.to_pos(week, time)

    def __str__(self):
        return self.name

    def need_allocate_p(self):
        return self.start_time == None
