#!/usr/bin/env python
# encoding: utf-8

class Debug:
    """用于调试时候的输出"""

    PRINT_MARKER = True # True 代表输出调试信息
    def __init__(self, msg):
        self.msg = '[%s]' % msg

    def p(self, *arg):
        if Debug.PRINT_MARKER == False:
            return
        print self.msg,
        for a in arg:
            print str(a).replace("\n",'\n%s ' % self.msg),
        print ""

    def p_list(self, lst):
        if Debug.PRINT_MARKER == False:
            return
        for a in lst:
            print "%s * %s" % (self.msg, a)

if __name__=='__main__':
    d = Debug('In Debug')
    d.p(1)
    d.p((1,2))
    d.p("""hello
        this is notright""")
    d.p([1,2,3,4,4])
    d.p({1:3, "ddd":34})
    d.p(1,2)
