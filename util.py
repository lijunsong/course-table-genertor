from config import *
from grade import Grade

def convert_str_to_num(str_lst):
    return [float(n) for n in str_lst.split(",")]

def to_standard_time(time):
    """standard_time is "xx:xx" """
    s = time.split(":")
    if len(s[0]) == 1: s[0] = "0" + s[0]
    if len(s[1]) == 1: s[1] = "0" + s[1]
    return ":".join(s)

def time_to_pos(time):
    """ convert the surface representation of time to [i,j] position"""
    if time == "":
        return None
    
    i = j = None
    
    tm, day = time.strip().split()
    tm = to_standard_time(tm.strip())
    day = day.strip().capitalize()
    for x in range(0, len(TIME)):
        if tm <= TIME[x][:5]:
            i = x
            break
    if i == None:
        print "error occured: %s" % time
        exit(1)
    for x in range(0, len(DAY)):
        if day == DAY[x][:3]:
            j = x
            break
    if j == None:
        print "error occured: %s" % time
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

def get_all_grades_info(courses):
    result = []
    gs = get_grades_name(courses)
    for grade_name in gs:
        cs = get_courses_of_grade(grade_name, courses)
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