#!/usr/bin/env python
# encoding: utf-8

import utils
import debug

d = debug.Debug('course')

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
        """
        self.cid = cid
        self.name = name
        self.credit = int(credit)
        self.groups = groups
        self.teachers = teachers
        #将 week, time 转化为二维数组的坐标[time, week]
        self.start_time = utils.to_pos(week, time)
        # 每门课的特殊要求（要求安排在周几，第几节课）
        self.preference = []

    def __str__(self):
        return "Name: %s, Teachers: %s, Groups: %s" % (self.name,
                                                       self.teachers,
                                                       self.groups)
    def need_allocate_p(self):
        return self.start_time == None

    def conflict_pref_day_p(self, day):
        """判断给定的天数是否会和自己的 preference 冲突"""
        d.p('判断day %d 是否符合 %s 的偏好?' % (day, self.name))
        d.p([p.day for p in self.preference])

        conflict = True
        if self.preference != []:
            for p in self.preference:
                if p.day == day:
                    conflict = False
                    break
        else:
            d.p('不冲突')
            return False

        d.p('冲突？%s' % conflict)
        return conflict

    def conflict_pref_time_p(self, time):
        """判断给的时间是否会和自己的 preference 冲突"""
        d.p('判断time %d 是否符合 %s 的偏好?' % (time, self.name))
        d.p([p.time for p in self.preference])

        conflict = True
        if self.preference != []:
            for p in self.preference:
                if time in p.time:
                    conflict = False
                    break
        else:
            d.p('不冲突')
            return False

        d.p('冲突？%s' % conflict)
        return conflict

    def has_preference_p(self):
        return self.preference != []
