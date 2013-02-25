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
        # preference 为空意味着没有偏好
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
        if self.preference == []:
            d.p('无偏好，不冲突')
            return False

        prefs_days = [p.day for p in self.preference]
        d.p('偏好是：%s' % prefs_days)
        if day in prefs_days:
            d.p('不冲突')
            return False
        else:
            d.p('冲突')
            return True

    def conflict_pref_time_p(self, day, time):
        """判断给的时间是否会和自己的 preference 冲突"""
        d.p('判断time %d 是否符合 %s 的偏好?' % (time, self.name))

        if self.preference == []:
            d.p('本课程无偏好，不冲突')
            return False

        prefs_time = self.get_time_preference(day)
        if prefs_time == []:
            d.p('老师的preference中不包含这一天 %d，冲突' % day)
            return True
        d.p('偏好是：%s' % prefs_time)
        if time in prefs_time:
            d.p('不冲突')
            return False
        else:
            d.p('冲突')
            return True

    def has_day_preference_p(self):
        """针对天而言，判断老师周一到周五是否有特殊的偏好"""
        if self.preference == []:
            return False
        days = [p.day for p in self.preference]
        if set(days) == set([0,1,2,3,4]):
            return False
        else:
            return True

    def has_time_preference_p(self, day):
        "对于某天而言，判断这一天时间上有没有任何的 preference"
        if self.preference == []:
            return False

        pref = filter(lambda x: x.day == day, self.preference)
        if pref == []:
            return True #如果preference 里面没有 day 这一天，说明这一
                        #天不能排，意味着有 time preference
        else:
            time = pref[0].time
            if set(time) != set([0,1,2,3,4,5,6,7,8,9,10,11,12]):
                return True
            else:
                return False

    def has_preference_p(self):
        "判断这个课程是否有任何的 preference"
        if self.preference == []:
            return False

        if self.has_day_preference_p():
            return True
        for d in [0,1,2,3,4]:
            if self.has_time_preference_p(d):
                return True
        return False

    def get_time_preference(self, day):
        pref = filter(lambda x: x.day == day, self.preference)
        if pref == []:
            return []
        else:
            return pref[0].time
