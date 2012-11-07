from config import *

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
    for x in range(0, len(PERIOD)):
        if tm <= PERIOD[x][:5]:
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

if __name__=='__main__':
    assert to_standard_time("9:01") == "09:01"
    assert to_standard_time("19:00") == "19:00"
    assert to_standard_time("0:4") == "00:04"
    
    assert time_to_pos("8:00 mon") == [0,0]
    assert time_to_pos("12:10 tue") == [4, 1]
    assert time_to_pos("13:20 WED") == [6, 2]