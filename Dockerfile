# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirement.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirement.txt

# Copy the rest of the application code into the container
COPY . .

# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Set the environment variable for MySQL
ENV MYSQL_DATABASE=mydatabase
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=Lina&mimi2706
ENV MYSQL_HOST=db
ENV MYSQL_PORT=3306

# Expose port 5000 for Flask
EXPOSE 5000

# Start the Flask app and the MySQL database
CMD ["docker-entrypoint.sh"]