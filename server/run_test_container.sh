#!/bin/bash

# Use a project name to isolate this from the development environment
PROJECT_NAME="studious_waffle_test"

# Make sure any old test containers are cleaned up first
echo "Cleaning up any previous test environment..."
docker compose -f docker-compose.test.yml -p $PROJECT_NAME down --remove-orphans

echo "Starting test containers..."
# Run the tests with the isolated project name
docker compose -f docker-compose.test.yml -p $PROJECT_NAME up --build --exit-code-from test

# Store the exit code from docker-compose
TEST_EXIT_CODE=$?

echo "Tests completed. Cleaning up test environment..."
# Clean up everything related to this test run
docker compose -f docker-compose.test.yml -p $PROJECT_NAME down --remove-orphans
echo "Test environment cleanup complete."

exit $TEST_EXIT_CODE