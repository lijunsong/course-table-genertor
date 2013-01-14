from course import Course
import csv
from util import *

class Reader:
    """Process files to get courses"""
    def __init__(self, file_name, delimiter=",", comment="#"):
        self.file_name = file_name
        self.delimiter = delimiter
        self.comment   = comment
        self.courses = []
        self.__process_csv()
    
    def get_courses(self):
        return self.courses

    def __check_sanity(self, course_info):
        """ check the sanity of the line """
        try:
            # should have 5 columns
            assert len(course_info) == 5
            # the second one should be numbers
            assert course_info[1].replace(".","",1).isdigit()
            # the last one should be like 1,1
            # pass
            return True
        except:
            return False

    def __is_comment(self, line):
        # string => boolean
        return line.startswith(self.comment) or line == ""

    def _get_teachers(self, teachers):
        return map(str.upper, map(str.strip, teachers.strip().split(";")))

    def __process_csv(self):
        #try:
            with open(self.file_name, "rb") as csvfile:
                course_reader = csv.reader(csvfile)
                for cid, name, credit, grade, teachers, start_time in course_reader:
                    if self.__is_comment(cid):
                        continue
                    # if the course has been allocated
                    pos = time_to_pos(start_time)
                    teachers = self._get_teachers(teachers)
                    course = Course(cid, name, int(credit), grade, teachers, pos)
                    self.courses.append(course)
        #except: 
        #    print "fail to process course file"
        #    exit(1)
            
if __name__=='__main__':
    reader = Reader("test.csv")
    for c in reader.get_courses():
        print c.cid, c.name, c.credit, c.grade_name, c.teachers
