#!/usr/bin/env python

#################################################
# Interface for testing MyBlob.
#################################################
import sys, pycurl, urllib, time
from threading import Thread

host = 'http://yi-testi.appspot.com'

def usage():
    print sys.argv[0], '<init>', '<num>', '<size>', '<b|kb|mb>'
    print sys.argv[0], '<delete>'
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

def delete():
    global host
    curl = pycurl.Curl()
    curl.setopt(pycurl.HTTPGET, 1)
    curl.setopt(pycurl.URL, '%s/newtask?%s' % (host, urllib.urlencode({
        'url': '/myblob/delete'
    })))
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
    curl.perform()
    curl.close()

def download(idx):
    global host
    curl = pycurl.Curl()
    curl.setopt(pycurl.HTTPGET, 1)
    curl.setopt(pycurl.URL, '%s/myblob/download?%s' % (host, urllib.urlencode({
        'id': idx
    })))
    curl.perform()
    curl.close()

class ThreadUpload(Thread):
    def __init__(self, idx):
        Thread.__init__(self)
        self.idx = idx
    def run(self):
        upload(self.idx)
        print 'uploading', self.idx
        time.sleep(0.01)

class ThreadDownload(Thread):
    def __init__(self, idx):
        Thread.__init__(self)
        self.idx = idx
    def run(self):
        downlaod(self.idx)
        print 'downloading', self.idx
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

def para(threadClass, n):
    li = []
    joiner = ThreadJoin(li, n)
    joiner.start()
    for i in range(n):
        thread = threadClass(i)
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
    if sys.argv[1] != 'delete':
        num = parse_num(2)

    if sys.argv[1] == 'init':
        size = parse_size(3)
        init(size, num)
    elif sys.argv[1] == 'delete':
        delete()
    elif sys.argv[1] == 'upload':
        if sys.argv[5] == 'seq':
            seq(upload, n)
        else:
            para(upload, n)
    elif sys.argv[1] == 'download':
        if sys.argv[5] == 'seq':
            seq(download, n)
        else:
            para(download, n)
except IndexError as ie:
    usage()
