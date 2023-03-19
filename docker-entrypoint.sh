#!/bin/sh

# Wait for the MySQL database to start
while ! nc -z db 3306; do
  sleep 0.1
done

# Run database migrations
flask db upgrade

# Start the Flask app
flask run --host=0.0.0.0