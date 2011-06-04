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

    total, colors = 0, [['c', 'y'], ['b', 'g']]
    for i, num in enumerate(files):
        li = []
        for data in all_data[i]:
            datb = map(expand, data)
            t = zip(*datb)
            li.append([avg(t[0]), dev(t[0]), avg(t[1]), dev(t[1])])
        t, r = zip(*li), range(total, total+len(li), 1)
        bar(r, t[0], color=colors[i%2][0])
        bar(r, t[2], color=colors[i%2][1], bottom=t[0])
        total += len(li)
    n_nums, nums = len(files), files.keys()
    width = float(total) / n_nums
    xticks(arange(n_nums)*width + width*.5, nums)
    xlabel('# data %sed concurrently' % key)
    ylabel('average latency (ms)')
    
    output = os.path.join(d, '%s.latency.stat.png' % key)
    title(output)
    savefig(output, format='PNG')

def plot_throughput(d, files, key, all_data):
    gcf().clf()
    gcf().set_size_inches(8, 6)

    total, throu = 0, []
    for i, num in enumerate(files):
        li = []
        for data in all_data[i]:
            t = zip(*data)
            li.append((max(t[2])-min(t[0]))/len(data))
        r = range(total, total+len(li), 1)
        bar(r, li, color='m')
        total += len(li)
        throu.append(avg(li))
    n_nums, nums = len(files), files.keys()
    width = float(total) / n_nums

    r, t = arange(n_nums+1)*width, throu + [0]
    plot(r, t, color='r', drawstyle='steps-post')

    r = arange(n_nums)*width
    xticks(r+width*.5, nums)
    xlabel('# data %sed concurrently' % key)
    ylabel('average time per data (ms)')

    output = os.path.join(d, '%s.throughput.stat.png' % key)
    title(output)
    savefig(output, format='PNG')

def plot_duration(d, files, key, all_data):
    def expand(d):
        return [d[0]-mi, d[2]-mi]

    for i, num in enumerate(files):
        gcf().clf()
        gcf().set_size_inches(8, 12)

        total, colors = 0, ['c', 'b']
        for j, data in enumerate(all_data[i]):
            mi = min(zip(*data)[0])
            datb = map(expand, data)
            t = zip(*datb)
            r = range(total, total+len(data), 1)
            barh(r, t[1], left=t[0], color=colors[j%2], linewidth=0)
            text(400, avg(r), 'max=%d' % max(t[1]), color='k')
            total += len(data)
        xlabel('duration (ms)')
        ylabel('# data %sed concurrently' % key)
        xlim(xmax=500)

        output = os.path.join(d, '%s.%s.duration.stat.png' % (key, num))
        title(output)
        savefig(output, format='PNG')

#=================== parse data begin ===================#
for dummy, dirs, dummy in os.walk(log_dir):
    break

os.chdir(log_dir)

dic = {}
for d in dirs:
    if not 'myblob' in d:
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
        plot_throughput(d, files, key, data)
        plot_duration(d, files, key, data)
#==================== parse data end ====================#
