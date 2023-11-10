#!/bin/bash

mkdir /root/ && touch /root/goldnugget.txt

echo $flag > /root/goldnugget.txt

/usr/sbin/sshd
php-fpm