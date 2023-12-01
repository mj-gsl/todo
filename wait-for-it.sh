#!/bin/bash
# wait-for-it.sh
# https://github.com/vishnubob/wait-for-it

set -e

host="$1"
port="$2"
shift 2
cmd="$@"

until [ "$(echo > /dev/tcp/$host/$port && echo $?)" == "0" ]; do
  >&2 echo "Waiting for $host:$port..."
  sleep 1
done

>&2 echo "$host:$port is available, executing command"
exec $cmd
