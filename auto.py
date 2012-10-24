#!/usr/bin/python


class Course:
    def __init__(self, name, credit, grade, teacher, time=None):
        self.name = name
        self.credit = credit
        self.grade = grade
        self.teacher = teacher
        self.time = time

class Grade:
    def __init__(self, name, course):
        self.name = name
        self.course = course
        self.course_table = None

class Reader:
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
            course = self.__course_obj(content)
            self.courses.append(course)
            
def pretty_courses():
    for c in courses:
        print c.__dict__

if __name__ == '__main__':
    import sys

    period = ["8:00", "9:00", "10:10", "11:10", "12:10", "14:00", \
              "15:00", "16:10", "17:10"]
    timetable = [[col for col in range(7)] for row in period]
    
    assert len(sys.argv) == 2

    reader = Reader(sys.argv[1])
    courses = reader.get_courses()

