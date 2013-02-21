#!/usr/bin/env python
# encoding: utf-8

from course import Course
import csv
import sys
import debug

d = debug.Debug('Reader')

class Reader:
    """读取课程信息的类

    Attributes:
        file_name -- 课程信息的文件名
        delimiter -- 每一列的分隔符
        comment   -- 注释符号（放在每行的最前面）
        courses   -- 课程对象数组
    """
    def __init__(self, file_name, delimiter=",", comment="#"):
        self.file_name = file_name
        self.delimiter = delimiter
        self.comment   = comment
        self.courses = []
        self._process_csv()

    def _is_comment_p(self, line):
        "(listof string) => boolean"
        empty_line = line == []
        if not empty_line:
            return line[0] == '' or line[0].startswith(self.comment)
        return True

    def _split(self, semicolon_str):
        """接到一个字符串，返回数组
        Argument:
            semicolon_str: 以分号分割域的字符串
        Return:
            string => (listof string)"""
        return map(str.upper,
                   map(str.strip,
                       semicolon_str.strip("; \n").split(";")))

    def filter_courses(self, group):
        """按照年级名筛选出课程

        Return: string => (listof Course)
        """
        f = lambda course: course.group == group
        return filter(f, self.courses)

    def get_groups_courses(self):
        """得到每个年级对应的课程字典

        Return:
            => (dictof string (listof Course))
        """
        f = lambda c: c.group
        groups = set(map(f, self.courses))
        g_c = {}
        for g in groups:
            g_c[g] = self.filter_courses(g)
        return g_c

    def _process_csv(self):
        "处理 csv 的方法"
        try:
            with open(self.file_name, "rb") as csvfile:
                course_reader = csv.reader(csvfile)
                try:
                    # 对每行进行处理
                    for course_info in course_reader:
                        if self._is_comment_p(course_info):
                            continue
                        cid, name, credit, groups, teachers, week, time = course_info
                        teachers = self._split(teachers)
                        gs = self._split(groups)
                        course = Course(cid, name, credit, gs,
                                        teachers, week, time)
                        self.courses.append(course)
                except Exception as e:
                    # TODO: 添加各种错误的 Exception
                    sys.exit('line %d: "%s"\nError: %s' %
                             (course_reader.line_num, ",".join(course_info), e))
        except IOError as e:
            sys.exit("file '%s' reading error\n%s" % (self.file_name, e))

if __name__=='__main__':
    reader = Reader("test-case/2012-2013.csv")
    for c in reader.courses:
        print c.cid, c.name, c.credit,
        print "group: %s, teachers: %s, start_time: %s" % (c.groups, c.teachers, c.start_time)
