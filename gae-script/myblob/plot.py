#!/usr/bin/env python

#################################################
# Plot graph for logs.
#################################################
import sys
from pylab import *

def usage():
    print sys.argv[0], '<input>', '<height>'
    exit()

def error(msg):
    print 'error: %s' % msg
    exit()

try:
    fin = open(sys.argv[1], 'r')
    lines = fin.readlines()
    fin.close()
    height = int(sys.argv[2])
except IndexError as ie:
    usage()
except IOError as ie:
    error('file does not exists')

n_data = len(lines) >> 1
data = [(lines[i<<1], lines[(i<<1)+1]) for i in range(n_data)]
data.sort()

def stat_tuple(name, li):
    return (name, max(li), min(li), sum(li)/len(li))

st_time, ed_time = data[0][0][:-1], data[-1][0][:-1]
t1, t2 = [], []
for i in range(n_data):
    tmp = data[i][1].split()
    t1.append(float(tmp[4])), t2.append(float(tmp[5]))

fout = open('%s.stat' % sys.argv[1], 'w')
fout.write('%12s: %s\n' % ('file', sys.argv[1]))
fout.write('%12s: %s\n' % ('start', st_time))
fout.write('%12s: %s\n' % ('end', ed_time))
fout.write('%12s: %d\n' % ('# data', n_data))
fout.write('%12s: max=%f, min=%f, avg=%f\n' % stat_tuple('t1', t1))
fout.write('%12s: max=%f, min=%f, avg=%f\n' % stat_tuple('t2', t2))

title(sys.argv[1])
plot(t1, color='r')
plot(t2, color='g')
axis([0, n_data, 0, height])
dx, dy = n_data / 128, height / 32
text(dx, height-dy*2, '%s ~ %s' % (st_time, ed_time))
text(dx, height-dy*3, '%2s: max=%f, min=%f, avg=%f' % stat_tuple('t1', t1), color='r')
text(dx, height-dy*4, '%2s: max=%f, min=%f, avg=%f' % stat_tuple('t2', t2), color='g')
savefig('%s.png' % sys.argv[1], format='png')
