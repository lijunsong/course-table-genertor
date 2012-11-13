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

    def compute_eachday_classroom(self):
        """ according to the coursetables in all grades, return a dict, which maps
        
        each day -> the classrooms usesage information
        """
        res = {}
        for day in range(self.day_num):
            max_num = 0
            for time in range(self.time_num):
                classroom_num = 0
                for grade in range(self.total_grade):
                    if self.grades[grade].course_table.coursetable[time][day] != -1:
                        # compute how many grades have courses in a day at the same time
                        classroom_num += 1
                if classroom_num > max_num:
                    max_num = classroom_num 
            res[day] = max_num
        return res
    
    def order_day(self):
        """ according to coursetables in all grades, return a list, which
         is ordered day_num. Sorting is based on the classroom 
         usage info in each day"""
         
        classrooms = self.compute_eachday_classroom()
        sorted_day = sorted(classrooms, key = classrooms.get)
        return sorted_day
        
    def order_time(self, which_grade, which_day):
        """ given a grade and a certain day, return a list, which
        is ordered time(optimized sorted time) in `which_day`
        """
        # TODO: Order the time based on all coursetable's classroom
        # usage: set time, and compute classroom usage again, find the best
        # time order.
        
        # check the time before noon:
        no_class_before_noon = True
        time_order_before_noon = []
        for time in range(self.time_num):
            if before_noon_p(get_end_time(TIME[time])) and \
               self.grades[which_grade].course_table.coursetable[time][which_day] != -1:
                no_class_before_noon = False
            else:
                time_order_before_noon.append(time)
        # check the time after noon
        no_class_after_noon = True
        time_order_after_noon = []
        for time in range(self.time_num):
            if not before_noon_p(get_start_time(TIME[time])) and \
               self.grades[which_grade].course_table.coursetable[time][which_day] != -1:
                no_class_after_noon = False
            else:
                time_order_after_noon.append(time)
                
        res = []
        if no_class_before_noon == False and no_class_after_noon:
            res.extend(time_order_after_noon)
            res.extend(time_order_before_noon)
        else:
            res.extend(time_order_before_noon)
            res.extend(time_order_after_noon)
        return res
    
    
    def set_course(self, which_grade, which_course):
        ordered_day = self.order_day()
        
        for day in ordered_day:
            ordered_time = self.order_time(which_grade, day)
            for time in ordered_time:
                self.generate_new(which_grade, which_course, [time, day])
    
    def set_grade(self, which_grade):
        # TODO: get ordered course list
        
        ordered_day = self.order_day()
        for day in ordered_day:
            ordered_time = self.order_time(which_grade, day)
            for time in ordered_time:
                self.generate_new(which_grade, 0, [time, day]) # TODO: should be from ordered course list
        
    def generate_new(self, which_grade, which_course, start_time):
        grade = self.grades[which_grade]
        total_course = len(grade.courses)
        
        set_p = grade.set_course(which_course, start_time)
        if not set_p:
            return False
        
        if which_course == total_course - 1 and which_grade == self.total_grade - 1:
            self.pretty_print_all_grades()
            if set_p:
                grade.unset_course(which_course, start_time)
                return True
        elif which_course == total_course - 1:
            self.set_grade(which_grade + 1)
        else:
            # TODO: get next course from optimized course list
            self.set_course(which_grade, which_course + 1)
        
        if set_p:
            grade.unset_course(which_course, start_time)
        return False
    
    # int * int * int=> boolean
    def generate(self, which_grade, which_course, start_time): #return boolean
        # todo: add course table as another formal arguments
        grade = self.grades[which_grade]
        total_course = len(grade.courses)  # number of course that need be allocated
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
            debug_print("classroom: %s" % self.compute_eachday_classroom())
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
        self.set_grade(0)

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
