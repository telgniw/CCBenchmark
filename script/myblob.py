#!/usr/bin/env python
from common import MyProcess

def init(num, size):
    return MyProcess(url='/myblob/init', args={'num': num, 'size': size})

def upload(id):
    return MyProcess(url='/myblob/upload', args={'id': id})

def download(id):
    return MyProcess(url='/myblob/download', args={'id': id})

def deleteAll():
    return MyProcess(url='/myblob/delete')

