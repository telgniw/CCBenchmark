#!/usr/bin/env python
from common import MyProcess

def init(max, num, size, seed):
    return MyProcess(url='/table/small/init', args={
        'max': max, 'num': num, 'size': size, 'seed': seed})

def get(size, seed):
    return MyProcess(url='/table/small/get', args={
        'size': size, 'seed': seed})

def put(size, seed):
    return MyProcess(url='/table/small/put', args={
        'size': size, 'seed': seed})

def delete(num, size, seed):
    return MyProcess(url='/table/small/del', args={
        'num': num, 'size': size, 'seed': seed})

def query(size, seed):
    return MyProcess(url='/table/small/query', args={
        'size': size, 'seed': seed})

def deleteAll():
    return MyProcess(url='/table/small/delete')

