#!/usr/bin/env python
from common import Logger
import myblob, sys, os

def usage():
    print sys.argv[0], '<log_dir>', '<num>', '<size>', '<offset>'
    exit(1)

try:
    log_dir, num, size, offset = [int(t) for t in sys.argv[1:]]
except ValueError:
    usage()

def run(func, args=()):
    t = func(*args)
    t.start()
    t.join()
    print t.get()

def run_multi(func, name):
    log = Logger(strm=open(os.path.join(log_dir, '%d.%s.log' % (i, name))))
    li = []
    for j in range(i):
        li.append(func(j))
    for j in range(i):
        li[j].start()
    for j in range(i):
        li[j].join()
        log.log(li[j].get())
    del log

run(myblob.init, (num, size))

for i in range(0, num, offset):
    run_multi(myblob.upload, 'upload')
    run_multi(myblob.download, 'download')
    run(myblob.deleteAll)

