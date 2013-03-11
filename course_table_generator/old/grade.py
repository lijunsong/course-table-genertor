from coursetable import CourseTable

class Grade:
    """  NOTE:
    courses: courses that need allocate
    all_courses: courses include pre-allocated courses
    """
    def __init__(self, name, all_courses):
        self.name = name
        self.unallocated_courses = []  # courses that need to allocate
        self.all_courses = all_courses
        self.course_table = CourseTable(all_courses)
        for c in all_courses:
            if c.need_allocate_p():
                self.unallocated_courses.append(c)

    def __str__(self):
        s = "=======Grade: %s=======\n" % self.name
        for c in self.all_courses:
            s += str(c) + "\n"
        s += self.course_table.pretty_course_table()
        return s

    def id_to_course(self, course_id):
        """int => Course:
        this function is used to refer to course with its id
        """
        for i in self.all_courses:
            if i.cid == course_id:
                return i
        print "course_id:%d is not found!" % course_id
        exit(1)

    def pretty_grade_course_table(self):
        s = "==== Grade: %s ====\n" % self.name
        s += self.course_table.pretty_course_table()
        return s
        
    def set_course(self, course_id, start_time):
        return self.course_table.set_course(course_id, start_time)

    def unset_course(self, course_id, start_time):
        self.course_table.unset_course(course_id, start_time)