#!/usr/bin/env python
# encoding: utf-8

from reader import Reader

file_name = "test.csv"

if __name__=='__main__':
    reader = Reader(file_name)
    grad_course = reader.get_grades_courses()
    for k in grad_course:
        print k
        for c in grad_course[k]:
            print "   %s" % c.name
