FROM mysql:latest

# This is executed when the mysql instance is instantiated
ADD init.sql /docker-entrypoint-initdb.d/

RUN chown -R mysql:mysql /docker-entrypoint-initdb.d/


