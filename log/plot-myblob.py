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

def plot_latency(d, files, key, all_data):
    gcf().clf()
    gcf().set_size_inches(8, 6)

    def expand(d):
        return [d[1]-d[0], d[2]-d[1]]

    li = []
    for i, num in enumerate(files):
        left = len(li)
        for data in all_data[i]:
            datb = map(expand, data)
            t = zip(*datb)
            li.append([avg(t[0]), avg(t[1])])
        right = len(li)
        axvspan(left, right, facecolor='y', alpha=0.25*(i%2+1))
    t, total = zip(*li), len(li)
    r = range(total)
    bar(r, t[0], color='b', label='t0~t1: avg=%.0f dev=%.0f' % (avg(t[0]), dev(t[0])))
    bar(r, t[1], bottom=t[0], color='c', label='t1~t2: avg=%.0f dev=%.0f' % (avg(t[1]), dev(t[1])))

    n_nums, nums = len(files), files.keys()
    width = float(total) / n_nums

    legend(loc='upper right')
    xticks(arange(n_nums)*width + width*.5, nums)
    xlabel('# data %sed concurrently' % key)
    ylabel('average latency (ms)')
    xlim(xmax=total), ylim(ymax=100)
    
    output = os.path.join(d, '%s.latency.stat.png' % key)
    title(output)
    savefig(output, format='PNG')

def plot_throughput(d, files, key, all_data):
    gcf().clf()
    gcf().set_size_inches(8, 6)

    li, throu = [], []
    for i, num in enumerate(files):
        left, t_li = len(li), []
        for data in all_data[i]:
            t = zip(*data)
            t_li.append((max(t[2])-min(t[0]))/len(data))
        li += t_li
        throu.append(avg(t_li))
        right = len(li)
        axvspan(left, right, facecolor='y', alpha=0.25*(i%2+1))
    total = len(li)
    r = range(total)
    bar(r, li, color='m', label='throughput per test')

    n_nums, nums = len(files), files.keys()
    width = float(total) / n_nums

    r, t = arange(n_nums+1)*width, throu + [0]
    plot(r, t, color='r', drawstyle='steps-post', label='average')

    legend(loc='upper right')
    xticks((arange(n_nums)+.5)*width, nums)
    xlabel('# data %sed concurrently' % key)
    ylabel('average time per data (ms)')
    xlim(xmax=total), ylim(ymax=100)

    output = os.path.join(d, '%s.throughput.stat.png' % key)
    title(output)
    savefig(output, format='PNG')

def plot_duration(d, files, key, all_data):
    def expand(d):
        return [d[1]-mi, d[2]-mi]

    for i, num in enumerate(files):
        gcf().clf()
        gcf().set_size_inches(8, 12)

        li = []
        for j, data in enumerate(all_data[i]):
            left = len(li)
            mi = min(zip(*data)[1])
            datb = map(expand, data)
            li += datb
            right = len(li)
            axhspan(left, right, facecolor='y', alpha=0.25*(j%2+1))
        t, total = zip(*li), len(li)
        r = range(total)
        barh(r, t[1], left=t[0], color='b', linewidth=0, log=True,
            label='duration')

        legend(loc='upper right')
        xlabel('time (ms)')
        ylabel('# data %sed concurrently' % key)
        xlim(xmin=1), ylim(ymax=total)

        output = os.path.join(d, '%s.%s.duration.stat.png' % (key, num))
        title(output)
        savefig(output, format='PNG')

#=================== parse data begin ===================#
for dummy, dirs, dummy in os.walk(log_dir):
    break

os.chdir(log_dir)

for d in dirs:
    if 'myblob-c' in d or not 'myblob' in d:
        continue
    for dummy, dummy, files in os.walk(d):
        break
    dic = {}
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
