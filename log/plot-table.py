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
    def expand(d):
        return [d[1]-d[0], d[2]-d[1]]

    for i, num in enumerate(files):
        gcf().clf()
        gcf().set_size_inches(16, 6)

        li = []
        for data in all_data[i]:
            datb = map(expand, data)
            li += datb
        t, r = zip(*li), range(len(li))
        b0 = bar(r, t[0], color='b', linewidth=0)
        b1 = bar(r, t[1], color='c', bottom=t[0], linewidth=0)

        legend((b0[0], b1[0]), (
            't0~t1: avg=%.0f dev=%.0f' % (avg(t[0]), dev(t[0])),
            't1~t2: avg=%.0f dev=%.0f' % (avg(t[1]), dev(t[1]))
        ))
        xlabel('cumulative # data')
        ylabel('latency (ms)')
        ylim(ymin=0, ymax=80)
    
        output = os.path.join(d, '%s.%s.latency.stat.png' % (key, num))
        title(output)
        savefig(output, format='PNG')

def hist_latency(d, files, key, all_data):
    gcf().clf()
    gcf().set_size_inches(8, 6)

    def expand(d):
        return [d[1]-d[0], d[2]-d[0]]

    li = []
    for i, num in enumerate(files):
        for data in all_data[i]:
            li += data
    t = zip(*map(expand, li))
    h0 = hist(t[0], bins=100, normed=True, range=[0, 100],
        cumulative=True, histtype='step', color='r', label='t0~t1')
    h1 = hist(t[1], bins=100, normed=True, range=[0, 100],
        cumulative=True, histtype='step', color='m', label='t0~t2')

    legend()
    xlabel('latency (ms)')
    ylabel('cumulative # data')
    ylim(ymin=0, ymax=1)

    output = os.path.join(d, '%s.latency.hist.png' % key)
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
        hist_latency(d, files, key, data)
#==================== parse data end ====================#
