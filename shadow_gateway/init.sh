#!/bin/sh

touch /root/goldnugget.txt

echo $flag > /root/goldnugget.txt

export flag=""  

exec "$@"