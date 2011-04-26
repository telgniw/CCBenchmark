#!/usr/bin/env python

#################################################
# Plot graph for logs.
#################################################
import sys
from pylab import *

def usage():
    print sys.argv[0], '<output>', '<height>', '<input>..'
    exit()

def error(msg):
    print 'error: %s' % msg
    exit()

def warning(msg):
    print 'warning: %s' % msg

if len(sys.argv) <= 3:
    usage()

fout = open(sys.argv[1], 'w')

max_li, min_li, avg_li = [], [], []
for name in sys.argv[3:]:
    try:
        fin = open(name, 'r')
        lines = fin.readlines()
        fin.close()
    except IOError as ie:
        warning('file does not exist %s' % name)
    n_data = len(lines) >> 1
    data = [lines[(i<<1)+1] for i in range(n_data)]
    t1, t2 = [], []
    for i in range(n_data):
        tmp = data[i].split()
        t1.append(float(tmp[4])), t2.append(float(tmp[5]))
    max_li.append((max(t1), max(t2))), min_li.append((min(t1), min(t2)))
    avg_li.append((sum(t1)/len(t1), sum(t2)/len(t2)))
    fout.write('%8s(t1) max=%f, min=%f, avg=%f\n' % (
        name, max_li[-1][0], min_li[-1][0], avg_li[-1][0]
    ))
    fout.write('%8s(t2) max=%f, min=%f, avg=%f\n' % (
        name, max_li[-1][1], min_li[-1][1], avg_li[-1][1]
    ))

fout.close()

n_data, height = len(sys.argv)-3, int(sys.argv[2])

title(sys.argv[1])
max_li = zip(*max_li)
plot(max_li[0], color='r')
plot(max_li[1], color='g')
min_li = zip(*min_li)
plot(min_li[0], color='b')
plot(min_li[1], color='c')
avg_li = zip(*avg_li)
plot(avg_li[0], color='y')
plot(avg_li[1], color='m')
axis([0, n_data, 0, height])
dy = height / 32
text(0, height-dy, 'max(t1)', color='r')
text(12, height-dy, 'max(t2)', color='g')
text(24, height-dy, 'min(t1)', color='b')
text(36, height-dy, 'min(t2)', color='c')
text(48, height-dy, 'avg(t1)', color='y')
text(60, height-dy, 'avg(t2)', color='m')
savefig('%s.png' % sys.argv[1], format='png')
