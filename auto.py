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
        self.tabletable = None

def read_course_info(file_name):
    contents = open(file_name).readlines()
    courses = []
    for content in contents:
        course_info = content.strip().split(",")
        courses.append(Course(course_info[0], course_info[1], course_info[2], course_info[3]))
    return courses


if __name__ == '__main__':
    period = ["8:00", "9:00", "10:10", "11:10", "12:10", "14:00", \
              "15:00", "16:10", "17:10"]
    timetable = [[col for col in range(7)] for row in period]

