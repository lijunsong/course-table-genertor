# configure file for course table generator

TIME =   ["08:00-08:50", "09:00-09:50", \
          "10:10-11:00", "11:10-12:00", \
          "12:10-13:00", "13:00-13:50", \
          "14:00-14:50", "15:00-15:50", \
          "16:10-17:00", "17:10-18:00"]

DAY = ["Mon", "Tue", "Wed", "Thu", "Fri"]

STUDENT_PREFER = { "all_course" : "time > 09:00" }

COURSE_PREFER = { "course_name" : "time > 09:00",
                  "course_name2" : "10:00 < time < 18:00"
                  
                }

TEACHER_PREFER = { "teacher_name" : " time > 09:00",
                   "teacher_name2" : "time < 17:00",
                   "teacher_name3" : "not on mon"
                   }

VIRTUAL_COURSE = 10000

