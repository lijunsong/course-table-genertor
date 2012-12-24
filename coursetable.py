from config import *
from log import *


# OTHER IMPLEMENT: add virtual course instead of judging the mutual time.

class CourseTable:
    """ CourseTable class represents a course table

    if constructed with information of courses, those pre-allocated course
    will be set on coursetable"""
    def __init__(self, courses):
        self.time_num = len(TIME)
        self.day_num = len(DAY)
        self.courses = courses
        self.coursetable = [[-1 for col in DAY] for row in TIME]
        # the time between courses may not have break at all, find which course is in 
        # this situation. 
        self.mutual_time = self.__get_mutual_pos()
        self.set_initially()
           
    def __str__(self):
        s = str(self.coursetable)
        return s

    def __get_mutual_pos(self):
        res = []
        for current in range(0, self.time_num - 1):
            next = current + 1
            if self.__concatenate_str_p(TIME[current], TIME[next]):
                res.append(current)
        return res 
        
    def set_initially(self):
        # pre_alloc course
        for which in range(0, len(self.courses)):
            if not self.courses[which].need_allocate_p():
                self.set_course(which, self.courses[which].start_time, True)
    
    def __concatenate_str_p(self, t1, t2):
        if t1.strip().split("-")[1] == t2.strip().split("-")[0] or \
           t1.strip().split("-")[0] == t2.strip().split("-")[1]:
            return True
        else:
            return False
    
    def concatenate_time_p(self, which_course, course_range, day):
        """ given course and its start time, this function will check
        current course table to see if there is any course that concatenates
        to current course
        
        concatenate means: 10:00-11:50 with succeeding 11:50-12:40
        """
        # first check if the time is in the mutual time list
        conc = False

        for mutual_time in self.mutual_time:
            # if which_course is in a mutual time, check if next pos has a course
            if mutual_time in course_range and \
               mutual_time == course_range[-1] and \
               self.coursetable[mutual_time + 1][day] != -1:
                conc = True
                break
            # check if previous pos has a course
            elif mutual_time + 1 in course_range and \
                 mutual_time + 1 == course_range[0] and \
                 self.coursetable[mutual_time][day] != -1:
                conc = True
                break
            else:
                continue
        return conc 

    def check_config_p(self, which_course, start_time):
        time = start_time[0]
        day  = start_time[1]
        # check student prefered time
        if time in STUDENT_PREFER_TIME_NOT:
            print 1
            return False

        # check course prefered time
        course_name = self.courses[which_course].name #intro bug: diff teacher with same course name
        if COURSE_PREFER_TIME.has_key(course_name):
            if time not in COURSE_PREFER_TIME[course_name]:
                print 2
                return False

        # check teacher perfered time
        teacher = self.courses[which_course].teacher
        if TEACHER_PREFER_TIME.has_key(teacher):
            if time not in TEACHER_PREFER_TIME[teacher]:
                print 3
                return False

        # check teacher prefered day
        if TEACHER_PREFER_DAY.has_key(teacher):
            if day not in TEACHER_PREFER_DAY[teacher]:
                print 4
                return False

        return True

    def can_set_p(self, which_course, start_time):

        credit = self.courses[which_course].credit
        posi = start_time[0]
        posj = start_time[1]
        
        course_range = range(posi, posi + credit)

        # check configure. If current course with the start_time is
        # not prefered by teachers and students, return False
        if not self.check_config_p(which_course, start_time):
            print "check_config_p return False"
            return False
        
        # courses CANNOT be setted to cross the mutual time
        for mutual_time in self.mutual_time:
            if mutual_time in course_range and mutual_time + 1 in course_range:
                print "cross mutual time"
                return False

        # since the number of courses is determined by credits, here check if current
        # start_time can meet the requirement of credits
        for i in range(0, credit):
            if posi + i >= self.time_num or self.coursetable[posi + i][posj] != -1:
                print("less than credit %s" % (posi + i))
                return False

        # Now, we have time to set the course,
        # but....check if there is any possible that there are courses before or after 
        # `which_course` that students do not have break between courses
        if self.concatenate_time_p(which_course, course_range, posj):
            print("concatenate")
            return False
        
        return True
    
    def set_course(self, which_course, start_time, set_force=False):
        """ set course at start_time

        return True if set sucessfully; otherwise return False"""
        
        posi = start_time[0]
        posj = start_time[1]
        if set_force == False and not self.can_set_p(which_course, start_time):
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
        for i in range(self.time_num):
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
    reader = Reader("test.csv")
    coursetable = CourseTable(reader.get_courses())
    print coursetable.mutual_time
    print coursetable.pretty_course_table()
