from coursetable import CourseTable

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
            if c.start_time == None:
                self.courses.append(c)

    def __str__(self):
        s = "=======Grade: %s=======\n" % self.name
        for c in self.all_courses:
            s += str(c) + "\n"
        s += self.course_table.pretty_course_table()
        return s

    def pretty_grade_course_table(self):
        s = "==== Grade: %s ====\n" % self.name
        s += self.course_table.pretty_course_table()
        return s
        
    def set_course(self, course, start_time):
        return self.course_table.set_course(course, start_time)

    def unset_course(self, course, start_time):
        self.course_table.unset_course(course, start_time)