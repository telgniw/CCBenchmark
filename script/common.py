#!/usr/bin/env python
from threading import Thread
from StringIO import StringIO
import pycurl, urllib

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
        self.curl.close()

    def run(self):
        buf = StringIO()
        self.curl.setopt(pycurl.WRITEFUNCTION, buf.write)
        self.curl.perform()
        self.response = buf.getvalue()
        buf.close()

    def get(self):
        return self.response

