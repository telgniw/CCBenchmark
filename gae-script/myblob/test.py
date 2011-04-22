#!/usr/bin/env python

#################################################
# Interface for testing MyBlob.
#################################################
import sys, pycurl, urllib, time
from threading import Thread

host = 'http://yi-testi.appspot.com'

def usage():
    print sys.argv[0], '<init>', '<num>', '<size>', '<b|kb|mb>'
    print sys.argv[0], '<del> [task]'
    print sys.argv[0], '<up|down>', '<num>', '<seq|para>'
    exit()

def init(size, n):
    global host
    curl = pycurl.Curl()
    curl.setopt(pycurl.HTTPGET, 1)
    curl.setopt(pycurl.URL, '%s/myblob/init?%s' % (host, urllib.urlencode({
        'size': size,
        'num': n
    })))
    curl.perform()
    curl.close()

def delete(task):
    global host
    curl = pycurl.Curl()
    curl.setopt(pycurl.HTTPGET, 1)
    if task:
        curl.setopt(pycurl.URL, '%s/newtask?%s' % (host, urllib.urlencode({
            'url': '/myblob/delete'
        })))
    else:
        curl.setopt(pycurl.URL, '%s/myblob/delete' % (host))
    curl.perform()
    curl.close()

def upload(idx):
    global host
    curl = pycurl.Curl()
    curl.setopt(pycurl.POST, 1)
    curl.setopt(pycurl.URL, '%s/myblob/upload' % (host))
    curl.setopt(pycurl.POSTFIELDS, urllib.urlencode({
        'id': idx
    }))
    print 'upload', idx
    curl.perform()
    curl.close()

def download(idx):
    global host
    curl = pycurl.Curl()
    curl.setopt(pycurl.HTTPGET, 1)
    curl.setopt(pycurl.URL, '%s/myblob/download?%s' % (host, urllib.urlencode({
        'id': idx
    })))
    print 'download', idx
    curl.perform()
    curl.close()

class ThreadAction(Thread):
    def __init__(self, idx, action):
        Thread.__init__(self)
        self.idx, self.act = idx, action
    def run(self):
        self.act(self.idx)
        time.sleep(0.01)

class ThreadJoin(Thread):
    def __init__(self, thread_list, n):
        Thread.__init__(self)
        self.thread_list = thread_list
        self.n = n
    def run(self):
        while self.n > 0:
            if len(self.thread_list) > 0:
                self.thread_list[0].join()
                self.n -= 1
            else:
                time.sleep(0.001)

def seq(action, n):
    for i in range(n):
        action(n)

def para(action, n):
    li = []
    joiner = ThreadJoin(li, n)
    joiner.start()
    for i in range(n):
        thread = ThreadAction(i, action)
        thread.start()
        li.append(thread)
    joiner.join()

def parse_num(idx):
    return int(sys.argv[idx])

def parse_size(idx):
    if sys.argv[idx+1] == 'b':
        return int(sys.argv[idx])
    if sys.argv[idx+1] == 'kb':
        return int(sys.argv[idx]) * 1000
    if sys.argv[idx+1] == 'mb':
        return int(sys.argv[idx]) * 1000000

try:
    if sys.argv[1] != 'del':
        num = parse_num(2)

    if sys.argv[1] == 'init':
        size = parse_size(3)
        init(size, num)
    elif sys.argv[1] == 'del':
        if len(sys.argv) > 2:
            delete(True)
        else:
            delete(False)
    elif sys.argv[1] == 'up':
        if sys.argv[3] == 'seq':
            seq(upload, num)
        else:
            para(upload, num)
    elif sys.argv[1] == 'down':
        if sys.argv[3] == 'seq':
            seq(download, num)
        else:
            para(download, num)
except IndexError as ie:
    usage()
