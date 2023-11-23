#!/bin/sh

timeout 1m bash /init.sh
init_pid=$!

sleep 80

if ps -p $init_pid > /dev/null; then
  echo "init.sh is still running, terminating..."
  kill $init_pid
fi

rm -f /init.sh

exec "$@"
