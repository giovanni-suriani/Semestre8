#!/bin/sh
export SCRIPT_PATH=`dirname "$0"`
export CMD_NAME="$SCRIPT_PATH/components/QuartusSetupWeb-13.0.1.232.run"
eval exec "\"$CMD_NAME\"" $@
