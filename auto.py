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
    def __init__(self):
        self.period = ["08:00", "10:10", "13:00", "16:10"]
        self.coursetable = [[-1 for col in range(5)] for row in self.period]

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
    def __init__(self, name, courses):
        self.name = name
        self.courses = courses
        self.course_table = CourseTable()

    def __str__(self):
        s = "=======Grade: %s=======\n" % self.name
        for c in self.courses:
            s += str(c) + "\n"
        s += str(self.course_table)
        return s

    def dump_course_table(self):
        print "==== Grade: %s ====\n" % self.name
        self.course_table.print_course_table(self.courses)
        

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
        """ time_str would be '1,1;2,2;3,3'"""
        result = []
        if time_str.strip(" \""):
            lst = time_str.strip(" \"").split(";")
            for ele in lst:
                posi = int(ele.strip().split(",")[0])
                posj = int(ele.strip().split(",")[1])
                result.append([posi, posj])
        return result

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

    # int * int * int * int => boolean
    def generate(self, which_grade, which_course, which_posi, which_posj): #return boolean
        grade = self.grades[which_grade]
        total_course = len(grade.courses)

        set_p = grade.set_course(which_course, which_posi, which_posj)
        if not set_p:  #fail to set course in the table
            return False

        if which_course == total_course - 1 and which_grade == self.total_grade - 1: # successfully put all courses in all grades
            #get all course table, return True
            self.pretty_print_all_grades()
            grade.unset_course(which_course, which_posi, which_posj) #before going back, unset
            return True

        elif which_course == total_course -1: # successfully put all courses in one grade
            for i in range(4):
                for j in range(5):
                    if self.generate( which_grade + 1, 0, i, j) == True:
                        # get all course table, return True
                        self.pretty_print_all_grades()
                        grade.unset_course(which_course, which_posi, which_posj)
                        continue
                    else:
                        grade.unset_course(which_course, which_posi, which_posj)
                        continue
        else:

            for next_posi in range(4):
                for next_posj in range(5):
                    res = self.generate(which_grade, which_course + 1, next_posi, next_posj)
                    if res == True:
                        continue
                    else:
                        continue

        grade.unset_course(which_course, which_posi, which_posj)
        return False
        
    def start(self):
        # before allocating all courses
        # todo:
        # 1. allocate those pre-allocated courses
        # 2. order the courses in every grade
        return self.generate(0, 0, 0, 0)

if __name__ == '__main__':
    import sys
    import types

    assert len(sys.argv) == 2

    reader = ReadCourse(sys.argv[1])
    courses = reader.get_courses()
    flter = CourseFilter(courses)

    grades = flter.get_grade_objs()
    gen = Generator(grades)
    if gen.start() == True:
        for g in grades:
            g.dump_course_table()
