#!/usr/bin/python

import re
from util import *
from course import Course
from coursetable import CourseTable



class Generator:
    def __init__(self, grades):
        self.grades = grades
        self.total_grade = len(grades)
        self.time_num = len(TIME)
        self.day_num = len(DAY)

    def pretty_print_all_grades(self):
        for g in self.grades:
            print g.pretty_grade_course_table()

    def set_next_course(self, which_grade, which_is_next, start_time=None):
        #TODO: cut the tree
        if start_time == None:
            for i in range(self.time_num):
                for j in range(self.day_num):
                    new_time = [i, j]
                    self.generate(which_grade, which_is_next, new_time)
        else:
            self.generate(which_grade, which_is_next, start_time)
        
    def set_next_grade(self, which_is_next, which_course=None, start_time=None):
        """ start to set next grade's first course """
        if start_time == None:
            for i in range(self.time_num):
                for j in range(self.day_num):
                    new_time = [i, j]
                    self.generate(which_is_next, 0, new_time)
        else:
            self.generate(which_is_next, which_course, start_time)

    # int * int * int * int => boolean
    def generate(self, which_grade, which_course, start_time): #return boolean
        # todo: add course table as another formal arguments
        grade = self.grades[which_grade]
        total_course = len(grade.courses)
        set_p = False

        # try to set couse at (i, j)
        debug_print("[try] to set course %s to %s" % (grade.courses[which_course].name, start_time))
        if not grade.courses[which_course].need_allocate_p(): # pre-allocatd
            debug_print("pre allocated one!")
        else:
            set_p = grade.set_course(which_course, start_time) 
            if not set_p:  #fail to set course in the table
                debug_print("[failed] to set course %s to %s" % (grade.courses[which_course].name, start_time))
                return False
            else:
                debug_print("[successed] to set course %s to %s" % (grade.courses[which_course].name, start_time))

        if which_course == total_course - 1 and which_grade == self.total_grade - 1: # successfully put all courses in all grades
            #get all course table, return True
            debug_print("get final result: ")
            self.pretty_print_all_grades()
            if set_p:
                debug_print("[unset] course %s to %s" % (grade.courses[which_course].name, start_time))
                grade.unset_course(which_course, start_time) #before going back, unset
            return True
        # else: not all courses are allocated
        elif which_course == total_course -1: # successfully put all courses in one grade
            debug_print("[try] to generate next grade: %s" % self.grades[which_grade + 1].name)
            self.set_next_grade(which_grade + 1)
        else:
            debug_print("[try] to generate next course: %s" % grade.courses[which_course+1].name)
            self.set_next_course(which_grade, which_course + 1)

        if set_p:
            debug_print("[unset] course %s to %s" % (grade.courses[which_course].name, start_time))
            grade.unset_course(which_course, start_time) #before going back, unset
        return False
        
    def start(self):

        for i in range(self.time_num):
            for j in range(self.day_num):
                start_time = [i, j]
                self.generate(0, 0, start_time)

if __name__ == '__main__':
    from reader import Reader
    courses = Reader('test.csv').get_courses()
    grades = get_all_grades_info(courses)
    
#   for g in grades:
#       g.pretty_grade_course_table()
#       print g
#   exit(0)

    gen = Generator(grades)
    gen.start()
    for g in grades:
        g.pretty_grade_course_table()
