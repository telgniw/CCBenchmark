#!/bin/bash
APP_ENGINE_PATH="/usr/local/lib/appengine-java-sdk-1.4.3"
APPCFG="$APP_ENGINE_PATH/bin/appcfg.sh"
APP_PATH="/home/celia/Documents/Git/CCBenchmark/GAEBenchmark/web"

if [ -z "$1" ]; then
    echo "usage: $0 <target>"
    exit
fi

TARGET=$1 N_DAYS=1 SEVERITY=1

$APPCFG --num_days=$N_DAYS --severity=$SEVERITY request_logs $APP_PATH $TARGET
