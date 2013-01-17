#!/usr/bin/env python
# encoding: utf-8

# 这个文件用于记录教师要求的条件
# 这个文件可以开放给用户编辑，或者是使用代码生成

# 某门课想要在某段时间上
# ID -> 时间 id 列表（从 0 开始)
COURSE_PREFER_TIME = {
    13 : [5, 6, 7, 8, 9]
                      }

# 某门课像要在某一天上
# id -> 日期 id 列表(从 0 开始）
COURSE_PREFER_DAY = {
                     }

# 教师想要在某段时间上课
# 教师名字 -> 时间 id 列表（从 0 开始)
TEACHER_PREFER_TIME = {}

# 教师想要在某几天上课 
# 教师名字 -> 日期 id 列表(从 0 开始）
TEACHER_PREFER_DAY = {}

