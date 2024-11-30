# Use the official MySQL 5.7 image as the base
FROM mysql:5.7

# Add the init.sql script to the container
COPY ./init.sql /docker-entrypoint-initdb.d/

# Set environment variables for MySQL
ENV MYSQL_ROOT_PASSWORD=password
ENV MYSQL_DATABASE=grades_db
ENV MYSQL_USER=user
ENV MYSQL_PASSWORD=password

# Expose MySQL port
EXPOSE 3306
