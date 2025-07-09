#!/bin/bash
set -e

WORKERS=${WORKERS:-4}
export WORKERS

# Update postgres config
docker compose exec -T postgres psql -U postgres -c "ALTER SYSTEM SET shared_buffers='512MB';"
docker compose restart postgres

docker compose up -d --build context-adapter

echo "Running short benchmark..."
locust -f tests/performance/locustfile.py --headless -u 10 -r 10 -t 1m --host http://localhost:8010 --csv tune
