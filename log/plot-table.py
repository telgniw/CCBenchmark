#!/usr/bin/env python
from pylab import *
import sys, os

def usage():
    print sys.argv[0], '<log_dir>'
    exit(1)

def error(msg):
    print 'Error:', msg
    exit(1)

#=================== parse argv begin ===================#
try:
    log_dir = sys.argv[1]
    os.stat(log_dir)
except OSError as e:
    error(e)
except ValueError:
    usage()
#==================== parse argv end ====================#

def fname_cmp(a, b):
    return cmp(map(int, a.split('.')[:2]), map(int, b.split('.')[:2]))

def avg(li):
    return float(sum(li))/len(li)

def dev(li):
    return (avg([t**2 for t in li]) - avg(li)**2)**0.5

def parse(d, files, key):
    all_data = []
    for f in files:
        with open(os.path.join(d, f)) as fin:
            lines = fin.readlines()
        try:
            data = [map(int, l.split()[-3:]) for l in lines]
        except ValueError as e:
            print '%s:' % os.path.join(d, f), e
            continue
        all_data.append(data)
    return all_data

def plot_latency(d, files, key, all_data):
    gcf().clf()
    gcf().set_size_inches(8, 6)

    def expand(d):
        return [d[1]-d[0], d[2]-d[1]]

    total, colors = 0, [['c', 'y'], ['b', 'g']]
    for i, f in enumerate(files):
        data = all_data[i]
        datb = map(expand, data)
        t, r = zip(*datb), range(total, total+len(data), 1)
        bar(r, t[0], color=colors[i%2][0])
        bar(r, t[1], color=colors[i%2][1], bottom=t[0])

    xlabel('cumulative # data (%s)' % key)
    ylabel('latency (ms)')
    
    output = os.path.join(d, '%s.latency.stat.png' % key)
    title(output)
    savefig(output, format='PNG')

#=================== parse data begin ===================#
for dummy, dirs, dummy in os.walk(log_dir):
    break

os.chdir(log_dir)

dic = {}
for d in dirs:
    if not 'table' in d:
        continue
    for dummy, dummy, files in os.walk(d):
        break
    for f in files:
        key, ext = f.split('.')[-2:]
        if ext != 'log':
            continue
        if not key in dic:
            dic[key] = []
        dic[key].append(f)
    for key in dic:
        dic[key].sort(fname_cmp)
        data = parse(d, dic[key], key)

        plot_latency(d, dic[key], key, data)
#==================== parse data end ====================#
