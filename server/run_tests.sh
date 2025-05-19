#!/bin/bash
set -e

# Print environment variables for debugging (omitting sensitive ones)
echo "Environment:"
echo "DB_HOST: $DB_HOST"
echo "TEST_DB: $TEST_DB"

# Wait for the PostgreSQL database to be ready
echo "Waiting for PostgreSQL at host: $DB_HOST..."
python -c "
import time
import psycopg2
import os

# Maximum number of attempts to connect to the database
max_attempts = 30
attempt = 0

# Get environment variables with defaults
db_host = os.environ.get('DB_HOST', 'test-db')
db_user = os.environ.get('DB_USER', 'postgres')
db_password = os.environ.get('DB_PASSWORD', 'postgres')
db_port = os.environ.get('DB_PORT', '5432')

print(f'Attempting to connect to PostgreSQL at {db_host}:{db_port}')

while attempt < max_attempts:
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        conn.close()
        print('PostgreSQL is ready!')
        break
    except psycopg2.OperationalError as e:
        attempt += 1
        print(f'Waiting for PostgreSQL... {attempt}/{max_attempts}')
        print(f'Error: {e}')
        time.sleep(1)

if attempt == max_attempts:
    print('Could not connect to PostgreSQL')
    exit(1)
"

# Create the test database if it doesn't exist
echo "Setting up test database: $TEST_DB"
python -c "
import psycopg2
import os

db_host = os.environ.get('DB_HOST', 'test-db')
db_user = os.environ.get('DB_USER', 'postgres')
db_password = os.environ.get('DB_PASSWORD', 'postgres')
db_port = os.environ.get('DB_PORT', '5432')
test_db = os.environ.get('TEST_DB', 'test_ecommerce')

try:
    # Connect to default postgres database
    conn = psycopg2.connect(
        dbname='postgres',
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Check if test database exists
    cursor.execute(f\"\"\"
        SELECT EXISTS(
            SELECT datname FROM pg_catalog.pg_database WHERE datname = '{test_db}'
        );
    \"\"\")
    exists = cursor.fetchone()[0]
    
    if not exists:
        print(f'Creating database {test_db}')
        cursor.execute(f'CREATE DATABASE {test_db}')
        print(f'Database {test_db} created')
    else:
        print(f'Database {test_db} already exists')
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f'Error setting up test database: {e}')
    exit(1)
"

# Run the tests
echo "Running tests..."
pytest $@

echo "Tests completed!"