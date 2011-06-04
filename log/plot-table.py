#!/usr/bin/env python
from common import *
from pylab import *
import sys, os

def usage():
    print sys.argv[0], '<log_dir>'
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

def parse(d, files, key):
    dic = {}
    for f in files:
        num = f.split('.')[-3]
        if not num in dic:
            dic[num] = []
        dic[num].append(f)

    all_data = []
    for i, num in enumerate(dic):
        all_data.append([])
        for f in dic[num]:
            with open(os.path.join(d, f)) as fin:
                lines = fin.readlines()
            try:
                data = [map(int, l.split()[-3:]) for l in lines]
            except ValueError as e:
                print '%s:' % os.path.join(d, f), e
                continue
            all_data[-1].append(data)
    return all_data, dic

def plot_latency(d, files, key, all_data):
    gcf().clf()
    gcf().set_size_inches(8, 6)

    def expand(d):
        return [d[1]-d[0], d[2]-d[1]]

    total = 0
    for i, num in enumerate(files):
        li = []
        for data in all_data[i]:
            datb = map(expand, data)
            t = zip(*datb)
            li.append([avg(t[0]), dev(t[0]), avg(t[1]), dev(t[1])])
        t, r = zip(*li), range(total, total+len(li), 1)
        bar(r, t[0], color='b')
        bar(r, t[2], color='c', bottom=t[0], yerr=t[3], ecolor='r')
        total += len(li)
    xlabel('test # (%s)' % key)
    ylabel('average latency (ms)')
    ylim(ymin=0)

    output = os.path.join(d, '%s.latency.stat.png' % key)
    title(output)
    savefig(output, format='PNG')

def plot_latency_each(d, files, key, all_data):
    def expand(d):
        return [d[1]-d[0], d[2]-d[1]]

    for i, num in enumerate(files):
        gcf().clf()
        gcf().set_size_inches(8, 6)

        total = 0
        for data in all_data[i]:
            datb = map(expand, data)
            t, r = zip(*datb), range(total, total+len(data), 1)
            bar(r, t[0], color='b')
            bar(r, t[1], color='c', bottom=t[0])
            total += len(data)
        xlabel('cumulative # data (%s)' % key)
        ylabel('latency (ms)')
    
        output = os.path.join(d, '%s.%s.latency.stat.png' % (key, num))
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
        data, files = parse(d, dic[key], key)

        plot_latency(d, files, key, data)
        plot_latency_each(d, files, key, data)
#==================== parse data end ====================#
