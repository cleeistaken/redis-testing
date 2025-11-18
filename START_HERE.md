# 🚀 Redis Benchmark Tool - START HERE

Welcome! This is your entry point to the Redis Benchmark Tool.

## What is This?

A professional-grade Python tool that:
- ✅ Benchmarks Redis performance automatically
- ✅ Tests multiple data sizes and read/write ratios
- ✅ Generates beautiful graphs and detailed reports
- ✅ Handles population, testing, and cleanup automatically

## 30-Second Quick Start

```bash
# 1. Verify everything is installed
python test_setup.py

# 2. Run a quick example
./run_example.sh

# 3. View your results
./view_results.sh
```

That's it! Results are in `results/graphs/` 📊

## 5-Minute Setup (If Needed)

### macOS
```bash
brew install redis memtier-benchmark
pip install -r requirements.txt
redis-server &
```

### Linux (Ubuntu/Debian)
```bash
sudo apt install lsb-release curl gpg
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
sudo apt-get update
sudo apt-get install redis-server memtier-benchmark
pip install -r requirements.txt
sudo systemctl start redis
```

**Need detailed instructions?** → See [INSTALL.md](INSTALL.md)

## Your First Custom Benchmark

```bash
python redis_benchmark.py \
  --data-sizes 64 256 1024 \
  --ratios 1:1 1:10 10:1
```

This tests:
- 3 data sizes (64, 256, 1024 bytes)
- 3 read/write ratios (balanced, read-heavy, write-heavy)
- 9 total test combinations
- ~15 minutes runtime

## Understanding Results

After running, you'll get:

### 1. Terminal Output
```
Data Size       Ratio           Ops/sec             Latency (ms)
64              1:1             45231.50            1.10
256             1:10            48923.40            1.02
...
```

### 2. Graphs (in `results/graphs/`)
- **summary_dashboard.png** ← Start here! Complete overview
- **throughput_by_data_size.png** - How fast is Redis?
- **latency_by_data_size.png** - How responsive is Redis?
- **throughput_heatmap.png** - Which config is best?

### 3. Raw Data (`results/benchmark_results_*.json`)
- Complete metrics for further analysis

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

### Quick Health Check
```bash
python redis_benchmark.py \
  --data-sizes 256 \
  --ratios 1:1 \
  --test-time 30
```

### Comprehensive Analysis
```bash
./run_comprehensive_test.sh
# Warning: Takes 90-120 minutes!
```

## What Do The Numbers Mean?

### Ratios Explained
- `1:1` = 50% writes, 50% reads (balanced workload)
- `1:10` = 9% writes, 91% reads (read-heavy, like caching)
- `10:1` = 91% writes, 9% reads (write-heavy, like logging)
- `1:0` = 100% writes (population phase)
- `0:1` = 100% reads (pure read test)

### Metrics Explained
- **Ops/sec**: Higher is better (throughput)
- **Latency**: Lower is better (response time)
- **Bandwidth**: Network data transfer rate

## Troubleshooting

### "Connection refused"
```bash
# Start Redis
redis-server &

# Test connection
redis-cli ping
```

### "memtier_benchmark not found"
```bash
# macOS
brew install memtier-benchmark

# Linux
sudo apt-get install memtier-benchmark
```

### "No module named 'matplotlib'"
```bash
pip install -r requirements.txt
```

### Still stuck?
```bash
# Run diagnostics
python test_setup.py

# Check detailed troubleshooting
open INSTALL.md  # See "Troubleshooting" section
```

## Documentation Guide

Choose your path:

### 🟢 Beginner
1. You are here! (START_HERE.md)
2. [QUICKSTART.md](QUICKSTART.md) - 5-minute tutorial
3. [README.md](README.md) - Full guide (read sections as needed)

### 🟡 Intermediate
1. [README.md](README.md) - Complete documentation
2. [WORKFLOW.md](WORKFLOW.md) - How it works
3. Experiment with custom configurations

### 🔴 Advanced
1. [WORKFLOW.md](WORKFLOW.md) - Technical details
2. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Architecture
3. Review source: `redis_benchmark.py`, `visualize.py`

### 📚 Full Documentation Index
See [INDEX.md](INDEX.md) for complete navigation guide

## File Overview

### You'll Use These
- `redis_benchmark.py` - Main script
- `run_example.sh` - Quick example
- `view_results.sh` - View results
- `test_setup.py` - Verify installation

### Documentation
- `START_HERE.md` - This file
- `QUICKSTART.md` - 5-minute guide
- `README.md` - Complete manual
- `INSTALL.md` - Installation guide
- `WORKFLOW.md` - Technical details
- `INDEX.md` - Navigation guide

### Configuration
- `requirements.txt` - Python packages
- `example_config.json` - Sample config

## Example Output

Here's what you'll see:

```
============================================================
REDIS BENCHMARK RESULTS SUMMARY
============================================================

Total Tests: 9
Successful: 9
Failed: 0

------------------------------------------------------------
DETAILED RESULTS
------------------------------------------------------------

Data Size       Ratio           Ops/sec             Latency (ms)
------------------------------------------------------------
64              1:1             45231.50            1.10
64              1:10            52341.20            0.95
64              10:1            38912.30            1.28
256             1:1             42156.80            1.18
256             1:10            48923.40            1.02
256             10:1            35678.90            1.40
1024            1:1             35234.60            1.42
1024            1:10            41234.80            1.21
1024            10:1            29876.40            1.67

------------------------------------------------------------
SUMMARY BY DATA SIZE
------------------------------------------------------------

Data Size           Avg Ops/sec              Avg Latency (ms)
------------------------------------------------------------
64                  45494.33                 1.11
256                 42253.03                 1.20
1024                35448.60                 1.43
```

## Tips for Success

1. **Start Small**: Run `./run_example.sh` first
2. **Check Setup**: Run `python test_setup.py` if issues occur
3. **Read Logs**: Check `logs/` if something fails
4. **Understand Graphs**: Start with `summary_dashboard.png`
5. **Experiment**: Try different data sizes and ratios
6. **Compare**: Run tests before/after Redis config changes

## What's Happening Behind the Scenes?

For each test:
1. 🗑️ Flush Redis (clean slate)
2. 📝 Populate with test data (write-only)
3. ⏸️ Wait 5 seconds (let Redis settle)
4. 🚀 Run benchmark (mixed read/write)
5. 📊 Parse and store results
6. ⏸️ Wait 10 seconds (before next test)

Then:
7. 💾 Save results to JSON
8. 📄 Print text report
9. 📈 Generate 8 beautiful graphs

## Performance Expectations

Typical results (depends on hardware):

| Data Size | Ops/sec | Latency |
|-----------|---------|---------|
| 64 bytes  | 40-60K  | 0.8-1.2ms |
| 256 bytes | 35-50K  | 1.0-1.5ms |
| 1KB       | 30-45K  | 1.2-2.0ms |
| 4KB       | 20-35K  | 1.5-3.0ms |

Your results will vary based on:
- CPU speed
- RAM speed
- Redis configuration
- Network latency (if remote)
- System load

## Next Steps

### Right Now
```bash
# Verify setup
python test_setup.py

# Run example
./run_example.sh

# View results
open results/graphs/summary_dashboard.png
```

### Next 5 Minutes
- Read [QUICKSTART.md](QUICKSTART.md)
- Try a custom benchmark
- Explore the graphs

### Next Hour
- Read [README.md](README.md)
- Experiment with different configurations
- Compare results

### This Week
- Run comprehensive tests
- Optimize your Redis configuration
- Create custom test scripts

## Real-World Use Cases

### 1. Capacity Planning
Test different data sizes to understand memory and performance trade-offs.

### 2. Configuration Tuning
Benchmark before/after Redis config changes to measure impact.

### 3. Hardware Selection
Compare performance across different servers or cloud instances.

### 4. Application Design
Understand read vs write performance to optimize your application.

### 5. Regression Testing
Run regular benchmarks to catch performance degradation.

## Getting Help

### Self-Service
1. Run: `python test_setup.py`
2. Check: `logs/benchmark_*.log`
3. Read: [INSTALL.md](INSTALL.md) Troubleshooting section

### Documentation
- **Installation issues**: [INSTALL.md](INSTALL.md)
- **Usage questions**: [README.md](README.md)
- **Technical details**: [WORKFLOW.md](WORKFLOW.md)
- **Navigation help**: [INDEX.md](INDEX.md)

## Project Stats

- **Total Lines**: 3,600+
- **Python Code**: ~1,000 lines
- **Documentation**: ~2,500 lines
- **Scripts**: 5 helper scripts
- **Graphs Generated**: 8 types
- **Test Time**: 15 min (quick) to 2 hours (comprehensive)

## Ready?

Let's go! 🚀

```bash
# Verify everything is ready
python test_setup.py

# Run your first benchmark
./run_example.sh

# Enjoy your results!
./view_results.sh
```

---

**Questions?** Check [INDEX.md](INDEX.md) for navigation or [README.md](README.md) for details.

**Issues?** Run `python test_setup.py` and see [INSTALL.md](INSTALL.md) troubleshooting.

**Ready to dive deeper?** Read [QUICKSTART.md](QUICKSTART.md) next!

Happy benchmarking! 📊✨

