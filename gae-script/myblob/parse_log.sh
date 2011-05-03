#!/bin/bash
GREP="grep -ao"

if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
    echo "usage: $0 <target> <limit> <output_file_prefix>"
    exit
fi

TARGET=$1 LIMIT=$2 OUTPUT=$3

TYPES[0]="upload"
TYPES[1]="download"
for TYPE in ${TYPES[*]}; do
    TIMESTAMP="\[[-/: 0-9A-Za-z]\+\]"
    ACTION="myblob $TYPE"
    RESULT="SUCCESS"
    TIME="SimBlob[0-9]\+ [0-9]\+ [0-9]\+ [0-9,]\+ [0-9,]\+"
    
    TEST=`$GREP "$ACTION" $TARGET | head -n 1`
    if [ -z "$TEST" ]; then
        continue
    fi

    FILT0="$TIMESTAMP.*$ACTION.*$TIME"
    FILT1="\($TIMESTAMP\)\|\($ACTION $RESULT $TIME\)"
    $GREP "$FILT0" $TARGET | head -n $LIMIT | $GREP "$FILT1" > $OUTPUT.$TYPE.log
done
