#!/bin/bash
set -e

# Wait for the PostgreSQL database to be ready
echo "Waiting for PostgreSQL..."
python -c "
import time
import psycopg2

# Maximum number of attempts to connect to the database
max_attempts = 30
attempt = 0

while attempt < max_attempts:
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user='${DB_USER}',
            password='${DB_PASSWORD}',
            host='db',
            port='5432'
        )
        conn.close()
        print('PostgreSQL is ready!')
        break
    except psycopg2.OperationalError:
        attempt += 1
        print(f'Waiting for PostgreSQL... {attempt}/{max_attempts}')
        time.sleep(1)

if attempt == max_attempts:
    print('Could not connect to PostgreSQL')
    exit(1)
"

# Run the tests
echo "Running tests..."
pytest $@

echo "Tests completed!"