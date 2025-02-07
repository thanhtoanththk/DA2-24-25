#!/bin/bash

if [ "$1" == "start" ]; then
    echo "Starting the Flask app with Docker..."
    docker-compose up -d web
    docker-compose exec web flask db migrate -m "Initial migration"
    docker-compose exec web flask db upgrade
elif [ "$1" == "stop" ]; then
    echo "Stopping the Flask app and removing Docker images..."
    docker-compose down
    docker image prune -f
    echo "Flask app stopped and Docker images removed."
elif [ "$1" == "restart" ]; then
    echo "Restarting the Flask app..."
    docker-compose down
    docker-compose up -d web
    docker-compose exec web flask db migrate -m "Initial migration"
    docker-compose exec web flask db upgrade
    echo "Flask app restarted."
else
    echo "Usage: ./app.sh {start|stop|restart}"
    echo "Use 'start' to start the Flask app, 'stop' to stop it, and 'restart' to restart it."
fi
