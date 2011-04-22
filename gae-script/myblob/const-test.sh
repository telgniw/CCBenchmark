#!/bin/bash
EXEC_TEST="./test.py"
EXEC_GET_LOG="./retrieve_log.sh"
EXEC_PARSE="./parse_log.sh"
EXEC_PLOT="./plot.py"

if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
    echo "usage: $0 <max> <num> <output_dir>"
    exit
fi

MAX=$1 NUM=$2 DIR=$3

if [ -d "$DIR" ]; then
    echo "dir '$DIR' already exists"
    exit
fi

mkdir $DIR
$EXEC_TEST init $MAX 1 kb

TYPES[0]="up"
TYPES[1]="down"
for i in $(seq $((NUM))); do
    for TYPE in ${TYPES[*]}; do
        echo $TYPE $i
        $EXEC_TEST $TYPE $MAX para >& /dev/null
        TMP=/tmp/$i.log
        $EXEC_GET_LOG $TMP >& /dev/null
        $EXEC_PARSE $TMP $MAX $DIR/$i
    done
    $EXEC_TEST del
done

TYPES[0]="upload"
TYPES[1]="download"
for TYPE in ${TYPES[*]}; do
    cat $DIR/*.$TYPE.log > $DIR/$TYPE.log
    $EXEC_PLOT $DIR/$TYPE.log 200
done
