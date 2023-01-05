#!/bin/sh

# setup logging to docker
ln -sf /dev/stdout /code/siteinfo.log
cd /code/src/siteinfo_cmd
ls /code

echo "Docker container has been started"
uvicorn siteinfo:app --proxy-headers --host "0.0.0.0"