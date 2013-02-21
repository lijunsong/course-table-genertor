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
# TODO: 这里需要保证所有的 courseid 是 str 类型的a
COURSE_PREFER_TIME = request.COURSE_PREFER_TIME

COURSE_PREFER_DAY = request.COURSE_PREFER_DAY

# 教师名字在这里变为大写
TEACHER_PREFER_TIME = {}
for name in request.TEACHER_PREFER_TIME:
    TEACHER_PREFER_TIME[name.upper()] = request.TEACHER_PREFER_TIME[name]

TEACHER_PREFER_DAY = {}
for name in request.TEACHER_PREFER_DAY:
    TEACHER_PREFER_DAY[name.upper()] = request.TEACHER_PREFER_DAY[name]

## 以下内容不能修改！
## 用于程序中的辅助变量
##

# 时间列表
TIME = BEFORENOON + AFTERNOON + NIGHT

day_num = len(DAY)
time_num = len(TIME)
beforenoon_num = len(BEFORENOON)
afternoon_num = beforenoon_num + len(AFTERNOON)

special_cid = list(set(COURSE_PREFER_TIME.keys() +
                       COURSE_PREFER_DAY.keys()))
special_teachers = list(set(TEACHER_PREFER_TIME.keys() +
                            TEACHER_PREFER_DAY.keys()))
