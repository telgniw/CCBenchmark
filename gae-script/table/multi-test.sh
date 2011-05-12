#!/bin/bash
TMP_DIR="/tmp"
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
    if [ "$(((i-1) % 10))" == "0" ]; then
        $EXEC_TEST init $i $SIZE 1 10
    fi
done

# get 1
echo "get(1)"
for i in {1..10}; do
    t=$((RANDOM % MAX))
    echo "get $t"
    for j in {1..10}; do
        $EXEC_TEST get $t $SIZE
    done
    TMP=$TMP_DIR/$i.log
    $EXEC_GET_LOG $TMP >& /dev/null
    $EXEC_PARSE $TMP 10 $DIR/$i get
done

# put 1
echo "put(1)"
for i in {1..10}; do
    t=$((RANDOM % MAX))
    echo "put $t"
    for j in {1..10}; do
        $EXEC_TEST put $t $SIZE
    done
    TMP=$TMP_DIR/$i.log
    $EXEC_GET_LOG $TMP >& /dev/null
    $EXEC_PARSE $TMP 10 $DIR/$i put
    $EXEC_TEST del $t $size 10
done

# init 9
echo "init(9)"
for i in $(seq $((MAX))); do
    if [ "$(((i-1) % 10))" == "0" ]; then
        $EXEC_TEST init $i $SIZE 9 10
    fi
done

# query 10
echo "query(10)"
for i in {1..10}; do
    t=$((RANDOM % MAX))
    echo "query $t"
    for j in {1..10}; do
        $EXEC_TEST query $t $SIZE
    done
    TMP=$TMP_DIR/$i.log
    $EXEC_GET_LOG $TMP >& /dev/null
    $EXEC_PARSE $TMP 10 $DIR/$i query
done

# delete all
$EXEC_TEST delete task

echo "plot get"
TYPE=get
cat $DIR/*.$TYPE.log > $DIR/$TYPE.log
$EXEC_PLOT $DIR/$TYPE.log 20
LIST=`ls $DIR/*.$TYPE.log`
$EXEC_CAL_STAT $DIR/$TYPE.stat 20 $LIST

echo "plot put"
TYPE=put
cat $DIR/*.$TYPE.log > $DIR/$TYPE.log
$EXEC_PLOT $DIR/$TYPE.log 20
LIST=`ls $DIR/*.$TYPE.log`
$EXEC_CAL_STAT $DIR/$TYPE.stat 20 $LIST

echo "plot query"
TYPE=query
cat $DIR/*.$TYPE.log > $DIR/$TYPE.log
$EXEC_PLOT $DIR/$TYPE.log 60
LIST=`ls $DIR/*.$TYPE.log`
$EXEC_CAL_STAT $DIR/$TYPE.stat 60 $LIST
