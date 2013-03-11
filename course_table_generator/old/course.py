class Course:
    def __init__(self, cid, name, credit, grade, teachers, start_time):
        self.name = name
        self.credit = credit
        self.grade_name = grade
        self.teachers = teachers
        self.start_time = start_time #represented as [1,2] for example
        self.cid = cid

    def __str__(self):
        return self.name

    def need_allocate_p(self):
        return self.start_time == None