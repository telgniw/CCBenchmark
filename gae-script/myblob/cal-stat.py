#!/usr/bin/env python

#################################################
# Plot graph for logs.
#################################################
import sys, re
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

def my_cmp(l, r):
    l, r = l.split('/')[-1].split('.')[0], r.split('/')[-1].split('.')[0]
    return cmp(int(l), int(r))

file_list = sys.argv[3:]
file_list.sort(my_cmp)

def to_float(s):
    return float(''.join(s.split(',')))

fout = open(sys.argv[1], 'w')

r = [0, 0, 1, 1]
clf()
gcf().set_size_inches(8, 6)
ax1 = axes(r)
ax1.xaxis.tick_bottom(), ax1.yaxis.tick_right()

max_li, min_li, avg_li, throughput = [], [], [], []
for j, name in enumerate(file_list):
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
        st.append(to_float(tmp[6])/1000), ed.append(to_float(tmp[7])/1000)
    duration = max(ed)-min(st)
    li = [1/(ed[i]-st[i]) for i in range(n_data)]
    dev = (sum([t*t for t in li])/len(li)-((sum(li)/len(li))**2))**0.5
    plot([j, j], [n_data/duration-dev, n_data/duration+dev], marker='_',
        markersize=10, color='c')
    max_li.append((max(t1), max(t2))), min_li.append((min(t1), min(t2)))
    avg_li.append((sum(t1)/len(t1), sum(t2)/len(t2)))
    throughput.append(n_data/duration)
    fout.write('%12s(t1) max=%f, min=%f, avg=%f\n' % (
        name, max_li[-1][0], min_li[-1][0], avg_li[-1][0]))
    fout.write('%12s(t2) max=%f, min=%f, avg=%f\n' % (
        name, max_li[-1][1], min_li[-1][1], avg_li[-1][1]))
    fout.write('%12s(throughput) %f\n' % (name, n_data/duration))

avg_throughput = sum(throughput)/len(throughput)
dev_throughput = (sum([t**2 for t in throughput]) / len(throughput) -
    avg_throughput**2)**0.5

fout.write('%12s max=%f, min=%f, avg=%f, dev=%f\n' % ('throughput',
    max(throughput), min(throughput), avg_throughput, dev_throughput))

fout.close()
plot(throughput, color='b', linewidth=2)

n_data, height = len(sys.argv)-3, int(sys.argv[2])

ax2 = axes(r, frameon=False)
ax2.xaxis.tick_top(), ax2.yaxis.tick_left()
hist(throughput, bins=1000, cumulative=True, normed=True, linewidth=2,
    histtype='step', color='r')
dev1, dev2 = avg_throughput+dev_throughput, avg_throughput+dev_throughput*2
plot([dev1, dev1], [0, 1], color='pink', linestyle='--')
plot([dev2, dev2], [0, 1], color='plum', linestyle='--')
xlim([0, max(throughput)-1])
suptitle(sys.argv[1])
savefig('%s.throughput.png' % sys.argv[1], format='png',
    bbox_inches='tight')

clf()
gcf().set_size_inches(8, 6)
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
title(sys.argv[1])
savefig('%s.png' % sys.argv[1], format='png', bbox_inches='tight')
