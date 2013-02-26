#!/usr/bin/env python
# encoding: utf-8

import request

# 课程表基本信息与教师条件
BEFORENOON = ["08:00-08:50",
           "09:00-09:50",
           "10:10-11:00",
           "11:10-12:00",
           "12:10-13:00"]

AFTERNOON = [ "13:00-13:50",
              "14:00-14:50",
              "15:00-15:50",
              "16:10-17:00",
              "17:10-18:00"]

NIGHT = ["18:30-19:20",
         "19:35-20:25",
         "20:40-21:30"]

DAY = ["Mon", "Tue", "Wed", "Thu", "Fri"]

# 以下两个都是 courseid -> (listof int) 的字典
# TODO: 这里需要保证所有的 courseid 是 str 类型的
COURSE_PREFERENCE = {}
for cid in request.COURSE_PREFERENCE:
    COURSE_PREFERENCE[cid.upper()] = request.COURSE_PREFERENCE[cid]

# 教师名字在这里变为大写
TEACHER_PREFERENCE = {}
for name in request.TEACHER_PREFERENCE:
    TEACHER_PREFERENCE[name.upper()] = request.TEACHER_PREFERENCE[name]

## 以下内容不能修改！
## 用于程序中的辅助变量
##

# 时间列表
TIME = BEFORENOON + AFTERNOON + NIGHT

day_num = len(DAY)
time_num = len(TIME)
beforenoon_num = len(BEFORENOON)
afternoon_num = beforenoon_num + len(AFTERNOON)
