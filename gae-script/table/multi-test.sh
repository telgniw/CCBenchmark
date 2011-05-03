#!/bin/bash
EXEC_TEST="./test.sh"
EXEC_GET_LOG="./retrieve_log.sh"
EXEC_PARSE="./parse_log.sh"
EXEC_PLOT="./plot.py"
EXEC_CAL_STAT="./cal-stat.py"

function usage {
    echo "usage: $0 <max> <size> <output_dir>"
    exit
}

if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
    usage
fi

MAX=$1 SIZE=$2 DIR=$3

if [ -d "$DIR" ]; then
    echo "dir '$DIR' already exists"
    exit
fi

mkdir $DIR

# init 1
echo "init(1)"
for i in $(seq $((MAX))); do
    if [ "$((i % 10))" == "0" ]; then
        $EXEC_TEST init $i $SIZE 1 10
    fi
done

# get 1
echo "get(1)"
for t in {1..100}; do
    i=$((RANDOM % MAX))
    echo "get i=$i"
    for j in {1..10}; do
        $EXEC_TEST get $i $SIZE
    done
    TMP=/tmp/$i.log
    $EXEC_GET_LOG $TMP >& /dev/null
    $EXEC_PARSE $TMP 10 $DIR/$i
done

# init 9
echo "init(9)"
for i in $(seq $((MAX))); do
    if [ "$((i % 10))" == "0" ]; then
        $EXEC_TEST init $i $SIZE 1 10
    fi
done

# query 10
echo "query(10)"
for t in {1..100}; do
    i=$((RANDOM % MAX))
    echo "query i=$i"
    for j in {1..10}; do
        $EXEC_TEST query $i $SIZE
    done
    TMP=/tmp/$i.log
    $EXEC_GET_LOG $TMP >& /dev/null
    $EXEC_PARSE $TMP 10 $DIR/$i
done

# delete all
$EXEC_TEST delete task

echo "plot get"
TYPE=get
cat $DIR/*.$TYPE.log > $DIR/$TYPE.log
$EXEC_PLOT $DIR/$TYPE.log 10
LIST=`ls $DIR/*.$TYPE.log`
$EXEC_CAL_STAT $DIR/$TYPE.stat 10 $LIST

echo "plot query"
TYPE=query
cat $DIR/*.$TYPE.log > $DIR/$TYPE.log
$EXEC_PLOT $DIR/$TYPE.log 50
LIST=`ls $DIR/*.$TYPE.log`
$EXEC_CAL_STAT $DIR/$TYPE.stat 50 $LIST
