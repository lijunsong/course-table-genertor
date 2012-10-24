#!/usr/bin/python

class Course:
    def __init__(self, name, credit, grade, teacher, time=None):
        self.name = name
        self.credit = credit
        self.grade = grade
        self.teacher = teacher
        self.time = time
    def __str__(self):
        return "name:%s credit:%s grade:%s tcher:%s time:%s" \
                % (self.name, self.credit, self.grade, self.teacher, self.time)

class CourseTable:
    def __init__(self):
        self.period = ["08:00", "10:10", "13:00", "16:10"]
        self.coursetable = [[-1 for col in range(5)] for row in period]
    def set_course(course, posx, posy):
        self.coursetable[posx][posy] = course
    def unset_course(course,posx, posy):
        self.coursetable[posx][posy] = -1
    
class Grade:
    def __init__(self, name, courses):
        self.name = name
        self.courses = courses
        self.course_table = CourseTable()

    def __str__(self):
        s = "=======Grade: %s=======\n" % self.name
        for c in self.courses:
            s += str(c) + "\n"
        return s

    def set_course(self, course, posx, posy):
        self.course_table.set_course(course, posx, posy)

    def unset_course(self, course, posx, posy):
        self.course_table.unset_course(course, posx, posy)

class ReadCourse:
    def __init__(self, file_name, delimiter=","):
        self.file_name = file_name
        self.delimiter = delimiter
        self.courses = []
        self.__check_file_type()
        self.__process_csv()

    def __check_file_type(self, check_type = "csv"):
        try:
            assert self.file_name.endswith(check_type)
        except AssertionError:
            print "File %s is not type of %s" % (self.file_name, self.check_type)
            exit(1)
    
    def get_courses(self):
        return self.courses

    def __course_obj(self, row):
        course_info = row.strip().split(self.delimiter)
        return Course(course_info[0], course_info[1], course_info[2], course_info[3])

    def __process_csv(self):
        contents = open(self.file_name).readlines()
        for content in contents:
            if content.startswith("#"):
                continue
            course = self.__course_obj(content)
            self.courses.append(course)
            
class CourseFilter:
    def __init__(self, courses):
        self.courses = courses

    def grade_courses(self, grade):
        result = []
        for c in self.courses:
            if c.grade == grade:
                result.append(c)
        return result

    def get_total_grades(self):
        result = []
        for c in self.courses:
            try:
                result.index(c.grade)
            except ValueError:
                result.append(c.grade)
        return result

    def get_grade_objs(self):
        result = []
        gs = self.get_total_grades()
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

    # Grade * int * int * int * int => boolean
    def generate(self, which_grade, which_course, total_course, which_posx, which_posy): #return boolean
        which_grade.course_table.set_course(which_course, which_posx, which_posy)
        if which_course == total_course - 1: # successfully put all courses
            return True
        for next_posx in range(which_posx+1, 5):
            for next_posy in range(which_posy+1, 4):
                self.generate(which_grade, which_course + 1, total_course, next_posx, next_posy)
        which_grade.course_table.unset_course(which_course, which_posx, which_posy)
        
        
if __name__ == '__main__':
    import sys
    import types

    assert len(sys.argv) == 2

    reader = ReadCourse(sys.argv[1])
    courses = reader.get_courses()
    flter = CourseFilter(courses)
    grade = flter.get_total_grades()

    grades = flter.get_grade_objs()
    printt(grades)
