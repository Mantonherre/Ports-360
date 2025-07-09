#!/bin/bash
set -e

docker exec timeseries pgbench -c 10 -T 120 -f /workspace/Ports-360/tests/performance/pgbench.sql
