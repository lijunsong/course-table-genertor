from config import *
from util import *

class CourseTable:
    """ CourseTable class represents a course table

    if constructed with information of courses, those pre-allocated course
    will be set on coursetable"""
    def __init__(self, courses):
        self.period = PERIOD
        self.day_num = len(DAY)
        self.courses = courses
        self.coursetable = [[-1 for col in range(self.day_num)] for row in self.period]
        self.set_in_advance()
           
    def __str__(self):
        s = str(self.coursetable)
        return s

    def set_in_advance(self):
         # pre_alloc course
        for which in range(0, len(self.courses)):
            if self.courses[which].start_time != None:
                self.set_course(which, self.courses[which].start_time)

    def set_course(self, which_course, start_time):
        """ set course at start_time

        return True if set sucessfully; otherwise return False"""
        if start_time == None:
            return
        posi = start_time[0]
        posj = start_time[1]
        if self.coursetable[posi][posj] != -1:
            return False
        else:
            for i in range(0, self.courses[which_course].credit):
                self.coursetable[posi+i][posj] = which_course
            return True

    def unset_course(self, which_course, start_time):
        if start_time == None:
            return
        posi = start_time[0]
        posj = start_time[1]
        for i in range(0, self.courses[which_course].credit):
            self.coursetable[posi+i][posj] = -1
        

    def pretty_course_table(self):
        s = ""
        for i in range(len(self.period)):
            s += self.period[i] + " "
            for j in range(5):
                o = self.coursetable[i][j]
                if o != -1:
                    s += (self.courses[o].name+" "*20)[:20]
                else:
                    s += "_"*20
                s += "  "
            s += "\n"
        return s
    
if __name__ == '__main__':
    from reader import Reader
    reader = Reader("info.csv")
    coursetable = CourseTable(reader.get_courses())
    print coursetable.pretty_course_table()