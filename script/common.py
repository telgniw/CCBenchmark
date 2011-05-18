#!/usr/bin/env python
from multiprocessing import Process, Queue
from StringIO import StringIO
import pycurl, urllib

queue = Queue()
host = 'http://yi-testi.appspot.com'

class MyProcess(Process):
    """
        A process that performs a HTTPGET request using PycURL.
    """
    def __init__(self, url, args=None, task=False):
        """
            Initialize the cURL object.
        """
        Process.__init__(self, target=self._func_)
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

    def __del__(self):
        Process.__del__(self)
        self.curl.close()

    def _func_(self):
        buf = StringIO()
        self.curl.setopt(pycurl.WRITEFUNCTION, buf.write)
        self.curl.perform()

        global queue
        queue.put(buf.getvalue())
        buf.close()

    @staticmethod
    def get():
        return queue.get()

