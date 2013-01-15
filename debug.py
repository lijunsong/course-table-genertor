#!/usr/bin/env python
# encoding: utf-8

class Debug:
    """Debug 类用于调试时候的输出"""

    def __init__(self, msg):
        self.msg = msg

    def stdout(self, *arg):
        print "[%s]" % self.msg
        for a in arg:
            print a

if __name__=='__main__':
    d = Debug('In Debug')
    d.stdout(1)
    d.stdout((1,2))
    d.stdout("""hello
        this is notright""")
    d.stdout([1,2,3,4,4])
    d.stdout({1:3, "ddd":34})
    d.stdout(1,2)
