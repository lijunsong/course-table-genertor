#!/usr/bin/env python
# encoding: utf-8

import configure as cfg
import debug
import sys

d = debug.Debug('generator')

class Generator:
    """排课程的类

    Attributes:
        tables -- 所有的初始化过的课程表
    """
    def __init__(self, tables):
        self.tables = tables
        self.total = len(tables)

    def get_course_pos(self, table, courseid):
        """根据现有情况，得到下一门课安排在什么地方

        1. 选择课少的一天
        2. 上下午时间尽量均匀
        3. 同一个老师尽量不在一天上课
        NOTE:
          排上午，就从上午第一节没课的地方开始排
          排下午，就从下午第一节没课的地方开始排

        Arguments:
            table -- CourseTable
           courseid -- 要安排哪一门课

        Return
            CourseTable * int => (tupleof int int)
        """
        tab = table.table
        course_num_dict = {}
        # 得到每天上课数量 *有同一老师的，数量+1000*
        for day in xrange(cfg.day_num):
            course_num_dict[day] = 0
            if table.conflict_teacher_p(courseid, day):
                course_num_dict[day] += 1000
                continue
            for time in xrange(cfg.time_num):
                if tab[time][day] != -1:
                    course_num_dict[day] += 1
                    
        d.p('目前各天课程数量：', course_num_dict.values())
        # 得到上下午
        while len(course_num_dict) != 0:
            day = min(course_num_dict, key=course_num_dict.get)
            d.p('选择星期 %s' % (day+1))
            # 安排在上午还是下午？
            time = self._get_pos_on_day(table, day, courseid)
            d.p('星期 %s 的位置是是 %s' % (day+1, time))
            if time == -1:
                del course_num_dict[day]
            else:
                break
        d.p('得到了课程应该放在', time, day)
        return (time, day)

    def _beforenoon_p(self, timeid):
        """看所给的 time id 是不是上午
        
        Argument:
            timeid -- 提供的时间，int
        Return:
            int => boolean
        """
        return timeid < cfg.beforenoon_num
 
    def _afternoon_p(self, timeid):
        """看所给的 time id 是不是下午
        
        Argument:
            timeid -- 提供的时间，int
        Return:
            int => boolean
        """
        return timeid >= cfg.beforenoon_num
    
    def _empty_period(self, start_timeid, length, course_list):
        """检查从 start_timeid 开始的长度为 length 的 course_list 里面是否为空
        
        NOTE： 此函数不会检查溢出
        
        Arguments:
        
        Return:
            int * int * (listof int) => boolean
            如果这个区间为空，返回 True
            否则返回 False
        """
        d.p('检查 ', course_list[start_timeid:start_timeid + length])
        for c in course_list[start_timeid:start_timeid + length]:
            if c != -1: # 有课
                return False
        return True
            
    def _set_beforenoon(self, table, courseid, day):
        """测试 courseid 的课能不能在 table 的上午放置
        并且测试上午有没有其他课程
        
        Arguments:
               table -- CourseTable 
            courseid -- 课程 id
                 day -- 放置在哪一天
        Return:
            CourseTable * int * int => (tupleof int boolean)
            
            如果能放置，返回 (可以放置的起始位置, 是否有其他课程)
            否则返回 (None, 是否有其他课程)
        """
        
        course_list = zip(*table.table)[day]
        credit = table.id_to_course(courseid).credit
        has_other_p = False
        pos = 0
        # TODO: 每次都检查pos+1效率不高
        while pos + credit - 1 < cfg.beforenoon_num:
            d.p('上午检查位置 %s' % pos)
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
            d.p('上午剩下的空表不足以排课了，退出上午')
                    
        return (pos, has_other_p)
    
    def _set_afternoon(self, table, courseid, day):
        """测试 courseid 的课能不能在 table 的下午放置
        Arguments:
               table -- CourseTable 
            courseid -- 课程 id
                 day -- 放置在哪一天
        Return:
            CourseTable * int * int => (tupleof int boolean)
            如果能放置，返回 (可以放置的起始位置, 是否有其他课程)
            否则返回 (None, 是否有其他课程)
        """
        course_list = zip(*table.table)[day]
        credit = table.id_to_course(courseid).credit
        has_other_p = False
        pos = cfg.beforenoon_num
        while pos + credit - 1 < cfg.afternoon_num:
            d.p('下午检查位置 %s' % pos)
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
            d.p('下午剩下的空表不足以排课了，退出下午')

        return (pos, has_other_p)
    
    def _set_night(self, table, courseid, day):
        """测试 courseid 的课能不能在 table 的晚上放置
        Arguments:
               table -- CourseTable 
            courseid -- 课程 id
                 day -- 放置在哪一天
        Return:
            CourseTable * int * int => (tupleof int boolean)
            如果能放置，返回 (可以放置的起始位置, 是否有其他课程)
            否则返回 (None, 是否有其他课程)
        """
        course_list = zip(*table.table)[day]
        credit = table.id_to_course(courseid).credit
        has_other_p = False
        pos = cfg.afternoon_num
        while pos + credit - 1 < cfg.time_num:
            d.p('晚上检查位置 %s' % pos)
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
            d.p('晚上剩下的空表不足以排课了，退出晚上')

        return (pos, has_other_p)
    
    def _get_pos_on_day(self, table, day, courseid):
        """根据当前课表和给定的星期，得出当天最好的一个位置

        Arguments:
            table -- 当前的 CourseTable
            day   -- 要计算哪一天的位置
           course -- 课程 id
        Return:
            CourseTable * int * int => int
        """
        
        # 得到上午、下午、晚上各可以放置该课程的时间
        # TODO: 先计算出 course_list 然后传递到set里面加快速度
        beforenoon_start, before_p = self._set_beforenoon(table, courseid, day)
        afternoon_start, after_p = self._set_afternoon(table, courseid, day)
        night_start, night_p = self._set_night(table, courseid, day)
        d.p('上午可以开始放的位置：', beforenoon_start, '有其他课？', before_p)
        d.p('下午可以开始放的位置：', afternoon_start, '有其他课？', after_p)
        d.p('晚上可以开始放的位置：', night_start, '有其他课？', after_p)
        
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
        
        if len(result[False]) != 0: # 如果存在有几个时间段没有其他的课
            return result[False][0] # 返回第0个（并且这个肯定不是 -1
        else:
            pos_list = result[True]
            res = -1
            # 取第一个不是-1的数字,如果都是-1就返回-1
            for i in pos_list:
                if i != -1:
                    res = i 
                    break
            return res

    def generate(self):
        """排课主程序。只需要找到一个解

        Return:
            => (listof CourseTable)
        """
        # 遍历试一试
        for table in self.tables:
            for course in table.unallocs:
                d.p('准备放置课程： %s [teachers:%s]' % (course.name, course.teachers))
                pos = self.get_course_pos(table, course.cid)
                d.p(' 位置 ',  pos)
                if pos[0] != -1:
                    table.set(course, pos)
                else:
                    err_msg = []
                    err_msg.append('----------------------ERROR-------------------\n')
                    err_msg.append("当前正在放置的课程是: %s [credit: %s; teachers: %s]\n" % (course.name, course.credit, course.teachers))
                    err_msg.append("当前的课表是:\n")
                    err_msg.append(table.pretty_str())
                    err_msg.append('\n 放置失败！\n' )
                    sys.exit("".join(err_msg))
                    
                
                d.p(table.pretty_str())

        return self.tables

if __name__=='__main__':
    from reader import Reader
    from course_table import CourseTable
    reader = Reader('test.csv')

    #得到年级与相应课程的映射
    grad_course = reader.get_groups_courses()

    # 初始化课程表
    tables = []
    for k in grad_course:
        tables.append(CourseTable(grad_course[k]))

    # d
    #for table in tables:
    #    print table.pretty_str()
    # 初始化生成器
    generator = Generator([tables[0]])

    new_tables = generator.generate()
    
    print new_tables[0].pretty_str()
