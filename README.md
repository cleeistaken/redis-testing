# Redis Benchmark Tool

A comprehensive Python-based benchmarking tool for Redis using `memtier_benchmark`. This tool automates the process of running Redis performance tests with various data sizes and read/write ratios, then generates detailed reports and visualizations.

## Features

- 🚀 **Automated Benchmarking**: Run multiple test permutations automatically
- 📊 **Rich Visualizations**: Generate graphs showing throughput, latency, and performance metrics
- 📝 **Detailed Logging**: Complete logs of all operations and results
- 🔄 **Database Management**: Automatic population, testing, and cleanup
- ⚙️ **Highly Configurable**: Customize all aspects of the benchmark
- 📈 **Comprehensive Reports**: Both text-based and graphical result summaries

## Prerequisites

### Required Software

1. **Redis Server**: A running Redis instance
   ```bash
   # Install Redis (macOS)
   brew install redis
   
   # Start Redis
   redis-server
   ```

2. **memtier_benchmark**: The Redis benchmark tool
   ```bash
   # Install memtier_benchmark (macOS)
   brew install memtier-benchmark
   
   # Verify installation
   memtier_benchmark --version
   ```

3. **Python 3.13+**: Python environment
   ```bash
   python3 --version
   ```

### Python Dependencies

Install required Python packages:

```bash
# Using pip
pip install -r requirements.txt

# Or using pipenv
pipenv install
pipenv shell
```

Required packages:
- `matplotlib` >= 3.8.0
- `seaborn` >= 0.13.0
- `pandas` >= 2.1.0

## Quick Start

### Basic Usage

Run a simple benchmark with default settings:

```bash
python redis_benchmark.py \
  --data-sizes 64 256 1024 \
  --ratios 1:1 1:10 10:1
```

This will:
1. Test with data sizes of 64, 256, and 1024 bytes
2. Test with SET:GET ratios of 1:1, 1:10, and 10:1
3. Run 9 total test permutations (3 sizes × 3 ratios)
4. Generate logs, results, and visualizations

### Custom Redis Connection

Connect to a remote Redis instance:

```bash
python redis_benchmark.py \
  --host 192.168.1.100 \
  --port 6380 \
  --password mypassword \
  --data-sizes 128 512 \
  --ratios 1:1 5:1
```

### Extended Benchmark

Run a comprehensive benchmark with custom settings:

```bash
python redis_benchmark.py \
  --data-sizes 64 128 256 512 1024 2048 \
  --ratios 1:0 1:1 1:5 1:10 5:1 10:1 0:1 \
  --test-time 120 \
  --benchmark-clients 100 \
  --benchmark-threads 8 \
  --wait-between-iterations 30
```

## Command-Line Options

### Redis Connection

| Option | Default | Description |
|--------|---------|-------------|
| `--host` | localhost | Redis server hostname |
| `--port` | 6379 | Redis server port |
| `--password` | None | Redis authentication password |

### Benchmark Parameters

| Option | Required | Description |
|--------|----------|-------------|
| `--data-sizes` | Yes | Space-separated list of data sizes in bytes |
| `--ratios` | Yes | Space-separated list of SET:GET ratios |

### Memtier Settings - Population Phase

| Option | Default | Description |
|--------|---------|-------------|
| `--populate-clients` | 50 | Number of concurrent clients |
| `--populate-threads` | 4 | Number of threads |
| `--populate-requests` | 10000 | Requests per client |

### Memtier Settings - Benchmark Phase

| Option | Default | Description |
|--------|---------|-------------|
| `--benchmark-clients` | 50 | Number of concurrent clients |
| `--benchmark-threads` | 4 | Number of threads |
| `--benchmark-requests` | 10000 | Requests per client |
| `--test-time` | 60 | Test duration in seconds |
| `--pipeline` | 1 | Pipeline depth |
| `--key-pattern` | R:R | Key pattern (R:R = random) |

### Timing Settings

| Option | Default | Description |
|--------|---------|-------------|
| `--wait-between-operations` | 5 | Seconds to wait between populate and benchmark |
| `--wait-between-iterations` | 10 | Seconds to wait between test iterations |

### Other Options

| Option | Default | Description |
|--------|---------|-------------|
| `--no-flush` | False | Skip flushing database before each test |
| `--log-dir` | logs | Directory for log files |
| `--results-dir` | results | Directory for results and graphs |
| `--no-visualize` | False | Skip generating visualization graphs |

## Understanding Ratios

The `--ratios` parameter specifies the SET:GET ratio:

- `1:0` - Write-only (100% SET operations)
- `1:1` - Balanced (50% SET, 50% GET)
- `1:5` - Read-heavy (16.7% SET, 83.3% GET)
- `1:10` - Very read-heavy (9% SET, 91% GET)
- `5:1` - Write-heavy (83.3% SET, 16.7% GET)
- `10:1` - Very write-heavy (91% SET, 9% GET)
- `0:1` - Read-only (100% GET operations)

## Output Files

### Directory Structure

```
redis-testing/
├── logs/
│   └── benchmark_YYYYMMDD_HHMMSS.log
├── results/
│   ├── benchmark_results_YYYYMMDD_HHMMSS.json
│   └── graphs/
│       ├── throughput_by_data_size.png
│       ├── latency_by_data_size.png
│       ├── throughput_by_ratio.png
│       ├── throughput_heatmap.png
│       ├── latency_heatmap.png
│       ├── get_set_comparison.png
│       ├── bandwidth_analysis.png
│       └── summary_dashboard.png
```

### Log Files

Located in `logs/` directory:
- Timestamped log file with complete operation history
- Includes all commands executed and their outputs
- Error messages and warnings

### Results Files

Located in `results/` directory:
- **JSON file**: Complete benchmark results with all metrics
  - Configuration used
  - Individual test results
  - Summary statistics

### Visualization Graphs

Located in `results/graphs/` directory:

1. **throughput_by_data_size.png**: Line graph showing ops/sec vs data size for each ratio
2. **latency_by_data_size.png**: Line graph showing latency vs data size for each ratio
3. **throughput_by_ratio.png**: Bar chart comparing throughput across ratios for different data sizes
4. **throughput_heatmap.png**: Heatmap of throughput across all test combinations
5. **latency_heatmap.png**: Heatmap of latency across all test combinations
6. **get_set_comparison.png**: Side-by-side comparison of GET vs SET performance
7. **bandwidth_analysis.png**: Bandwidth utilization across tests
8. **summary_dashboard.png**: Comprehensive dashboard with multiple metrics

## Example Workflows

### 1. Quick Performance Check

Test basic performance with common scenarios:

```bash
python redis_benchmark.py \
  --data-sizes 64 256 1024 \
  --ratios 1:1 1:10 10:1 \
  --test-time 30
```

### 2. Comprehensive Analysis

Full performance analysis across many configurations:

```bash
python redis_benchmark.py \
  --data-sizes 32 64 128 256 512 1024 2048 4096 \
  --ratios 1:0 1:1 1:5 1:10 5:1 10:1 0:1 \
  --test-time 120 \
  --benchmark-clients 100 \
  --benchmark-threads 8 \
  --wait-between-iterations 30
```

### 3. Write-Heavy Workload

Focus on write performance:

```bash
python redis_benchmark.py \
  --data-sizes 64 256 1024 4096 \
  --ratios 1:0 10:1 5:1 3:1 \
  --test-time 90
```

### 4. Read-Heavy Workload

Focus on read performance:

```bash
python redis_benchmark.py \
  --data-sizes 64 256 1024 4096 \
  --ratios 0:1 1:10 1:5 1:3 \
  --test-time 90
```

### 5. Large Object Performance

Test with large data sizes:

```bash
python redis_benchmark.py \
  --data-sizes 1024 4096 16384 65536 \
  --ratios 1:1 1:5 5:1 \
  --test-time 120 \
  --populate-requests 5000 \
  --benchmark-requests 5000
```

## Interpreting Results

### Text Report

The script outputs a formatted text report showing:

1. **Summary Statistics**
   - Total tests run
   - Success/failure counts
   
2. **Detailed Results Table**
   - Each test configuration
   - Throughput (ops/sec)
   - Average latency (ms)
   - Status

3. **Aggregated Results**
   - Average performance by data size
   - Average performance by ratio

### Key Metrics

- **Operations per Second (ops/sec)**: Higher is better
- **Latency (ms)**: Lower is better
- **Bandwidth (KB/sec)**: Network throughput
- **Hits/Misses per Second**: Cache hit rate

### Performance Patterns

Common observations:
- **Larger data sizes** typically result in lower throughput and higher latency
- **Read-heavy workloads** (e.g., 1:10) often show higher throughput than write-heavy
- **Pipeline depth** can significantly improve throughput
- **Client/thread count** affects concurrency and total throughput

## Troubleshooting

### memtier_benchmark not found

```bash
# Install memtier_benchmark
brew install memtier-benchmark  # macOS
# or
sudo apt-get install memtier-benchmark  # Ubuntu/Debian
```

### Redis connection refused

```bash
# Check if Redis is running
redis-cli ping

# Start Redis if not running
redis-server
```

### Permission denied errors

```bash
# Ensure directories are writable
chmod +w logs results
```

### Out of memory errors

- Reduce `--populate-requests`
- Use smaller `--data-sizes`
- Increase Redis `maxmemory` configuration

### Timeout errors

- Increase `--test-time`
- Reduce `--benchmark-requests`
- Check network connectivity to Redis

## Advanced Configuration

### Custom Key Patterns

```bash
# Sequential keys
python redis_benchmark.py --key-pattern S:S --data-sizes 256 --ratios 1:1

# Gaussian distribution
python redis_benchmark.py --key-pattern G:G --data-sizes 256 --ratios 1:1
```

### Pipeline Testing

```bash
# Test with different pipeline depths
python redis_benchmark.py \
  --pipeline 10 \
  --data-sizes 64 256 \
  --ratios 1:1
```

### Skip Database Flush

```bash
# Don't flush between tests (faster but less isolated)
python redis_benchmark.py \
  --no-flush \
  --data-sizes 64 256 \
  --ratios 1:1
```

### Disable Visualizations

```bash
# Skip graph generation (faster)
python redis_benchmark.py \
  --no-visualize \
  --data-sizes 64 256 \
  --ratios 1:1
```

## Best Practices

1. **Warm-up**: Run a quick test first to warm up the system
2. **Isolation**: Run benchmarks on a dedicated Redis instance
3. **Consistency**: Use the same hardware and configuration for comparisons
4. **Multiple runs**: Run tests multiple times and average results
5. **Monitoring**: Monitor system resources (CPU, memory, network) during tests
6. **Documentation**: Keep notes about test conditions and configurations

## Contributing

Feel free to extend this tool with additional features:
- Support for Redis Cluster
- Additional visualization types
- Export to other formats (CSV, Excel)
- Real-time monitoring during tests
- Comparison between multiple benchmark runs

## License

This tool is provided as-is for Redis performance testing and analysis.

## References

- [Redis Documentation](https://redis.io/documentation)
- [memtier_benchmark Documentation](https://github.com/RedisLabs/memtier_benchmark)
- [Redis Benchmarking Best Practices](https://redis.io/topics/benchmarks)

