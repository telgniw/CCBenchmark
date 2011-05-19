#!/usr/bin/env python
from common import ThreadAction 

def init(max, num, size, seed):
    return ThreadAction(url='/table/small/init', args={
        'max': max, 'num': num, 'size': size, 'seed': seed})

def get(size, seed):
    return ThreadAction(url='/table/small/get', args={
        'size': size, 'seed': seed})

def put(size, seed):
    return ThreadAction(url='/table/small/put', args={
        'size': size, 'seed': seed})

def delete(num, size, seed):
    return ThreadAction(url='/table/small/del', args={
        'num': num, 'size': size, 'seed': seed})

def query(size, seed):
    return ThreadAction(url='/table/small/query', args={
        'size': size, 'seed': seed})

def deleteAll():
    return ThreadAction(url='/table/small/delete')

