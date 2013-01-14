# configure file for course table generator

TIME =   ["08:00-08:50", "09:00-09:50", \
          "10:10-11:00", "11:10-12:00", \
          "12:10-13:00", "13:00-13:50", \
          "14:00-14:50", "15:00-15:50", \
          "16:10-17:00", "17:10-18:00"]

DAY = ["Mon", "Tue", "Wed", "Thu", "Fri"]

# this should be "time >= 9:00"
STUDENT_PREFER_TIME_NOT = [0]

# the data structure has changed
# refer to util.py
COURSE_PREFER_TIME = { 

#23 : [4,5,6,7,8,9],
#34 : [1,2,3,4]
                  
}

TEACHER_PREFER_TIME = {
#"Ben-Piet Venter".upper() : [0,1,2,3,4],
#"LIU Peng".upper() : [0, 1, 2, 3, 4],
}

TEACHER_PREFER_DAY = {

}



VIRTUAL_COURSE = 10000

