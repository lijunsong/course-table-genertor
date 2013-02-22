#!/usr/bin/env python
# encoding: utf-8

# 这个文件用于记录课程要求的条件
# 这个文件可以开放给用户编辑，或者是使用代码生成


# 定义时间段，上午，下午，晚上
p1 = [0,1,2,3,4]
p2 = [5,6,7,8,9]
p3 = [10, 11, 12]

# 某门课想要在某段时间上
# ID -> 时间 id 列表（从 0 开始)
COURSE_PREFER_TIME = {
                      }

# 某门课像要在某一天上
# id -> 日期 id 列表(从 0 开始）
COURSE_PREFER_DAY = {
                     }

# 教师想要在某段时间上课的要求可以转化为课程
# 对时间的要求
TEACHER_PREFERENCE = {
    # 'hr' : [Request(3, [5,6]),
    #         Request(2, p1)
    #         ],
    # 'crh' : request_list([0,1], [0,1,2,3,4]),
    
}

TEACHER_PREFER_DAY = {
    'crh' : [0, 1],
    'hxy' : [0,1,4],
    'dll' : [2,3,4],
    'dxs' : [0,1,2,3],
    'qy'  : [0,1,2],
    'yxq' : [0,1,2,3],
    'mew' : [0],
    'zxj' : [0,1,2,5],
    'fds' : [0, 2],
}

TEACHER_PREFER_TIME = {
    'crh' : [0,1,2,3,4],
    'zt' : p1 + p2,
    'hxy' : p1 + p2,
    'xl' : [1,2,3,4] + p2 + p3,
    'dll' : [2,3,4,5,6],
    'cxn' : p1 + p2,
    'hr' : [5,6],
    'ygl' : [2,3,4] + p2 + p3,
    'fds' : [0,1],
}
