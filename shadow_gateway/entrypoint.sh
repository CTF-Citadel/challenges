#!/bin/sh

touch /root/goldnugget.txt

echo $flag > /root/goldnugget.txt

export flag=""  

echo '' > /entrypoint.sh

exec "$@"
