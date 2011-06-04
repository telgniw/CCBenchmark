#!/usr/bin/env python

def error(msg):
    print 'Error:', msg
    exit(1)

def fname_cmp(a, b):
    return cmp(map(int, a.split('.')[:2]), map(int, b.split('.')[:2]))

def avg(li):
    return float(sum(li))/len(li)

def dev(li):
    return (avg([t**2 for t in li]) - avg(li)**2)**0.5

