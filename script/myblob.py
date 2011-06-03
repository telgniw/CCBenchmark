#!/usr/bin/env python
from common import ThreadAction 

def init(num, size, task=False):
    return ThreadAction(url='/myblob/init', args={
        'num': num, 'size': size}, task=task)

def upload(id):
    return ThreadAction(url='/myblob/upload', args={'id': id})

def download(id):
    return ThreadAction(url='/myblob/download', args={'id': id})

def deleteAll(task=False):
    return ThreadAction(url='/myblob/delete', task=task)

