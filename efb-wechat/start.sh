#!/bin/sh

EWS_LOGIN_STATUS_FILE="/home/efb/efb_config/profiles/default/blueset.wechat/wxpy.pkl"

if [ -e "$EWS_LOGIN_STATUS_FILE" ]; then
    rm "$EWS_LOGIN_STATUS_FILE"
    echo "Deleted  previous WeChat login status file."
    echo "Checking environment variables"
else
    echo "Checking environment variables"
fi

python3 configuration.py && ehforwarderbot -p default