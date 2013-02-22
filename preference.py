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
    """
    return [Pref(d, time) for d in days]

def prefs_notin(days=[], time=[]):
    """用于得到不在哪几天的哪几个时间
    Arguments:
        days: 不排在哪几天
        time: 不排在这几个时间段
    Return:
        (listof int) * (listof int) => (listof Pref)
    """
    total_days = [0,1,2,3,4]
    total_time = p1 + p2 + p3

    preftime = filter(lambda x: x not in time,
                      total_time)

    result = []
    for d in total_days:
        if d in days:
            result.append(Pref(d,preftime))
        else:
            result.append(Pref(d,total_time))
    return result

def prefs_notin_specially(day, time, *other):
    """用于指定不在某一天的某个时刻，参数可以是任意偶数多个
    Argument:
        day: 不排在哪一天
        time: 不排在那一天的某个时刻
        other: day 和 time 的重复
    Return:
        int * (listof int) * ... => (listof Pref)
    """
    d = {day: time}
    for i in range(0,len(other),2):
        d[other[i]] = other[i+1]
        #TODO HERE
    total_days = [0,1,2,3,4]
    total_time = p1 + p2 + p3

    ts = [t for t in total_time if t not in time]
    result = []
    for d in total_days:
        if d == day:
            result.append(Pref(d, ts))
        else:
            result.append(Pref(d, total_time))
    if len(other) != 0:
        print other
        result.extend(prefs_notin_specially(other[0],
                                            other[1],
                                            *other[2:]))
    return result
