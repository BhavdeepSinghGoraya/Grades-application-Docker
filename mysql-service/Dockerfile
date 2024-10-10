# Use the official MySQL image
FROM mysql:5.7

# Set environment variables
ENV MYSQL_ROOT_PASSWORD=password
ENV MYSQL_DATABASE=grades_db
ENV MYSQL_USER=user
ENV MYSQL_PASSWORD=password

# Copy the initialization script
COPY init.sql /docker-entrypoint-initdb.d/
