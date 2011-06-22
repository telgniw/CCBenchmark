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

def parse(files, key):
    dic = {}
    for d, f in files:
        num = f.split('.')[0]
        if not num in dic:
            dic[num] = []
        dic[num].append((d, f))

    all_data = []
    for i, num in enumerate(dic):
        all_data.append([])
        for d, f in dic[num]:
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

def hist_latency(files, key, all_data):
    gcf().clf()
    gcf().set_size_inches(8, 6)

    def expand(d):
        return d[2]-d[1]

    dic = {}
    for i, num in enumerate(files):
        for j, (d, f) in enumerate(files[num]):
            try:
                datb = map(expand, all_data[i][j])
            except IndexError as e:
                print '%s:' % os.path.join(d, f), e
                continue
            if not d in dic:
                dic[d] = []
            dic[d] += datb

    xmax = []
    for i, d in enumerate(dic):
        ds = d.split('-')
        if len(ds[-1]) == 1:
            num, size = ds[-3:-1]
        else:
            num, size = ds[-2:]
        li, total = dic[d], len(dic[d])
        r, ax = range(total), axes()
        hist(li, bins=100000, normed=True, cumulative=True, histtype='step',
            color=(random(), random(), random()), label='num=%s, size=%s' % (num, size))
        xmax.append(max(li))

    legend(loc='lower right')
    xlabel('time (ms)')
    ylabel('cumulative # data')
    if log(min(xmax)) > 2:
        xscale('log'), xlim(xmin=1)
    xlim(xmax=min(xmax)), ylim([0, 1])
    
    output = 'all.%s.latency.hist.png' % key
    title(output)
    savefig(output, format='PNG')

def plot_throughput(files, key, all_data):
    gcf().clf()
    gcf().set_size_inches(8, 6)

    throu = {}
    for i, num in enumerate(files):
        dic = {}
        for j, (d, f) in enumerate(files[num]):
            try:
                t = zip(*all_data[i][j])
            except IndexError as e:
                print '%s:' % os.path.join(d, f), e
                continue
            if not d in dic:
                dic[d] = []
            dic[d].append((max(t[2])-min(t[0]))/len(all_data[i][j]))
        for d in dic:
            if not d in throu:
                throu[d] = []
            throu[d].append(avg(dic[d]))

    for i, d in enumerate(dic):
        ds = d.split('-')
        if len(ds[-1]) == 1:
            num, size = ds[-3:-1]
        else:
            num, size = ds[-2:]
        li, total = throu[d] + [0], len(throu[d]) + 1
        r, ax = range(total), axes()
        plot(r, li, color=(random(), random(), random()), drawstyle='steps-post',
            label='num=%s size=%s' % (num, size))
    
    legend(loc='upper right')
    xticks(r, files.keys())
    xlabel('# data %sed concurrently' % key)
    ylabel('average time per data (ms)')

    output = 'all.%s.throught.stat.png' % key
    title(output)
    savefig(output, format='PNG')
#=================== parse data begin ===================#
for dummy, dirs, dummy in os.walk(log_dir):
    break

os.chdir(log_dir)

def generate_dic(cond):
    dic = {}
    for d in dirs:
        if cond(d):
            continue
        for dummy, dummy, files in os.walk(d):
            break
        for f in files:
            key, ext = f.split('.')[-2:]
            if ext != 'log':
                continue
            if not key in dic:
                dic[key] = []
            dic[key].append((d, f))
    return dic

dic = generate_dic(lambda d: 'myblob-c' in d or not 'myblob' in d)
for key in dic:
    dic[key].sort(fname_cmp)
    data, files = parse(dic[key], key)

    plot_throughput(files, key, data)

dic = generate_dic(lambda d: not 'myblob-c' in d)
for key in dic:
    dic[key].sort(fname_cmp)
    data, files = parse(dic[key], key)

    hist_latency(files, key, data)

dic = generate_dic(lambda d: not 'table' in d)
for key in dic:
    dic[key].sort(fname_cmp)
    data, files = parse(dic[key], key)

    hist_latency(files, key, data)
#==================== parse data end ====================#
