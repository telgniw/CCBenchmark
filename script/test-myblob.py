#!/usr/bin/env python
from common import Logger
import myblob, sys

def usage():
    print sys.argv[0], '<num>', '<size>', '<offset>', '<n_iters>'
    exit(1)

if len(sys.argv) != 5:
    usage()

num, size, offset, n_iters = [int(t) for t in sys.argv[1:]]
log = Logger(strm=sys.stdout)

del log

