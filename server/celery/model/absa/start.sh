#!/bin/bash

dockerize -wait tcp://kafka:9093 -timeout 20s

echo "Start Analysis Worker"

python -u worker.py