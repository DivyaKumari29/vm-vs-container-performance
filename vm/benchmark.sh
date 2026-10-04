#!/bin/bash

echo "Running VM CPU benchmark..."

sysbench cpu \
  --cpu-max-prime=20000 \
  --threads=4 \
  --time=30 \
  run
