#!/usr/bin/env python
from datetime import datetime
from threading import Thread
from StringIO import StringIO
import pycurl, urllib, sys

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

        self.response = None

    def __del__(self):
        """
            Close the cURL object.
        """
        self.curl.close()

    def run(self):
        """
            Run the cURL and store the response message.
        """
        buf = StringIO()
        self.curl.setopt(pycurl.WRITEFUNCTION, buf.write)
        self.curl.perform()
        self.response = buf.getvalue()
        buf.close()

    def get(self):
        """
            Return the response message.
        """
        return self.response

class Logger(object):
    """
        A simple logger.
    """
    def __init__(self, strm=sys.stderr):
        """
            Initialize logger output stream.
        """
        self.out = strm

    def __del__(self):
        """
            Close logger output stream.
        """
        self.out.close()

    def log(self, msg=''):
        """
            Automatically add a newline after log message.
        """
        self.out.write(msg)
        self.out.write('\n')

