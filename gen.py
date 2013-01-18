#!/usr/bin/env python
# encoding: utf-8

import configure as cfg
import debug
import sys

d = debug.Debug('gen')

class Generator:
    """排课程的类

    Attributes:
        course_pool -- 课程池，提供对课程的各种操作
        determined  -- 已经预置的课程
        sorted_determined -- 没有预置，但按照老师的各种要求排过序的课程
    """
    ## 主要方法 ##
    def gen(self):
        # 先放预置的课程
        for course in self.determined:
            tables = self.course_to_table(course.cid)
            self._set_on_table(tables, course.start_time, course.cid)

        for course in self.sorted_undetermined:
            self.set_course(course.cid)

    def print_coursetables(self):
        print self.get_detail_tables_str()

    #-----------辅助方法------------
    def __init__(self, course_pool):
        self.course_pool = course_pool
        self.determined = course_pool.get_determined()
        self.sorted_undetermined = course_pool.get_sorted_undetermined()

    def set_course(self, courseid):
        "在相应的课表上找最佳位置摆放"
        # 1. 得到与之相关的所有课表
        tables = self.course_to_table(courseid)
        course = self.id_to_course(courseid)

        # 2. 在相关的几个课表上，找到一个 *都空着的* *最佳* 位置
        pos = self.get_course_pos(tables, courseid)
        # 3. 放到这个位置上
        d.p('课程 %s 放在这里\n%s' % (self.id_to_course(courseid),
                                      pos))
        self._set_on_table(tables, pos, courseid)
        d.p('当前课程表:\n%s' % self.get_detail_tables_str())

    def get_course_pos(self, tables, courseid):
        """
        确定位置：
        1. 首先几个课表有的满，有的空。先从满的开始找位置（如果比较
        满的课表找不到位置，就肯定找不到位置了）
        2. 找到了最满的课表，开始找一个最佳位置
        """
        d.p('准备设置课程 %s' % self.id_to_course(courseid))
        # 找课程最多的课表
        fullest_table = self.find_max_course_num(tables)
        # 得到这张表上每天上课数量
        course_num_dict = self.get_eachday_course(fullest_table)
        d.p('每天上课数量 %s' % course_num_dict.values())
        # 在这些天里面找出一天，查看是否有冲突
        while len(course_num_dict) != 0:
            # 找到课程最少的一天
            day = min(course_num_dict, key = course_num_dict.get)
            d.p('试试星期 %s' % day)
            # 先查看这一天有没有问题
            if self._conflict_day_p(tables, day, courseid):
                d.p('day有冲突，不能排星期 %s' % day)
                del course_num_dict[day]
                continue

            # 返回那一天最好的几个位置
            times = self._get_poses_on_day(fullest_table, day,
                                           courseid)
            time = -1
            for t in times: # 在位置里面依次查找符合条件的值
                if self._conflict_pos_p(tables, (t, day), courseid):
                    d.p('pos有冲突，不能放在星期 %s 的位置 %s' % (day, t))
                else: # 能放，找到位置了
                    d.p('能放在星期 %s 的位置 %s)' % (day, t))
                    time = t
                    break
            if time == -1:
                del course_num_dict[day]
                continue
            else:
                d.p('试试星期 %s 的位置 %s' % (day, time))
                break
        else:
            d.p('找不到位置:\n%s' %
                self.course_pool.get_detail_tables())
            sys.exit('')

        return (time, day)

    def _set_on_table(self, tables, pos, courseid):
        assert(pos[0] != -1)
        course = self.id_to_course(courseid)
        for table in tables:
            table.set(course, pos)

    def _conflict_pos_p(self, tables, pos, courseid):
        time, day = pos
        # 如果在这一天找不到一个合适的位置，
        if time == -1:
            return True

        # 检查这个位置是否符合特殊要求
        d.p('pos: 检查课程 %s 的特殊要求' % courseid)
        if courseid in cfg.COURSE_PREFER_TIME:
            d.p('[haha]')
            if time not in cfg.COURSE_PREFER_TIME[courseid]:
                d.p('不符合')
                return True
        else:
            d.p('oh')

        credit = self.course_pool.id_to_course(courseid).credit
        # 再看看其他课表这个时间段是不是可以放下这门课
        for table in tables:
            for t in xrange(time, time+credit):
                if table.table[t][day] != -1: # 有课
                    return True

        return False

    def _conflict_day_p(self, tables, day, courseid):
        """查看 courseid 这门课能不能在 day
        这一天设置在指定的 tables 里面
        NOTE: 这里不判断有没有位置放，有没有位置是之后的事情
        """
        d.p('day: 检查课程 %s 的特殊要求' % courseid)
        # 查看这一天符不符合特殊要求
        if courseid in cfg.COURSE_PREFER_DAY:
            if day not in cfg.COURSE_PREFER_DAY[courseid]:
                d.p('不符合')
                return True

        for table in tables:
            if self._conflict_day_p_help(table, day, courseid):
                return False

    def _conflict_day_p_help(self, table, day, courseid):
        "辅助方法，针对一个 table 判断 day 能不能放置 courseid"
        course_list = zip(*table.table)[day]
        for c in course_list:
            if c == -1:
                continue
            # 判断当前table中是否有courseid的老师的课了
            if self._conflict_teacher_p(c, courseid):
                return True
        # 到这里说明没有冲突
        return False

    def _conflict_teacher_p(self, cid1, cid2):
        if cid1 == cid2:
            return True
        t1 = set(self.course_pool.id_to_course(cid1).teachers)
        t2 = set(self.course_pool.id_to_course(cid2).teachers)
        if t1.isdisjoint(t2): #没有交集
            return False
        else:
            return True

    def _get_poses_on_day(self, table, day, courseid):
        """根据当前课表和给定的星期，得出当天能够摆放的所有位置
        最好的位置在最前面

        Arguments:
            table -- 当前的 CourseTable
            day   -- 要计算哪一天的位置
           course -- 课程 id
        Return:
            CourseTable * int * int => (listof int)
        """

        # 得到上午、下午、晚上各可以放置该课程的时间
        # TODO: 先计算出 course_list 然后传递到set里面加快速度
        beforenoon_start, before_p = \
          self._set_period(table, courseid,
                           day, 0, cfg.beforenoon_num)

        afternoon_start, after_p = \
          self._set_period(table, courseid,
                           day, cfg.beforenoon_num, cfg.afternoon_num)

        night_start, night_p = \
          self._set_period(table, courseid,
                           day, cfg.afternoon_num, cfg.time_num)

        d.p('上午可以开始放的位置：', beforenoon_start, '有其他课？', before_p)
        d.p('下午可以开始放的位置：', afternoon_start, '有其他课？', after_p)
        d.p('晚上可以开始放的位置：', night_start, '有其他课？', night_p)

        # 准备返回结果：这里比较复杂
        # 直接写 if 的话，需要写很多很多很多if才能判断完全：
        #    如果上午，下午，晚上都有课，如果上午可以放，就放上午，如果下午可以放，就放下午……
        #    如果三个时间段哪个没有课，就返回那一个的位置
        #    如果有两个没有课，依次从上午开始判断……
        #    如果都没有课，返回上午的位置
        # 更简单的办法如下
        result = {True : [], False : []}
        # 按顺序放入
        result[before_p].append(beforenoon_start)
        result[after_p].append(afternoon_start)
        result[night_p].append(night_start)

        res = []  # 返回值放到这里
        # 如果存在有几个时间段没有其他的课
        res.extend(result[False])
        # 有课的时间段
        pos_list = result[True]
        # 取第一个不是-1的数字
        for i in pos_list:
            if i != -1:
                res.append(i)
        return res
    def _set_period(self, table, courseid, day, start, end):
        """测试 courseid 的课能不能在 table 的晚上放置
        Arguments:
               table -- CourseTable
            courseid -- 课程 id
                 day -- 放置在哪一天
               start -- 从哪个位置开始放
                 end -- 到哪个位置结束(exclusive)
        Return:
            CourseTable * int * int => (tupleof int boolean)
            如果能放置，返回 (可以放置的起始位置, 是否有其他课程)
            否则返回 (None, 是否有其他课程)
        """
        course_list = zip(*table.table)[day]
        credit = self.id_to_course(courseid).credit
        has_other_p = False
        pos = start
        while pos + credit - 1 < end:
            d.p('检查位置 %s' % pos)
            if course_list[pos] != -1: # 有课
                has_other_p = True
                d.p('位置 %s 有课' % pos)
                pos += 1
            else: # 没课
                if self._empty_period(pos, credit, course_list):
                    d.p('位置 %s 可以使用' % pos)
                    break
                else: # 一旦和另外一门课位置交叉了，直接跳到交叉位置
                    pos += 1
        else:
            pos = -1
            d.p('剩下的空表不足以排课了，退出')

        return (pos, has_other_p)

    def _empty_period(self, start_timeid, length, course_list):
        """检查从 start_timeid 开始的长度为 length 的 course_list 里面是否为空

        NOTE： 此函数不会检查溢出

        Arguments:

        Return:
            int * int * (listof int) => boolean
            如果这个区间为空，返回 True
            否则返回 False
        """
        for c in course_list[start_timeid:start_timeid + length]:
            if c != -1: # 有课
                return False
        return True
    #-----------对 course_pool 进行包装 -----------------
    def course_to_table(self, courseid):
        return self.course_pool.course_to_table(courseid)
    def id_to_course(self, courseid):
        return self.course_pool.id_to_course(courseid)

    def find_max_course_num(self, tables):
        return self.course_pool.find_max_course_num(tables)
    def get_eachday_course(self, table):
        """这张课程表上每天都上了多少节课
        Return: 星期与对应的课程数
           (dictof int int)
        """
        d = {}
        e = self.course_pool.get_eachday_course(table)
        for i, e in enumerate(e):
            d[i] = e
        return d

    def get_detail_tables_str(self):
        return self.course_pool.get_detail_tables()

if __name__=='__main__':
    from reader import Reader
    from course_table import CourseTable
    from course_pool import CoursePool

    reader = Reader('test.csv')
    course_pool = CoursePool(reader.courses)

    generator = Generator(course_pool)

    generator.gen()

    generator.print_coursetables()
