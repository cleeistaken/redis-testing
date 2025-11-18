#!/bin/bash
# Comprehensive Redis benchmark test
# This runs an extensive benchmark covering many scenarios

echo "=========================================="
echo "Comprehensive Redis Benchmark Test"
echo "=========================================="
echo ""
echo "This will run approximately 56 test permutations"
echo "Estimated time: 90-120 minutes"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 0
fi

python3 redis_benchmark.py \
  --data-sizes 32 64 128 256 512 1024 2048 4096 \
  --ratios 1:0 10:1 5:1 2:1 1:1 1:2 1:5 1:10 0:1 \
  --test-time 120 \
  --benchmark-clients 100 \
  --benchmark-threads 8 \
  --populate-clients 100 \
  --populate-threads 8 \
  --wait-between-iterations 30 \
  --wait-between-operations 10

echo ""
echo "=========================================="
echo "Comprehensive test complete!"
echo "=========================================="

