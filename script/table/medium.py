#!/usr/bin/env python
from common import MyProcess

def init(max, num, size, seed):
    return MyProcess(url='/table/medium/init', args={
        'max': max, 'num': num, 'size': size, 'seed': seed})

def get(size, seed):
    return MyProcess(url='/table/medium/get', args={
        'size': size, 'seed': seed})

def put(size, seed):
    return MyProcess(url='/table/medium/put', args={
        'size': size, 'seed': seed})

def delete(num, size, seed):
    return MyProcess(url='/table/medium/del', args={
        'num': num, 'size': size, 'seed': seed})

def query(size, seed):
    return MyProcess(url='/table/medium/query', args={
        'size': size, 'seed': seed})

def queryl(size, seed):
    return MyProcess(url='/table/medium/queryl', args={
        'size': size, 'seed': seed})

def deleteAll():
    return MyProcess(url='/table/medium/delete')

