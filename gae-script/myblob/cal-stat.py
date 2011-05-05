#!/usr/bin/env python

#################################################
# Plot graph for logs.
#################################################
import sys, re
from pylab import *

def usage():
    print sys.argv[0], '<output>', '<height>', '<size>', '<input>..'
    exit()

def error(msg):
    print 'error: %s' % msg
    exit()

def warning(msg):
    print 'warning: %s' % msg

if len(sys.argv) <= 4:
    usage()

fout = open(sys.argv[1], 'w')
n_data, height = len(sys.argv)-3, int(sys.argv[2])
data_size = int(sys.argv[3])

def to_float(s):
    return float(''.join(s.split(',')))

max_li, min_li, avg_li, thr = [], [], [], []
for name in sys.argv[4:]:
    try:
        fin = open(name, 'r')
        lines = fin.readlines()
        fin.close()
    except IOError as ie:
        warning('file does not exist %s' % name)
    n_data, data, tmp = 0, [], ''
    for line in lines:
        if re.match('^\[.*\]$', line) is not None:
            tmp = line
        else:
            if not tmp:
                continue
            data.append(line)
            n_data, tmp = n_data+1, ''
    if n_data == 0:
        continue
    t1, t2, st, ed = [], [], [], []
    for i in range(n_data):
        tmp = data[i].split()
        t1.append(float(tmp[4])), t2.append(float(tmp[5]))
        st.append(to_float(tmp[6])), ed.append(to_float(tmp[7]))
    max_li.append((max(t1), max(t2))), min_li.append((min(t1), min(t2)))
    avg_li.append((sum(t1)/len(t1), sum(t2)/len(t2)))
    duration, total_size = max(ed)-min(st), data_size*n_data
    throughput = total_size/duration*1000
    thr.append(throughput)
    fout.write('%8s(t1) max=%f, min=%f, avg=%f\n' % (
        name, max_li[-1][0], min_li[-1][0], avg_li[-1][0]))
    fout.write('%8s(t2) max=%f, min=%f, avg=%f\n' % (
        name, max_li[-1][1], min_li[-1][1], avg_li[-1][1]))
    fout.write('%8s(duration) %dms\n' % (name, duration))
    fout.write('%8s(total size) %dbytes\n' % (name, total_size))
    fout.write('%8s(throughput) %fbytes/s\n' % (
        name, throughput))

fout.close()

clf()
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
axis([0, n_data-1, 0, height])
dy = height / 32
text(0, height-dy*1, 'max(t1)', color='r')
text(0, height-dy*2, 'max(t2)', color='g')
text(0, height-dy*3, 'min(t1)', color='b')
text(0, height-dy*4, 'min(t2)', color='c')
text(0, height-dy*5, 'avg(t1)', color='y')
text(0, height-dy*6, 'avg(t2)', color='m')
savefig('%s.png' % sys.argv[1], format='png')

clf()
title(sys.argv[1] + ':throughput')
plot(thr, color='k')
savefig('%s.throughput.png' % sys.argv[1], format='png')
