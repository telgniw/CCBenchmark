#!/usr/bin/env python
from common import Logger, error, run
from time import sleep
import sys, os, random

def usage():
    print sys.argv[0], '<log_dir>', '<type>', '<num>', '<size>', '<repeat>'
    exit(1)

#=================== parse argv begin ===================#
try:
    log_dir, data_type = sys.argv[1], sys.argv[2]
    table = __import__('table.%s' % data_type, fromlist=['table'])
    num, size, repeat = [int(t) for t in sys.argv[3:]]
    os.mkdir(log_dir)
except (OSError, ImportError) as e:
    error(e)
except (ValueError, IndexError):
    usage()
#==================== parse argv end ====================#

# number of data query returns
n_data = 10

def run_multi(func, args, name, i, repeat):
    log_name = os.path.join(log_dir, '%d.%s.log' % (i, name))
    log = Logger(strm=open(log_name, 'w'))
    for j in range(repeat):
        t = func(*args)
        t.start()
        t.join()
        log.log(t.get())
    del log

#====================== test begin ======================#
task = True

for j in range(repeat):
    print '1st phase (get, put)'
    for i in range(num):
        print 'i =', i
        run_multi(table.put, (size, i), '%d.put' % j, i, n_data)
        run_multi(table.get, (size, i), '%d.get' % j, i, n_data)

    print '2nd phase (query)'
    for i in range(num):
        print 'i =', i
        run_multi(table.query, (size, i), '%d.query' % j, i, n_data)

    if not run(table.deleteAll):
        error('deleteAll failed')
    if task:
        sleep(1800)
#======================= test end =======================#

