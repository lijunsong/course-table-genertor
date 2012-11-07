from grade import Grade    



            
class CourseFilter:
    def __init__(self, courses):
        self.courses = courses

    def grade_courses(self, grade):
        result = []
        for c in self.courses:
            if c.grade_name == grade:
                result.append(c)
        return result

    def get_total_grades_name(self):
        result = []
        for c in self.courses:
            try:
                result.index(c.grade_name)
            except ValueError:
                result.append(c.grade_name)
        return result

    def get_grade_objs(self):
        result = []
        gs = self.get_total_grades_name()
        for g in gs:
            name = g
            cs = self.grade_courses(name)
            result.append(Grade(name, cs))
        return result