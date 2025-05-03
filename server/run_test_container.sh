#!/bin/bash

# Stop any existing test containers
docker-compose -f docker-compose.test.yml down -v

# Build and run the test container
docker-compose -f docker-compose.test.yml up --build --exit-code-from test

# Cleanup
docker-compose -f docker-compose.test.yml down -v