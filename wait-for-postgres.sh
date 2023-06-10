#!/bin/sh
# wait-for-postgres.sh

set -e

host="$1"
dbuser="$2"
dbpassword="$3"
dbdb="$4"
shift
#cmd="$@"

until PGPASSWORD="$dbpassword" psql -h "$host" -d "$dbdb" -U "$dbuser" -c '\q'; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
done

>&2 echo "Postgres is up - executing command"
#echo 'run'
#echo $cmd
#exec $cmd