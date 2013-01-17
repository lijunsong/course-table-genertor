#!/usr/bin/env python
# encoding: utf-8

import configure as cfg
import sys

def to_standard_time(time):
    """将一般的时间表示转化为 xx:xx 形式 """
    # TODO: optimize
    s = time.split(":")
    if len(s[0]) == 1: s[0] = "0" + s[0]
    if len(s[1]) == 1: s[1] = "0" + s[1]
    return ":".join(s)

def to_pos(week, time):
    """将 week 和 time 转为数字表示的 [time, week]

    NOTE: time 可以是 xx:xx，也可以是 xx:xx-xx:xx

    string * string => (listof int)
    """
    if week == '' or time == '':
        return None
    # 如果格式是 xx:xx-xx:xx， 时间取第一个
    if '-' in time:
        standard_t = to_standard_time(time.split('-')[0])
    else:
        standard_t = to_standard_time(time)
    standard_w = week.capitalize()[:3]
    week_pos = -1
    time_pos = -1

    for i, v in enumerate(cfg.DAY):
        if standard_w in v:
            week_pos = i
            break
    if week_pos == -1:
        sys.exit("Error: week %s is not legal" % week)

    for i, v in enumerate(cfg.TIME):
        if standard_t in v:
            time_pos = i
            break
    if time_pos == -1:
        sys.exit("Error: time %s is not legal" % time)

    return (time_pos, week_pos)
