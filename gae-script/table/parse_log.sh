#!/bin/bash
GREP="grep -ao"

function usage {
    echo "usage: $0 <target> <limit> <output_file_prefix> <type>"
    exit
}

if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ]; then
    usage
fi

TARGET=$1 LIMIT=$2 OUTPUT=$3 TYPE=$4

TIMESTAMP="\[[-/: 0-9A-Za-z]\+\]"
ACTION="table $TYPE"
RESULT="SUCCESS"
TIME="[0-9]\+ [0-9]\+ [0-9]\+"

TEST=`$GREP "$ACTION" $TARGET | head -n 1`
if [ -z "$TEST" ]; then
    exit
fi

FILT0="$TIMESTAMP.*$ACTION.*$TIME"
FILT1="\($TIMESTAMP\)\|\($ACTION $RESULT $TIME\)"
$GREP "$FILT0" $TARGET | head -n $LIMIT | $GREP "$FILT1" > $OUTPUT.$TYPE.log
