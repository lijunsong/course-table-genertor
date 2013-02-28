#!/usr/bin/env python
# encoding: utf-8

# 课程池，用于处理各种有关课程的操作

import configure as cfg
from course_table import CourseTable
import debug
import pyh as pyh


d = debug.Debug('course_pool')

class CoursePool:
    #------ 对外接口 ------
    def id_to_course(self, courseid):
        return self._courseid_course_dict[courseid]

    def course_to_table(self, courseid):
        return self._courseid_table_dict[courseid]

    def find_max_course_num(self, tables):
        return max(tables, key=lambda x: x.get_course_num())

    def get_eachday_course(self, table):
        return table.eachday_course

    def get_teacher_courseids(self, t):
        return self._teacher_cid_dict[t]

    def get_sorted_undetermined(self):
        return self._sorted_undetermined

    def get_determined(self):
        return self._determined

    def get_detail_tables(self, tables):
        result = []
        for table in tables:
            result.append('GRUOP: %s' % table.title)
            result.append(self._table_detail(table.table))
        return '\n'.join(result)

    def write_HTML_tables(self, filename):
        """返回课表的HTML文本"""
        def _HTML_table_detail(num_table):
            t = pyh.table()
            for i in xrange(len(cfg.TIME)):
                tr = t << pyh.tr(style='border:1px solid;')
                tr << pyh.td(cfg.TIME[i])
                for j in range(len(cfg.DAY)):
                    cid = num_table[i][j]
                    if cid == -1:
                        tr << pyh.td(' ', style='border: 1px solid;')
                    else:
                        c = self.id_to_course(cid)
                        info = "%s[%s]" % (c.name,c.teachers[0])
                        tr << pyh.td(info, style='border: 1px solid;')
            return t

        page = pyh.PyH("course table")
        for table in sorted(self._tables, key=lambda x: x.title):
            page << pyh.h1('GROUP: %s' % table.title)
            page << _HTML_table_detail(table.table)
        page.printOut(filename)

    def teacher_has_course_on_p(self, teacher, day):
        """查看老师 teacher 在某一天 day 是否有课

        Arguement:
            teacher: str 的老师
            day: 查看 day 这一天是否有课
        Return:
            有课返回True；无课返回False
        """
        if teacher not in self._eachday_course_of_teacher:
            return False
        cd = self._eachday_course_of_teacher[teacher]
        if day >=0 and day <= 4 and cd[day] != 0: # 注意 day 可能超出范围
            return True
        else:
            return False

    def teacher_has_course_on_day_time_p(self, teacher, day, time):
        """查看老师 teacher 在某个时间段是否有课
        NOTE：这个方法将会针对所有的课表进行检查
        """
        for t in self._tables:
            cid = t.table[time][day]
            if cid == -1:
                continue
            else:
                course = self.id_to_course(cid)
                if teacher in course.teachers:
                    return True
        return False

    #----基本方法
    def __init__(self, all_courses):
        # 所有的课程
        self._all_courses = all_courses
        # 每个courseid对应的课程
        self._courseid_course_dict = self._get_courseid_course_dict()
        # 所有group的课程表
        self._tables = self._get_all_tables()
        # group 对应的课程表
        self._group_table_dict = self._get_group_table_dict()
        # 每个课程对应的课程表
        self._courseid_table_dict = self._get_courseid_table_dict()
        # 每个老师教的所有课程id
        self._teacher_cid_dict = self._get_teacher_cid_dict()
        # 每个老师教每天的课程数量
        self._eachday_course_of_teacher = {}
        # 预置的课程
        self._determined = self._get_determined()
        # 未预置的课程
        self._undetermined = self._get_undetermined()
        # 排好序的未预置的课程
        # 1. 首先设置教师与课程的特殊要求
        self._set_preference()
        # 2. 排序
        self._sorted_undetermined = self._sort_undetermined()

        d.p("排序之后：")
        for i in self._sorted_undetermined:
            d.p('===\n课程:%s\npreference' % i)
            for p in i.preference:
                d.p('%s' % p)
            d.p('factor:=%s' % i.factor)

    def _set_preference(self):
        """读取 TEACHER_PREFERENCE 和 COURSE_PREFERENCE 里面的条件，对每
        门课进行设置"""
        for t in cfg.TEACHER_PREFERENCE:
            for c in self._all_courses:
                if t in c.teachers:
                    #TODO: 可能引入bug：两个老师教一门课的时候，这个时候
                    #应该合并两个老师的条件。可将这个赋值改为course中的一个
                    #方法的调用，判断是否重复设定了这个课程的
                    #preference
                    c.set_prefs(cfg.TEACHER_PREFERENCE[t])
                    #c.preference = cfg.TEACHER_PREFERENCE[t]
        # 如果对某门课有特殊的 preference，
        # 应该覆盖掉老师的 preference
        for c in self._all_courses:
            if c.cid in cfg.COURSE_PREFERENCE:
                c.set_prefs(cfg.COURSE_PREFERENCE[c.cid])

        # 计算影响因子
        for c in self._all_courses:
            c.calc_factor()


    def _get_determined(self):
        dc = []
        for c in self._all_courses:
            if not c.need_allocate_p():
                dc.append(c)
        return dc

    def _get_undetermined(self):
        udc = []
        for c in self._all_courses:
            if c.need_allocate_p():
                udc.append(c)
        return udc

    def _sort_undetermined(self):
        """对所有的课程进行排序
        """

        return sorted(self._undetermined,
                      key=lambda x: x.factor)

    def _course_has_pref_p(self, courseid):
        if self.id_to_course(courseid).has_preference_p():
            return True
        else:
            return False

    def _get_teacher_cid_dict(self):
        tcd = {}
        for c in self._all_courses:
            for t in c.teachers:
                try:
                    if c.cid not in tcd[t]:
                        tcd[t].append(c.cid)
                except KeyError:
                    tcd[t] = [c.cid]
        return tcd

    def _get_courseid_course_dict(self):
        ccd = {}
        for c in self._all_courses:
            ccd[c.cid] = c
        return ccd

    def _get_group_table_dict(self):
        "每个 group 对应一个 table"
        gtd = {}
        for table in self._tables:
            gtd[table.title] = table
        return gtd

    def _get_all_groups(self):
        "得到所有的group名字"
        groups = []
        for c in self._all_courses:
            groups.extend(c.groups)
        return set(groups)

    def _get_courseid_table_dict(self):
        """返回课程与课程对应的group的table"""
        ctd = {}
        for c in self._all_courses:
            for g in c.groups:
                try:
                    # 去重，因为在 _all_courses 里面可能会出现两个
                    # 一样的课程（e.g.一个星期上两次2次2学分的X课）
                    if self._group_table_dict[g] not in ctd[c.cid]:
                        ctd[c.cid].append(self._group_table_dict[g])
                except KeyError:
                    ctd[c.cid] = [self._group_table_dict[g]]
        return ctd

    def _get_all_tables(self):
        #得到年级与相应课程的映射
        groups = self._get_all_groups()

        # 初始化课程表
        tables = []
        for k in groups:
            tables.append(CourseTable(k))
        return tables

    def _table_detail(self, num_table):
        """返回课程表具体内容
        Argument:
            num_table: 数字矩阵
        Return:
            (listof (listof int)) => string
        """
        max_len = 21 #最长多少个字符
        s = ""
        for i in xrange(len(cfg.TIME)):
            s += cfg.TIME[i] + ' '
            for j in range(len(cfg.DAY)):
                cid = num_table[i][j]
                if cid == -1:
                    s += '_' * max_len
                else:
                    c = self.id_to_course(cid)
                    info = "%s[%s]" % (c.name,c.teachers[0])
                    s += (info + "_" * max_len)[:max_len]
                s += '  '
            s += '\n'
        return s


if __name__ == '__main__':
    import reader
    r = reader.Reader('test.csv')
    cp = CoursePool(r.courses)
    # 打印所有的课程
    for c in cp._all_courses:
        print c.cid, c.name, c.credit, c.groups, c.teachers

    print 'ALL GROUPS: %s' % cp._get_all_groups()

    print '============='
    for i in cp._tables:
        print i
    print '-------------'
    for i in cp._group_table_dict:
        print 'GROUP: %s' % i
        print cp._group_table_dict[i]
    print '每个课程对应的课程表：'
    for i in cp._courseid_table_dict:
        c = cp.id_to_course(i)
        print 'COURSE: %s %s %s' % (c.name, c.groups, c.teachers)
        for k in cp._courseid_table_dict[i]:
            print k
    print '每个老师对应的课程'
    for t in cp._teacher_cid_dict:
        print 'TEACHER: %s' % t
        print cp._teacher_cid_dict[t]
