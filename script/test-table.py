#!/usr/bin/env python
from common import Logger, error, run
from time import sleep
import sys, os, random

def usage():
    print sys.argv[0], '<log_dir>', '<type>', '<num>', '<size>'
    exit(1)

#=================== parse argv begin ===================#
try:
    log_dir, data_type = sys.argv[1], sys.argv[2]
    table = __import__('table.%s' % data_type, fromlist=['table'])
    num, size = [int(t) for t in sys.argv[3:]]
    os.mkdir(log_dir)
except (OSError, ImportError) as e:
    error(e)
except (ValueError, IndexError):
    usage()
#==================== parse argv end ====================#

# number of data query returns
repeat = 10

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

print '1st phase (get, put)'
for i in range(num):
    print 'i =', i
    run_multi(table.put, (size, i), 'put', i, repeat)

for i in range(num):
    print 'i =', i
    run_multi(table.get, (size, i), 'get', i, repeat)

print '2nd phase (query)'
for i in range(num):
    print 'i =', i
    run_multi(table.query, (size, i), 'query', i, repeat)

if not run(table.deleteAll):
    error('deleteAll failed')
if task:
    sleep(1800)
#======================= test end =======================#

