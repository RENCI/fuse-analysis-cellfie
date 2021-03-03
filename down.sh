#!/bin/bash

set -o allexport
source env.TAG
source tests/env.docker
set +o allexport

docker-compose -f docker-compose.yml down
