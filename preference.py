#!/usr/bin/env python
# encoding: utf-8

p1 = [0,1,2,3,4]
p2 = [5,6,7,8,9]
p3 = [10, 11, 12]

class Pref:
    def __init__(self, day, time):
        """每门课排课时候的要求。TODO:是否可以把start_time归到这里里面？

        Attributes:
            time: 时间, (listof int), 从 0 开始
            day : 周数，int， 从 0 开始
        """
        self.day = day
        self.time = time
        assert(type(day) == int)
        assert(type(time) == list)
    def __str__(self):
        return "day:%s, time:%s" % (self.day, self.time)

def prefs(days=[0,1,2,3,4], time=p1+p2+p3):
    """用于指定了在哪几天的哪几个时间段
    Argument:
       days: 排课要求排在哪几天
       time: 排课要求排在这几天的哪些时间里面
    Return: (listof int) * (listof int) => (listof Pref)
    示例：
      - 周一和周三的上午： prefs(days=[0,2], time=p1)
      - 周一和周三： prefs(days=[0,2])
      - 周一至周五的上午: prefs(time=p1)
    """
    return [Pref(d, time) for d in days]

def compact(day):
    "老师想在day天内上完所有课程"
    return day

def prefs_notin(days=[], time=[]):
    """如果条件是“不在哪几天的哪几个时间”，则用这个函数

    Arguments:
        days: 不排在哪几天
        time: 不排在这几个时间段
    Return:
        (listof int) * (listof int) => (listof Pref)

    示例：
      - 不在周二和周三的下午： prefs_notin([1,2],p2)
    """
    total_days = [0,1,2,3,4]
    total_time = p1 + p2 + p3

    result = []
    if time == []:
        for d in filter(lambda x: x not in days,
                        total_days):
            result.append(Pref(d, total_time))
        return result


    if days == []:
        preftime = filter(lambda x: x not in time,
                          total_time)

        for d in total_days:
            result.append(Pref(d,preftime))
        return result

    if time != [] and days != []:
        preftime = filter(lambda x: x not in time,
                          total_time)
        for d in total_days:
            if d in days:
                result.append(Pref(d, preftime))
            else:
                result.append(Pref(d, total_time))
        return result

def prefs_notin_special(day, time, *other):
    """用于指定不在某一天的某个时刻，参数可以是任意偶数多个
    Argument:
        day: 不排在哪一天
        time: 不排在那一天的某个时刻
        other: day 和 time 的重复
    Return:
        int * (listof int) * ... => (listof Pref)

    示例：
      - 不在周三的下午和周四的晚上： prefs_notin_specially(2,p2,3,p3)
    """
    assert(len(other) % 2 == 0)
    total_time = p1+p2+p3
    total_days = [0,1,2,3,4]

    not_dict = {day: time}
    for i in range(0,len(other),2):
        not_dict[other[i]] = other[i+1]
    result = []
    for d in total_days:
        if d in not_dict:
            ts = filter(lambda x: x not in not_dict[d], total_time)
            result.append(Pref(d, ts))
        else:
            result.append(Pref(d, total_time))
    return result

def prefs_special(day, time, *other):
    """用于指定某一天的某个时刻，参数可以是任意偶数多个
    Arguments:
        day: 在某一天
        time: 在那一天的某个时间段
        other: day 和 time 的重复
    Return:
        int * (listof int) * ... => (listof Pref)

    示例：
      - 在周二上午和周三下午：prefs_special(1,p1,2,p2)
    """
    assert(len(other) % 2 == 0)
    total_time = p1 + p2 + p3
    total_days = [0,1,2,3,4]
    in_dict = {day: time}
    for i in range(0, len(other), 2):
        in_dict[other[i]] = other[i+1]
    result = []
    for d in in_dict:
        result.append(Pref(d, in_dict[d]))
    return result
