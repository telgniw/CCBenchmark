#!/usr/bin/env python
from common import Logger
import myblob, sys, os

def usage():
    print sys.argv[0], '<log_dir>', '<num>', '<size>', '<off_t>', '<repeat>'
    exit(1)

def error(msg):
    print 'Error:', msg
    exit(1)

#=================== parse argv begin ===================#
try:
    log_dir = sys.argv[1]
    num, size, off_t, repeat = [int(t) for t in sys.argv[2:]]
    os.mkdir(log_dir)
except OSError as e:
    error(e)
except (ValueError, IndexError):
    usage()
#==================== parse argv end ====================#

def run(func, args=()):
    t = func(*args)
    t.start()
    t.join()
    res = t.get()
    print res
    return 'SUCCESS' in res

def run_multi(func, name):
    log_name = os.path.join(log_dir, '%d.%s.log' % (i, name))
    log = Logger(strm=open(log_name, 'w'))
    li = []
    for j in range(i):
        li.append(func(j))
    for j in range(i):
        li[j].start()
    for j in range(i):
        li[j].join()
        log.log(li[j].get())
    del log

#====================== test begin ======================#
if not run(myblob.init, (num, size)):
    error('init failed')


for i in range(off_t, num+1, off_t):
    print 'i =', i
    for j in range(repeat):
        run_multi(myblob.upload, '%d.upload' % j)
        run_multi(myblob.download, '%d.download' % j)
        if not run(myblob.deleteAll):
            error('delete failed')
#======================= test end =======================#

