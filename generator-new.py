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

    def pretty_print_grade(self, g):
        "int => void"
        print self.grades[g].pretty_grade_course_table()

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
                    course_id = self.grades[grade].course_table.coursetable[time][day]
                    if course_id != -1 and \
                       self.grades[grade]._id_to_course(course_id).need_allocate_p():
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
         
        # TODO: sort by total credits in a day! 
        classrooms = self.compute_eachday_classroom()
        print "classroom usage: %s" % classrooms
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
            elif before_noon_p(get_end_time(TIME[time])) and \
                time not in STUDENT_PREFER_TIME_NOT:
                time_order_before_noon.append(time)
                #break # only one position is enough


        print "in day %s, time_order_before_noon: %s" % (which_day, time_order_before_noon)
        # check the time after noon
        no_class_after_noon = True
        time_order_after_noon = []
        for time in range(self.time_num):
            if not before_noon_p(get_start_time(TIME[time])) and \
               self.grades[which_grade].course_table.coursetable[time][which_day] != -1:
                no_class_after_noon = False
            elif not before_noon_p(get_start_time(TIME[time])) and \
               time not in STUDENT_PREFER_TIME_NOT:
                time_order_after_noon.append(time)
                #break

        print "in day %s, time_order_after_noon: %s" % (which_day, time_order_after_noon)
                
        res = []
        if no_class_before_noon == False and no_class_after_noon:
            res.extend(time_order_after_noon)
            res.extend(time_order_before_noon)
        else:
            res.extend(time_order_before_noon)
            res.extend(time_order_after_noon)
        print "return from order_time(): %s" % res
        return res
    
    
    def set_course(self, which_grade, nth_unallocated):
        # TODO: ordered_day should be start with the prefered day in the config.py
        # then following other not prefered time
        ordered_day = self.order_day()
        print "set_course of grade %s course %s" % (which_grade, nth_unallocated)
        for day in ordered_day:
            ordered_time = self.order_time(which_grade, day)
            for time in ordered_time:
                print "start to set course on %s,%s" % (time, day)
                self.generate_new(which_grade, nth_unallocated, [time, day])
    
    def set_grade(self, which_grade):  
        self.pretty_print_all_grades()  
        ordered_day = self.order_day()   
        for day in ordered_day:        
            ordered_time = self.order_time(which_grade, day)
            for time in ordered_time:
                # start from the first *unallocated* course!
                self.generate_new(which_grade, 0, [time, day])
        
    def generate_new(self, which_grade, nth_unallocated, start_time):
        grade = self.grades[which_grade]
        total_course = len(grade.unallocated_courses)
        # get the course_id of the nth_unallocated course
        course_id = grade.unallocated_courses[nth_unallocated].cid 
        
        print "generate_new(grade:%s, course:%s(%s), start_time:%s" % (which_grade, nth_unallocated, grade.unallocated_courses[nth_unallocated], start_time)
        set_p = grade.set_course(course_id, start_time)
        if not set_p:
            print "cannot set on %s" % start_time
            return False

        # debug
        # self.pretty_print_grade(which_grade)

        if nth_unallocated == total_course - 1 and which_grade == self.total_grade - 1:
            self.pretty_print_all_grades()
            if set_p:
                grade.unset_course(course_id, start_time)
                return True
        elif nth_unallocated == total_course - 1:
            self.set_grade(which_grade + 1)
        else:
            # DONE: get next course from optimized course list
            print "[generate_new]: begin to set next course"
            self.set_course(which_grade, nth_unallocated + 1)
        
        if set_p:
            grade.unset_course(course_id, start_time)
        return False
        
    def start(self):
        self.set_grade(0)

if __name__ == '__main__':
    from reader import Reader
    courses = Reader('test.csv').get_courses()
    grades = get_all_grades_info(courses)
    
#    for g in grades:
#        #g.pretty_grade_course_table()
#        print g
#    exit(0)

    gen = Generator(grades)
    gen.start()
    for g in grades:
        g.pretty_grade_course_table()
