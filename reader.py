#!/usr/bin/env python
# encoding: utf-8

from course import Course
import csv
import sys

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

    def _get_teachers(self, teachers):
        """教师名字全部大写，以分号为分隔符变成数组

        Argument:
            teachers: 以分号分割域的字符串

        Return
            string => (listof string)
        """
        return map(str.upper, map(str.strip,
                                  teachers.strip().split(";")))

    def filter_courses(self, grade):
        """按照年级名筛选出课程

        Return: string => (listof Course)
        """
        f = lambda course: course.grade == grade
        return filter(f, self.courses)

    def get_grades_courses(self):
        """得到每个年级对应的课程字典

        Return:
            => (dictof string (listof Course))
        """
        f = lambda c: c.grade
        grades = set(map(f, self.courses))
        g_c = {}
        for g in grades:
            g_c[g] = self.filter_courses(g)
        return g_c

    def _process_csv(self):
        "处理 csv 的方法"
        try:
            with open(self.file_name, "rb") as csvfile:
                course_reader = csv.reader(csvfile)
                try:
                    for course_info in course_reader:
                        if self._is_comment_p(course_info):
                            continue
                        cid, name, credit, grade, teachers, week, time = course_info
                        teachers = self._get_teachers(teachers)
                        course = Course(cid, name, credit, grade,
                                        teachers, week, time)
                        self.courses.append(course)
                except Exception as e:
                    # TODO: 添加各种错误的 Exception
                    sys.exit('line %d: "%s"\nError: %s' %
                             (course_reader.line_num, ",".join(course_info), e))
        except IOError as e:
            sys.exit("file '%s' reading error\n%s" % (self.file_name, e))

if __name__=='__main__':
    reader = Reader("test.csv")
    #for c in reader.courses:
    #    print c.cid, c.name, c.credit, c.grade_name, c.teachers, c.start_time
