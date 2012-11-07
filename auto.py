#!/usr/bin/python

import re
from config import *
from course import Course
from coursetable import CourseTable
from reader import Reader


class Generator:
    def __init__(self, grades):
        self.grades = grades
        self.total_grade = len(grades)

    def pretty_print_all_grades(self):
        for g in self.grades:
            g.dump_course_table()

    def set_next_course(self, which_grade, which_is_next, which_posi=None, which_posj=None):
        if which_posi == None and which_posj == None:
            for i in range(4):
                for j in range(5):
                    self.generate(which_grade, which_is_next, i, j)
        else:
            self.generate(which_grade, which_is_next, which_posi, which_posj)
        
    def set_next_grade(self, which_is_next, which_course=None, which_posi=None, which_posj=None):
        if which_posi == None and which_posj == None and which_course == None:
            for i in range(4):
                for j in range(5):
                    self.generate(which_is_next, 0, i, j)
        else:
            self.generate(which_is_next, which_course, which_posi, which_posj)

    # int * int * int * int => boolean
    def generate(self, which_grade, which_course, which_posi, which_posj): #return boolean
        grade = self.grades[which_grade]
        total_course = len(grade.courses)
        set_p = False

        # try to set couse at (i, j)
        print "[try] to set course %s to (%s,%s)" % (grade.courses[which_course].name, which_posi, which_posj)
        if grade.courses[which_course].pre_alloc != None: # pre-allocatd
            print "pre allocated one!"
        else:
            set_p = grade.set_course(which_course, which_posi, which_posj)
            if not set_p:  #fail to set course in the table
                print "[failed] to set course %s to (%s,%s)" % (grade.courses[which_course].name, which_posi, which_posj)
                return False
            else:
                print "[successed] to set course %s to (%s,%s)" % (grade.courses[which_course].name, which_posi, which_posj)

        if which_course == total_course - 1 and which_grade == self.total_grade - 1: # successfully put all courses in all grades
            #get all course table, return True
            print "get final result: "
            self.pretty_print_all_grades()
            if set_p:
                print "[unset] course %s to (%s,%s)" % (grade.courses[which_course].name, which_posi, which_posj)
                grade.unset_course(which_course, which_posi, which_posj) #before going back, unset
            return True
        # else: not all courses are allocated
        elif which_course == total_course -1: # successfully put all courses in one grade
            print "[try] to generate next grade: %s" % self.grades[which_grade + 1].name
            self.set_next_grade(which_grade + 1)
        else:
            print "[try] to generate next course: %s" % grade.courses[which_course+1].name
            self.set_next_course(which_grade, which_course + 1)

        if set_p:
            print "[unset] course %s to (%s,%s)" % (grade.courses[which_course].name, which_posi, which_posj)
            grade.unset_course(which_course, which_posi, which_posj) #before going back, unset
        return False
        
    def start(self):
        # before allocating all courses
        # todo:
        # 1. allocate those pre-allocated courses
        # 2. order the courses in every grade
        for i in range(4):
            for j in range(5):
                self.generate(0, 0, i, j)

if __name__ == '__main__':
    import sys
    import types

    assert len(sys.argv) == 2

    courses = Reader(sys.argv[1]).get_courses()
    flter = CourseFilter(courses)

    grades = flter.get_grade_objs()
    
#   for g in grades:
#       g.dump_course_table()
#       print g
#   exit(0)

    gen = Generator(grades)
    gen.start()
    for g in grades:
        g.dump_course_table()
