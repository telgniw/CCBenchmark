#!/usr/bin/env python

def error(msg):
    print 'Error:', msg
    exit(1)

def fname_cmp(a, b):
    if type(a) == tuple and type(b) == tuple:
        return fname_cmp(a[1], b[1])
    return cmp(map(int, a.split('.')[:2]), map(int, b.split('.')[:2]))

def avg(li):
    return float(sum(li))/len(li)

def dev(li):
    return (avg([t**2 for t in li]) - avg(li)**2)**0.5

