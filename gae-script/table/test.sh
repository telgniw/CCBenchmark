#!/bin/bash
URL_PREFIX="http://yi-testi.appspot.com"
EXEC_WGET="wget -qO-"

function usage {
    echo "usage: $0 <init> <seed> <size> <num> <max> [task]"
    echo "usage: $0 <del> <seed> <size> <num>"
    echo "usage: $0 <get|put|query> <seed> <size>"
    echo "usage: $0 <delete> [task]"
    exit
}

if [ "$1" == "init" ]; then
    if [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ] || [ -z "$5" ]; then
        usage; fi
    if [ "$5" == "task" ]; then
        $EXEC_WGET "$URL_PREFIX/newtask?url=/table/$1?seed%3D$2%26size%3D$3%26num%3D$4%26max%3D$5"
    else
        $EXEC_WGET "$URL_PREFIX/table/$1?seed=$2&size=$3&num=$4&max=$5"
    fi
    exit
elif [ "$1" == "del" ]; then
    if [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ]; then
        usage; fi
elif [ "$1" == "get" ] || [ "$1" == "put" ] || [ "$1" == "query" ]; then
    if [ -z "$2" ] || [ -z "$3" ]; then
        usage; fi
elif [ "$1" == "delete" ]; then
    if [ "$2" == "task" ]; then
        $EXEC_WGET "$URL_PREFIX/newtask?url=/table/$1"
    else
        $EXEC_WGET "$URL_PREFIX/table/$1"
    fi
    exit
else
    usage
fi

$EXEC_WGET "$URL_PREFIX/table/$1?seed=$2&size=$3&num=$4"
