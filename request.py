#!/usr/bin/env python
# encoding: utf-8

# 这个文件用于记录课程要求的条件
# 这个文件可以开放给用户编辑，或者是使用代码生成
from preference import *

# 定义时间段，上午，下午，晚上
p1 = [0,1,2,3,4]
p2 = [5,6,7,8,9]
p3 = [10, 11, 12]

# 某门课想要在某时间上
# ID -> (listof preference)
# ID 是 string 类型的
COURSE_PREFERENCE = {
    'xfjjxzt' : prefs(days=[2], time=p3)
}

# 教师想要在某段时间上课的要求可以转化为课程
# 对时间的要求
TEACHER_PREFERENCE = {
    'crh' : prefs(days=[0,1], time=[0,1,2,3,4]),
    'hxy' : prefs(days=[0,1,4], time=p1+p2),
    'dll' : prefs(days=[2,3,4], time=[2,3,4,5,6]),
    'dxs' : prefs(days=[0,1,2,3], compact=1),
    'qy'  : prefs(days=[0,1,2]),
    'yxq' : prefs(days=[0,1,2,3]),
    'mew' : prefs(days=[0]),
    'zxj' : prefs_notin_special({4: [5,6]}),
    'ygl' : prefs_notin(time=[0,1]),
    'fds' : prefs(days=[0, 2]),
    'cxn' : prefs_notin(time=p3),
    'hr'  : prefs_special({3 : [5,6],
                           2 : p1}),
    'ysg' : prefs(time=[2,3,4,5,6,7]),
    'xl'  : prefs_notin(time=[0,1]),
    'yjc' : prefs(days=[0,1,3,4],time=[3,4]+p2+p3),
    'fj'  : prefs_notin(days=[2], time=p2+p3),

    'cxx' : prefs(time=p1, compact=3),
    'wq'  : prefs(days=[1,2], time=p1+p2),
    #'zxb' : 尽量安排在三天内
    'zxb' : prefs(time=p1+p2, compact=3),
    'lyl' : prefs_notin(days=[1]),
    'qyp' : prefs(days=[1,2], time=p1),
    'wy'  : prefs(time=[0,1]),
    'wjg' : prefs(time=[2,3,4,5,6,7], compact=3),
    'nw'  : prefs(days=[1,2,3,4], time=p1+p2, compact=3),
    'zl'  : prefs(time=p1),
    'cbc' : prefs(days=[1,3,4], time=[5,6]),
    'syw' : prefs_special({1 : p1+[5,6,7],
                           2 : p1+[5,6,7],
                           3 : p1+[5,6,7],
                           4 : [2,3,4,5,6,7]}),
    'lyh' : prefs_special({0 : [2,3,4] + p2,
                           2 : p1+p2,
                           3 : p1+p2}),
    'whx' : prefs(days=[0,2,4], time=p1),
    'lx'  : prefs(days=[1,2,3]),
    'pp'  : prefs(time=p1+p2),
    'sp'  : prefs(time=p1+p2),
    'wjg' : prefs(time=p1+p2),
    'hwy' : prefs(time=p1+p2),
}
