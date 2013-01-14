from config import *
from grade import Grade

def convert_str_to_num(str_lst):
    return [float(n) for n in str_lst.split(",")]

def to_standard_time(time):
    """standard_time is "xx:xx" """
    # TODO: optimize
    s = time.split(":")
    if len(s[0]) == 1: s[0] = "0" + s[0]
    if len(s[1]) == 1: s[1] = "0" + s[1]
    return ":".join(s)

def before_noon_p(time):
    return (to_standard_time(time) <= "12:59")

def get_start_time(time_range):
    return to_standard_time(time_range.split('-')[0])

def get_end_time(time_range):
    return to_standard_time(time_range.split('-')[1])

def time_to_pos(time):
    """ convert the surface representation of time to [i,j] position"""
    if time == "":
        return None
    
    i = j = None
    
    tm, day = time.strip().split()
    tm = to_standard_time(tm.strip())
    day = day.strip().capitalize()[:3]
    for x in range(0, len(TIME)):
        if tm <= TIME[x][:5]:
            i = x
            break
    if i == None:
        print "error occured when processing time: %s" % time
        exit(1)
    for x in range(0, len(DAY)):
        if day == DAY[x][:3]:
            j = x
            break
    if j == None:
        print "error occured when processing day: %s" % time
        exit(1)
        
    return [i, j]

def get_grades_name(courses):
    """ according to the courses given, this function will
    return names of all grades in a list"""
    result = []
    for c in courses:
        if not c.grade_name in result:
            result.append(c.grade_name)
            
    return result

def get_courses_of_grade(grade_name, courses):
    """ return grade's courses """
    res = []
    for c in courses:
        if c.grade_name == grade_name:
            res.append(c)
    return res

def conditional_course_p(course):
    """Course => boolean:
    check if the course is conditional course
    """
    if course.name in COURSE_PREFER_TIME:
        return True
    if set(course.teachers).issubset(TEACHER_PREFER_TIME):
        return True
    if set(course.teachers).issubset(TEACHER_PREFER_DAY):
        return True
    return False

def sort_courses(courses):
    "(listof Course) => (listof Course)"
    conditional = []
    els = []
    for c in courses:
        if conditional_course_p(c):
            conditional.append(c)
        else:
            els.append(c)

    conditional.extend(els)
    return conditional

def get_all_grades_info(courses):
    """(listof Course) => (listof Grade):

    NOTE: This function has sorted the courses based on configure file.
    """
    result = []
    gs = get_grades_name(courses)
    for grade_name in gs:
        cs = get_courses_of_grade(grade_name, courses)
        # sort the course: conditonal courses should be put at the head
        cs = sort_courses(cs)
        result.append(Grade(grade_name, cs))
    return result

def get_not_pre_alloc_courses(courses):
    result = []
    for c in courses:
        if c.start_time == None:
            result.append(c)
    return result

def debug_print(s):
    DEBUG = True
    if DEBUG:
        print "debug: ",
        print s
        
if __name__=='__main__':
    from reader import Reader
    reader = Reader('test.csv')
    assert to_standard_time("9:01") == "09:01"
    assert to_standard_time("19:00") == "19:00"
    assert to_standard_time("0:4") == "00:04"
    
    assert time_to_pos("8:00 mon") == [0,0]
    assert time_to_pos("12:10 tue") == [4, 1]
    assert time_to_pos("13:20 WED") == [6, 2]
    assert get_grades_name(reader.get_courses()) == ['Y1-1', 'Y1-2', 'Y2-1', 'Y2-2']
    print get_all_grades_info(reader.get_courses())
