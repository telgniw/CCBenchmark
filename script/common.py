#!/usr/bin/env python
from datetime import datetime
from threading import Thread
from StringIO import StringIO
import pycurl, urllib, sys, time

def error(msg):
    print 'Error:', msg
    exit(1)

host = 'http://yi-testi.appspot.com'

class ThreadAction(Thread):
    """
        A thread that performs a HTTPGET request using PycURL.
    """
    def __init__(self, url, args=None, task=False):
        """
            Initialize the cURL object.
        """
        Thread.__init__(self)
        self.curl = pycurl.Curl()
        self.curl.setopt(pycurl.HTTPGET, 1)

        global host
        if args:
            url = '%s?%s' % (url, urllib.urlencode(args))
        if task:
            self.curl.setopt(pycurl.URL, '%s%s?%s' % (
                host, '/newtask', urllib.urlencode({'url': url})))
        else:
            self.curl.setopt(pycurl.URL, '%s%s' % (host, url))

        self.buf = StringIO()
        self.curl.setopt(pycurl.WRITEFUNCTION, self.buf.write)

    def __del__(self):
        """
            Close the cURL object.
        """
        self.buf.close()
        self.curl.close()

    def run(self):
        """
            Run the cURL object.
        """
        self.curl.perform()
        time.sleep(0.01)

    def get(self):
        """
            Return the response message.
        """
        return self.buf.getvalue()

class Logger(object):
    """
        A simple logger.
    """
    def __init__(self, strm=sys.stderr, listed=False):
        """
            Initialize logger output stream.
        """
        self.out, self.listed = strm, listed
        if self.listed:
            self.log_list = []

    def __del__(self):
        """
            Close logger output stream.
        """
        self.out.close()

    def log(self, msg=''):
        """
            Automatically add a newline after log message.
        """
        if self.listed:
            self.log_list.append(msg)
        self.out.write(msg)
        self.out.write('\n')

    def time(self):
        self.out.write('###%s###' % datetime.now())
        self.out.write('\n')

    def get(self):
        return self.log_list

def run(func, args=()):
    t = func(*args)
    t.start()
    t.join()
    res = t.get()
    print res
    return 'SUCCESS' in res

