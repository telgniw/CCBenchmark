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

# set the limit to prevent table.init timeout
off_t = 10

# number of tests to be performed
n_tests = num/10

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
seed_list = [random.choice(range(num)) for t in range(n_tests)]

print '1st phase (get, put)'
for i in range(off_t, num+1, off_t):
    if not run(table.init, tuple(i, 1, size, 0, task)):
        run(table.deleteAll, tuple(task))
        error('init failed')
    if task:
        sleep(600)

for i, seed in enumerate(seed_list):
    print 'i =', i, ', seed =', seed
    run_multi(table.get, tuple(size, seed), 'get', i, repeat)
    run_multi(table.put, tuple(size, seed), 'put', i, repeat)
    if not run(table.delete, tuple(repeat, size, seed)):
        run(table.deleteAll, tuple(task))
        error('delete failed')
    if task:
        sleep(600)

print '2nd phase (query)'
for i in range(off_t, num+1, off_t):
    if not run(table.init, tuple(i, 9, size, 0, task)):
        run(table.deleteAll, tuple(task))
        error('init failed')
    if task:
        sleep(600)

for i, seed in enumerate(seed_list):
    print 'i =', i, ', seed =', seed
    run_multi(table.query, tuple(size, seed), 'query', i, repeat)

if not run(table.deleteAll):
    error('deleteAll failed')
if task:
    sleep(600)
#======================= test end =======================#

