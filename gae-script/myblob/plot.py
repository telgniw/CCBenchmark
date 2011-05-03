#!/usr/bin/env python

#################################################
# Plot graph for logs.
#################################################
import sys
from pylab import *

def usage():
    print sys.argv[0], '<input>', '<height>', '<size>'
    exit()

def error(msg):
    print 'error: %s' % msg
    exit()

try:
    fin = open(sys.argv[1], 'r')
    lines = fin.readlines()
    fin.close()
    height = int(sys.argv[2])
    data_size = int(sys.argv[3])
except IndexError as ie:
    usage()
except IOError as ie:
    error('file does not exists')

n_data = len(lines) >> 1
data = [(lines[i<<1], lines[(i<<1)+1]) for i in range(n_data)]
data.sort()

def to_float(s):
    return float(''.join(s.split(',')))

def stat_tuple(name, li):
    return (name, max(li), min(li), sum(li)/len(li))

st_time, ed_time = data[0][0][:-1], data[-1][0][:-1]
t1, t2, st, ed = [], [], [], []
for i in range(n_data):
    tmp = data[i][1].split()
    t1.append(float(tmp[4])), t2.append(float(tmp[5]))
    st.append(to_float(tmp[6])), ed.append(to_float(tmp[7]))

duration, total_size = max(ed)-min(st), data_size*n_data

fout = open('%s.stat' % sys.argv[1], 'w')
fout.write('%12s: %s\n' % ('file', sys.argv[1]))
fout.write('%12s: %s\n' % ('start', st_time))
fout.write('%12s: %s\n' % ('end', ed_time))
fout.write('%12s: %d\n' % ('# data', n_data))
fout.write('%12s: max=%f, min=%f, avg=%f\n' % stat_tuple('t1', t1))
fout.write('%12s: max=%f, min=%f, avg=%f\n' % stat_tuple('t2', t2))
fout.write('%12s: %fbytes\n' % ('total size', int(total_size)))
fout.write('%12s: %dms\n' % ('duration', int(duration)))
fout.write('%12s: %fbytes/s\n' % (
    'throughput', total_size*1000/duration))

title(sys.argv[1])
plot(t1, color='r')
plot(t2, color='g')
axis([0, n_data-1, 0, height])
dx, dy = n_data / 128, height / 32
text(dx, height-dy*2, '%s ~ %s' % (st_time, ed_time))
text(dx, height-dy*3, '%2s: max=%f, min=%f, avg=%f' % stat_tuple('t1', t1), color='r')
text(dx, height-dy*4, '%2s: max=%f, min=%f, avg=%f' % stat_tuple('t2', t2), color='g')
savefig('%s.png' % sys.argv[1], format='png')
