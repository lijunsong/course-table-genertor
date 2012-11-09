class Course:
    def __init__(self, name, credit, grade, teacher, start_time):
        self.name = name
        self.credit = credit
        self.grade_name = grade
        self.teacher = teacher
        self.start_time = start_time #represented as [1,2] for example
    def __str__(self):
        return self.name
    def need_allocate_p(self):
        return self.start_time == None