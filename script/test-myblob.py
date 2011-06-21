#!/usr/bin/env python
from common import Logger, error, run
from time import sleep
import myblob, sys, os

def usage():
    print sys.argv[0], '<log_dir>', '<task>', '<num>', '<size>', '<off_t>', '<repeat>'
    exit(1)

#=================== parse argv begin ===================#
try:
    log_dir, task = sys.argv[1], bool(int(sys.argv[2]))
    num, size, off_t, repeat = [int(t) for t in sys.argv[3:]]
    os.mkdir(log_dir)
except OSError as e:
    error(e)
except (ValueError, IndexError):
    usage()
#==================== parse argv end ====================#

def run_multi(func, name, i):
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
print 'task =', task

if not run(myblob.init, (num, size, task)):
    run(myblob.deleteAll, (task,))
    error('init failed')
if task:
    sleep(600)

for i in range(off_t, num+1, off_t):
    print 'i =', i
    for j in range(repeat):
        run_multi(myblob.upload, '%d.upload' % j, i)
        run_multi(myblob.download, '%d.download' % j, i)
        if not run(myblob.deleteAll, (task,)):
            error('deleteAll failed')
        if task:
            sleep(300)
#======================= test end =======================#

