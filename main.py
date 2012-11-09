from coursetable import CourseTable
from grade import Grade
from course import Course
from util import *
from generator import Generator
from reader import Reader
from config import *

class Main:
    def __init__(self, file_name):
        self.reader = Reader(file_name)
        self.courses = self.reader.get_courses()
        self.grades = get_all_grades_info(self.courses)
        self.generator = Generator(self.grades)
    
    def start(self):
        self.generator.start()

if __name__=='__main__':
    import sys
    if len(sys.argv) < 2:
        print "main.py needs additional argument as file name"
        exit(1)
    
        
    main = Main(sys.argv[1])
    main.start()
    