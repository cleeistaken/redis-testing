# Quick Start Guide

Get up and running with Redis benchmarking in 5 minutes!

## Step 1: Install Prerequisites

### macOS
```bash
# Install Redis
brew install redis

# Install memtier_benchmark
brew install memtier-benchmark

# Start Redis
redis-server &
```

### Ubuntu/Debian
```bash
# Install Redis
sudo apt-get update
sudo apt-get install redis-server

# Install memtier_benchmark
sudo apt-get install memtier-benchmark

# Start Redis
sudo systemctl start redis-server
```

## Step 2: Install Python Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# Or using pipenv
pipenv install
pipenv shell
```

## Step 3: Run Your First Benchmark

### Option A: Use the Example Script (Easiest)

```bash
./run_example.sh
```

This runs a quick benchmark with sensible defaults.

### Option B: Run Manually

```bash
python redis_benchmark.py \
  --data-sizes 64 256 1024 \
  --ratios 1:1 1:10 10:1
```

## Step 4: View Results

After the benchmark completes, check:

1. **Terminal Output**: Summary table of results
2. **Logs**: `logs/benchmark_YYYYMMDD_HHMMSS.log`
3. **JSON Results**: `results/benchmark_results_YYYYMMDD_HHMMSS.json`
4. **Graphs**: `results/graphs/*.png`

### Key Files to Check

```bash
# View the latest log
ls -t logs/*.log | head -1 | xargs tail -50

# View the latest results
ls -t results/*.json | head -1 | xargs cat | python -m json.tool

# Open graphs folder
open results/graphs/  # macOS
xdg-open results/graphs/  # Linux
```

## Understanding Your Results

### Key Metrics

- **Ops/sec**: Higher is better (throughput)
- **Latency**: Lower is better (response time)

### What the Ratios Mean

- `1:1` = 50% writes, 50% reads (balanced)
- `1:10` = 9% writes, 91% reads (read-heavy)
- `10:1` = 91% writes, 9% reads (write-heavy)

### Graph Descriptions

1. **summary_dashboard.png** - Start here! Overview of all metrics
2. **throughput_by_data_size.png** - How performance changes with data size
3. **latency_by_data_size.png** - How latency changes with data size
4. **throughput_heatmap.png** - Quick view of best/worst configurations

## Common Use Cases

### Test Read Performance
```bash
python redis_benchmark.py \
  --data-sizes 64 256 1024 \
  --ratios 0:1 1:10 1:5
```

### Test Write Performance
```bash
python redis_benchmark.py \
  --data-sizes 64 256 1024 \
  --ratios 1:0 10:1 5:1
```

### Test Large Objects
```bash
python redis_benchmark.py \
  --data-sizes 4096 16384 65536 \
  --ratios 1:1 \
  --test-time 120
```

### Quick Performance Check
```bash
python redis_benchmark.py \
  --data-sizes 256 \
  --ratios 1:1 \
  --test-time 30
```

## Troubleshooting

### "Connection refused"
```bash
# Check if Redis is running
redis-cli ping

# If not, start it
redis-server &
```

### "memtier_benchmark: command not found"
```bash
# Install memtier_benchmark
brew install memtier-benchmark  # macOS
sudo apt-get install memtier-benchmark  # Linux
```

### "No module named 'matplotlib'"
```bash
# Install Python dependencies
pip install -r requirements.txt
```

### Tests are too slow
```bash
# Reduce test time and iterations
python redis_benchmark.py \
  --data-sizes 64 256 \
  --ratios 1:1 \
  --test-time 30 \
  --wait-between-iterations 5
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Customize settings for your specific use case
- Compare results across different Redis configurations
- Share your findings!

## Example Output

```
================================================================================
REDIS BENCHMARK RESULTS SUMMARY
================================================================================

Total Tests: 9
Successful: 9
Failed: 0

--------------------------------------------------------------------------------
DETAILED RESULTS
--------------------------------------------------------------------------------

Data Size       Ratio           Ops/sec             Latency (ms)        Status         
--------------------------------------------------------------------------------
64              1:1             45231.50            1.10                SUCCESS        
64              1:10            52341.20            0.95                SUCCESS        
64              10:1            38912.30            1.28                SUCCESS        
256             1:1             42156.80            1.18                SUCCESS        
256             1:10            48923.40            1.02                SUCCESS        
256             10:1            35678.90            1.40                SUCCESS        
1024            1:1             35234.60            1.42                SUCCESS        
1024            1:10            41234.80            1.21                SUCCESS        
1024            10:1            29876.40            1.67                SUCCESS        
```

Happy benchmarking! 🚀

