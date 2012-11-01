#!/usr/bin/python

import re

class Course:
    def __init__(self, name, credit, grade, teacher, pre_alloc):
        self.name = name
        self.credit = credit
        self.grade_name = grade
        self.teacher = teacher
        self.pre_alloc = pre_alloc
    def __str__(self):
        return self.name

class CourseTable:
    """ CourseTable class represents a course table

    if constructed with information of courses, those pre-allocated course
    will be set on coursetable"""
    def __init__(self, courses=None):
        self.period = ["08:00", "10:10", "13:00", "16:10"]
        self.coursetable = [[-1 for col in range(5)] for row in self.period]
        if courses != None:
            # pre_alloc course
            for which in range(0, len(courses)):
                if courses[which].pre_alloc != None: #pre_alloc
                    self.set_course(which, courses[which].pre_alloc[0] -1, courses[which].pre_alloc[1] -1)

    def __str__(self):
        s = str(self.coursetable)
        return s

    def set_course(self, course, posi, posj):
        """ set course at posi posj

        return True if set sucessfully; otherwise return False"""
        if self.coursetable[posi][posj] != -1:
            return False
        else:
            self.coursetable[posi][posj] = course
            return True

    def unset_course(self, course,posi, posj):
        self.coursetable[posi][posj] = -1

    def print_course_table(self, extra_info):
        for i in range(4):
            print self.period[i] + " ",
            for j in range(5):
                o = self.coursetable[i][j]
                if o != -1:
                    print (str(extra_info[o])+" "*20)[:20],
                else:
                    print "_"*20,
                print "  ",
            print "\n"
    
class Grade:
    """  NOTE:
    courses: courses that need allocate
    all_courses: courses include pre-allocated courses
    """
    def __init__(self, name, courses):
        self.name = name
        self.courses = []  # courses that need to allocate
        self.all_courses = courses
        self.course_table = CourseTable(courses)
        for c in courses:
            if c.pre_alloc == None:
                self.courses.append(c)

    def __str__(self):
        s = "=======Grade: %s=======\n" % self.name
        for c in self.all_courses:
            s += str(c) + "\n"
        s += str(self.course_table)
        return s

    def dump_course_table(self):
        print "==== Grade: %s ====\n" % self.name
        self.course_table.print_course_table(self.all_courses)
        

    def set_course(self, course, posi, posj):
        return self.course_table.set_course(course, posi, posj)

    def unset_course(self, course, posi, posj):
        self.course_table.unset_course(course, posi, posj)

class ReadCourse:
    def __init__(self, file_name, delimiter=",", comment="#"):
        self.file_name = file_name
        self.delimiter = delimiter
        self.comment   = comment
        self.courses = []
        self.__check_file()
        self.__process_csv()

    def __check_file(self, check_type = "csv"):
        try:
            assert self.file_name.endswith(check_type)
        except AssertionError:
            print "File %s is not type of %s" % (self.file_name, self.check_type)
            exit(1)
    
    def get_courses(self):
        return self.courses

    def __check_sanity(self, course_info):
        """ check the sanity of the line """
        try:
            # should have 5 columns
            assert len(course_info) == 5
            # the second one should be numbers
            assert course_info[1].replace(".","",1).isdigit()
            # the last one should be like 1,1; 2,2; 3,3
            # pass
            return True
        except:
            return False

    def __pre_alloc(self, time_str):
        """ time_str would be '1,1'
        
        return: [posi, posj]
        """
        if time_str.strip(" \""):
            lst = time_str.strip(" \"").split(",")
            return [int(lst[0]), int(lst[1])]
        else:
            return None

    def __course_obj(self, row):
        course_info = row.strip().split(self.delimiter, 4)

        if not self.__check_sanity(course_info):
            print("line: %s is broken" % row.strip())
            exit(1)
        # whether to pre-allocate course
        pre_pos = self.__pre_alloc(course_info[4])
        return Course(course_info[0], course_info[1], course_info[2], course_info[3], pre_pos)

    def __is_comment(self, line):
        return line.startswith(self.comment)

    def __process_csv(self):
        contents = open(self.file_name).readlines()
        for content in contents:
            if self.__is_comment(content):
                continue
            course = self.__course_obj(content)
            self.courses.append(course)
            
class CourseFilter:
    def __init__(self, courses):
        self.courses = courses

    def grade_courses(self, grade):
        result = []
        for c in self.courses:
            if c.grade_name == grade:
                result.append(c)
        return result

    def get_total_grades_name(self):
        result = []
        for c in self.courses:
            try:
                result.index(c.grade_name)
            except ValueError:
                result.append(c.grade_name)
        return result

    def get_grade_objs(self):
        result = []
        gs = self.get_total_grades_name()
        for g in gs:
            name = g
            cs = self.grade_courses(name)
            result.append(Grade(name, cs))
        return result

def printt(os):
    if type(os) == types.ListType:
        for o in os:
            print o
    else:
        print os

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

    reader = ReadCourse(sys.argv[1])
    courses = reader.get_courses()
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
