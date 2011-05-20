#!/usr/bin/env python
from common import Logger
from pylab import *
import myblob, sys, os

def usage():
    print sys.argv[0], '<log_dir>', '<num>', '<size>', '<offset>'
    exit(1)

def error(msg):
    print 'Error:', msg
    exit(1)

try:
    log_dir = sys.argv[1]
    num, size, offset = [int(t) for t in sys.argv[2:]]
    os.mkdir(log_dir)
except OSError as e:
    error(e)
except (ValueError, IndexError):
    usage()

def run(func, args=()):
    t = func(*args)
    t.start()
    t.join()
    res = t.get()
    print res
    return 'SUCCESS' in res

def run_multi(func, name):
    log_name = os.path.join(log_dir, '%d.%s.log' % (i, name))
    log = Logger(strm=open(log_name, 'w'), listed=True)
    li = []
    for j in range(i):
        li.append(func(j))
    for j in range(i):
        li[j].start()
    for j in range(i):
        li[j].join()
        log.log(li[j].get())
    return log.get()

#====================== test begin ======================#
if not run(myblob.init, (num, size)):
    error('init failed')

upload_log, download_log = [], []

for i in range(offset, num+1, offset):
    print 'i =', i
    upload_log += run_multi(myblob.upload, 'upload')
    download_log += run_multi(myblob.download, 'download')
    if not run(myblob.deleteAll):
        error('delete failed')
#======================  test end  ======================#

def parse_log(log_list):
    log_list = [map(int, t.split()[-3:]) for t in log_list]
    min_st = min(log_list)[0]
    duration = [(t[-1]-t[0], t[-1]-t[1]) for t in log_list]
    interval = [(t[0]-min_st, t[-1]-min_st) for t in log_list]
    return duration, interval

#====================== plot begin ======================#
gcf().set_size_inches(16, 6)


#======================  plot end  ======================#

