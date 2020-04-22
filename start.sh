#! /usr/bin/env sh
set -e

# If there's a prestart.sh script in the /app directory, run it before starting
INIT_SCRIPT=/app/init.sh
echo "Checking for script in $INIT_SCRIPT"
if [ -f $INIT_SCRIPT ] ; then
    echo "Running script $INIT_SCRIPT"
    source $INIT_SCRIPT
else
    echo "There is no script $INIT_SCRIPT"
fi

# Start Supervisor, with Nginx and uWSGI
exec /usr/bin/supervisord