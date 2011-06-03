#!/usr/bin/env python
from common import ThreadAction 

def init(max, num, size, seed, task=False):
    return ThreadAction(url='/table/medium/init', args={
        'max': max, 'num': num, 'size': size, 'seed': seed}, task=task)

def get(size, seed):
    return ThreadAction(url='/table/medium/get', args={
        'size': size, 'seed': seed})

def put(size, seed):
    return ThreadAction(url='/table/medium/put', args={
        'size': size, 'seed': seed})

def delete(num, size, seed):
    return ThreadAction(url='/table/medium/del', args={
        'num': num, 'size': size, 'seed': seed})

def query(size, seed):
    return ThreadAction(url='/table/medium/query', args={
        'size': size, 'seed': seed})

def queryl(size, seed):
    return ThreadAction(url='/table/medium/queryl', args={
        'size': size, 'seed': seed})

def deleteAll(task=False):
    return ThreadAction(url='/table/medium/delete', task=task)

