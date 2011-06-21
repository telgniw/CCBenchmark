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
except (ValueError, IndexError):
    usage()
#==================== parse argv end ====================#

def parse(d, files, key):
    dic = {}
    for f in files:
        num = f.split('.')[0]
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
                data = []
                for l in lines:
                    t = map(int, l.split()[-3:])
                    if len(t) < 3:
                        continue
                    data.append(t)
            except ValueError as e:
                print '%s:' % os.path.join(d, f), e
                continue
            all_data[-1].append(data)
    return all_data, dic

def hist_latency(d, files, key, all_data):
    gcf().clf()
    gcf().set_size_inches(8, 6)

    def expand(d):
        return d[2]-d[1]

    li = []
    for i, num in enumerate(files):
        for data in all_data[i]:
            li += data
    t = map(expand, li)
    hist(t, bins=100000, normed=True, cumulative=True, histtype='step', color='m',
        label='t1~t2: avg=%.0f dev=%.0f' % (avg(t), dev(t)))

    legend(loc='lower right')
    xlabel('time (ms)')
    ylabel('cumulative # data')
    xscale('log'), xlim(xmax=max(t)), ylim([0, 1])
    
    output = os.path.join(d, '%s.latency.hist.png' % key)
    title(output)
    savefig(output, format='PNG')

def hist_finish_time(d, files, key, all_data):
    gcf().clf()
    gcf().set_size_inches(8, 6)

    li = []
    for i, num in enumerate(files):
        for data in all_data[i]:
            mi = min(zip(*data)[0])
            li += [t[2]-mi for t in data]
    hist(li, bins=100000, normed=True, cumulative=True, histtype='step', color='r',
        label='finish time')

    legend(loc='lower right')
    xlabel('time (ms)')
    ylabel('cumulative # data')
    xscale('log'), xlim(xmax=max(li)), ylim([0, 1])

    output = os.path.join(d, '%s.finish.hist.png' % key)
    title(output)
    savefig(output, format='PNG')

#=================== parse data begin ===================#
for dummy, dirs, dummy in os.walk(log_dir):
    break

os.chdir(log_dir)

dic = {}
for d in dirs:
    if not 'myblob-c' in d:
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

        hist_latency(d, files, key, data)
        hist_finish_time(d, files, key, data)
#==================== parse data end ====================#
