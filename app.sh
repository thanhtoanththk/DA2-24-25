#!/bin/bash

# Start or Stop the Flask app based on the argument passed

if [ "$1" == "start" ]; then
    echo "Starting the Flask app with Docker..."
    docker-compose up -d web
elif [ "$1" == "stop" ]; then
    echo "Stopping the Flask app and removing Docker images..."
    docker-compose down
    docker image prune -f
    echo "Flask app stopped and Docker images removed."
else
    echo "Usage: ./app.sh {start|stop}"
    echo "Use 'start' to start the Flask app and 'stop' to stop it."
fi