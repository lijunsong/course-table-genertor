from config import *

class CourseTable:
    """ CourseTable class represents a course table

    if constructed with information of courses, those pre-allocated course
    will be set on coursetable"""
    def __init__(self, courses):
        self.period_num = len(TIME)
        self.day_num = len(DAY)
        self.courses = courses
        self.coursetable = [[-1 for col in DAY] for row in TIME]
        self.set_in_advance()
           
    def __str__(self):
        s = str(self.coursetable)
        return s

    def set_in_advance(self):
        # pre_alloc course
        for which in range(0, len(self.courses)):
            if self.courses[which].start_time != None:
                self.set_course(which, self.courses[which].start_time)
    
    def concatenate_time_p(self, which_course, start_time):
        """ given course and its start time, this function will check
        current course table to see if there is any course that concatenates
        to current course 
        """
        credit = self.courses[which_course].credit
        day = start_time[1]
        end_time = start_time[0] + credit - 1
        check_time_before = start_time[0] - 1
        check_time_after  = end_time + 1
        if check_time_before >= 0 and check_time_after < self.period_num:
            return self.coursetable[check_time_before][day] != -1 or self.coursetable[check_time_after][day]  != -1
        else:
            if check_time_before < 0: # check check_time_after
                return self.coursetable[check_time_after][day] != -1
            else:
                return self.coursetable[check_time_before][day] != -1
        
    def can_set_p(self, which_course, start_time):
        res = True
        credit = self.courses[which_course].credit
        posi = start_time[0]
        posj = start_time[1]
        
        if self.concatenate_time_p(which_course, start_time):
            return False
        
        for i in range(0, credit):
            if posi + i >= self.period_num or self.coursetable[posi + i][posj] != -1:
                res = False
                break
        return res
    
    def set_course(self, which_course, start_time):
        """ set course at start_time

        return True if set sucessfully; otherwise return False"""
        
        posi = start_time[0]
        posj = start_time[1]
        if not self.can_set_p(which_course, start_time):
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
        for i in range(self.period_num):
            s += TIME[i] + " "
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