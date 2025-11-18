# Redis Benchmark Tool - Workflow Documentation

## High-Level Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                     START BENCHMARK                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  Parse Configuration                                             │
│  • Command-line arguments                                        │
│  • Validate Redis connection                                     │
│  • Setup logging                                                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  Generate Test Matrix                                            │
│  • Data Sizes: [64, 256, 1024]                                  │
│  • Ratios: [1:1, 1:10, 10:1]                                    │
│  • Total Tests: 3 × 3 = 9                                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │  For Each Test  │◄─────────┐
                    └────────┬───────┘          │
                             │                  │
                             ▼                  │
        ┌─────────────────────────────────────┐│
        │  STEP 1: Flush Database (Optional)  ││
        │  • redis-cli FLUSHALL               ││
        │  • Wait 2 seconds                   ││
        └────────────────┬────────────────────┘│
                         │                     │
                         ▼                     │
        ┌─────────────────────────────────────┐│
        │  STEP 2: Populate Database          ││
        │  • memtier_benchmark                ││
        │    --ratio 1:0 (write-only)         ││
        │    --data-size <SIZE>               ││
        │    --requests <N>                   ││
        │  • Parse population metrics         ││
        └────────────────┬────────────────────┘│
                         │                     │
                         ▼                     │
        ┌─────────────────────────────────────┐│
        │  Wait Between Operations            ││
        │  • Default: 5 seconds               ││
        └────────────────┬────────────────────┘│
                         │                     │
                         ▼                     │
        ┌─────────────────────────────────────┐│
        │  STEP 3: Run Benchmark              ││
        │  • memtier_benchmark                ││
        │    --ratio <RATIO>                  ││
        │    --data-size <SIZE>               ││
        │    --test-time <SECONDS>            ││
        │  • Parse benchmark metrics          ││
        └────────────────┬────────────────────┘│
                         │                     │
                         ▼                     │
        ┌─────────────────────────────────────┐│
        │  Store Results                      ││
        │  • Ops/sec, Latency, Bandwidth      ││
        │  • GET/SET specific metrics         ││
        └────────────────┬────────────────────┘│
                         │                     │
                         ▼                     │
        ┌─────────────────────────────────────┐│
        │  Wait Between Iterations            ││
        │  • Default: 10 seconds              ││
        └────────────────┬────────────────────┘│
                         │                     │
                         └─────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  Generate Summary Statistics                                     │
│  • Aggregate by data size                                        │
│  • Aggregate by ratio                                            │
│  • Calculate averages                                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  Save Results                                                    │
│  • JSON file with all data                                       │
│  • Timestamped filename                                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  Generate Text Report                                            │
│  • Summary table                                                 │
│  • Detailed results                                              │
│  • Aggregated statistics                                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  Generate Visualizations                                         │
│  • 8 different graph types                                       │
│  • High-resolution PNG files                                     │
│  • Saved to results/graphs/                                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     BENCHMARK COMPLETE                           │
└─────────────────────────────────────────────────────────────────┘
```

## Detailed Component Interactions

### 1. Initialization Phase

```
User Input (CLI)
      │
      ▼
┌──────────────┐
│ ArgumentParser│
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ Config Dictionary │
└──────┬───────────┘
       │
       ▼
┌─────────────────────────┐
│ RedisMemtierBenchmark   │
│ • Setup logging         │
│ • Validate connection   │
└─────────────────────────┘
```

### 2. Test Execution Phase

```
Test Matrix (N × M tests)
         │
         ▼
    ┌─────────┐
    │ Test Loop│
    └────┬────┘
         │
         ├─► Flush DB ──► redis-cli FLUSHALL
         │
         ├─► Populate ──► memtier_benchmark (write-only)
         │                      │
         │                      ▼
         │                Parse JSON output
         │                      │
         │                      ▼
         │                Extract metrics
         │
         ├─► Wait ──► time.sleep(N)
         │
         ├─► Benchmark ──► memtier_benchmark (mixed workload)
         │                      │
         │                      ▼
         │                Parse JSON output
         │                      │
         │                      ▼
         │                Extract metrics
         │
         └─► Store ──► results.append(data)
```

### 3. Results Processing Phase

```
Raw Results List
      │
      ▼
┌──────────────────┐
│ Generate Summary │
│ • Count tests    │
│ • Calculate avgs │
│ • Group by dims  │
└────┬─────────────┘
     │
     ├─► Save JSON ──► results/benchmark_results_*.json
     │
     ├─► Print Report ──► Terminal output
     │
     └─► Visualize ──► visualize.py
                           │
                           ├─► Convert to DataFrame
                           │
                           ├─► Generate 8 graphs
                           │
                           └─► Save PNGs
```

## Data Flow

### Input Data

```
Command Line Arguments
├── Redis Connection
│   ├── --host
│   ├── --port
│   └── --password
├── Test Parameters
│   ├── --data-sizes [64, 256, 1024]
│   └── --ratios [1:1, 1:10, 10:1]
├── Memtier Settings
│   ├── --clients
│   ├── --threads
│   ├── --requests
│   └── --test-time
└── Timing Settings
    ├── --wait-between-operations
    └── --wait-between-iterations
```

### Intermediate Data

```
memtier_benchmark JSON Output
├── ALL STATS
│   ├── Totals
│   │   ├── Ops/sec
│   │   ├── Hits/sec
│   │   ├── Misses/sec
│   │   ├── Latency
│   │   └── KB/sec
│   ├── Gets
│   │   ├── Ops/sec
│   │   └── Latency
│   └── Sets
│       ├── Ops/sec
│       └── Latency
```

### Output Data

```
Results Structure
├── config: {...}
├── results: [
│   {
│     data_size: 64,
│     ratio: "1:1",
│     timestamp: "2024-11-18T14:30:22",
│     success: true,
│     populate_metrics: {...},
│     benchmark_metrics: {
│       ops_per_sec: 45231.5,
│       latency_avg: 1.10,
│       get_ops_per_sec: 22615.75,
│       set_ops_per_sec: 22615.75,
│       ...
│     }
│   },
│   ...
│ ]
└── summary: {
    total_tests: 9,
    successful_tests: 9,
    by_data_size: {...},
    by_ratio: {...}
  }
```

## Error Handling Flow

```
Operation Attempt
      │
      ▼
   Try Block
      │
      ├─► Success ──► Continue
      │
      └─► Failure
            │
            ▼
       Log Error
            │
            ▼
      Mark Test Failed
            │
            ▼
      Store Error Info
            │
            ▼
      Continue to Next Test
```

## Timing Diagram

```
Time ──────────────────────────────────────────────────►

Test 1:
├─ Flush (2s)
├─ Populate (variable)
├─ Wait (5s)
├─ Benchmark (60s)
└─ Wait (10s)
                Test 2:
                ├─ Flush (2s)
                ├─ Populate (variable)
                ├─ Wait (5s)
                ├─ Benchmark (60s)
                └─ Wait (10s)
                                Test 3:
                                ├─ Flush (2s)
                                ├─ Populate (variable)
                                ├─ Wait (5s)
                                ├─ Benchmark (60s)
                                └─ Wait (10s)
                                                ...
```

## File Operations

```
Benchmark Start
      │
      ├─► Create logs/ directory
      │   └─► Create benchmark_TIMESTAMP.log
      │
      ├─► Create results/ directory
      │   ├─► Create benchmark_results_TIMESTAMP.json
      │   └─► Create graphs/ directory
      │       ├─► throughput_by_data_size.png
      │       ├─► latency_by_data_size.png
      │       ├─► throughput_by_ratio.png
      │       ├─► throughput_heatmap.png
      │       ├─► latency_heatmap.png
      │       ├─► get_set_comparison.png
      │       ├─► bandwidth_analysis.png
      │       └─► summary_dashboard.png
      │
      └─► Create /tmp/ files (temporary)
          ├─► memtier_populate.json
          └─► memtier_benchmark.json
```

## Parallel vs Sequential Operations

### Sequential (Current Implementation)

```
Test 1 → Test 2 → Test 3 → ... → Test N
  │        │        │              │
  └────────┴────────┴──────────────┴─► Results
```

### Why Sequential?

1. **Database State**: Each test needs clean state
2. **Resource Contention**: Avoid competing for Redis
3. **Accurate Metrics**: Isolated measurements
4. **Reproducibility**: Consistent conditions

## Memory Management

```
┌──────────────────────────────────┐
│ Benchmark Object                  │
│ ├─ config (small)                │
│ ├─ results list (grows)          │
│ │  └─ ~1KB per test result       │
│ └─ logger (small)                │
└──────────────────────────────────┘

For 100 tests: ~100KB memory
For 1000 tests: ~1MB memory
```

## Performance Characteristics

### Time Complexity

- **Per Test**: O(1) - fixed operations
- **Total**: O(N × M) where N = data sizes, M = ratios
- **Visualization**: O(N × M) - processes all results

### Space Complexity

- **Results Storage**: O(N × M) - one result per test
- **Graphs**: O(1) - fixed number of graphs
- **Logs**: O(N × M) - proportional to tests

### Typical Runtimes

```
Configuration          | Tests | Time per Test | Total Time
-----------------------|-------|---------------|------------
Quick (3×3)           | 9     | ~90s          | ~15 min
Standard (4×4)        | 16    | ~90s          | ~25 min
Comprehensive (8×9)   | 72    | ~150s         | ~3 hours
```

## Extension Points

### Adding New Metrics

```python
def parse_memtier_output(self, output: str, json_file: str):
    # Add new metric extraction here
    metrics['new_metric'] = extract_new_metric(json_data)
    return metrics
```

### Adding New Visualizations

```python
def plot_new_visualization(df: pd.DataFrame, output_dir: Path):
    # Create new graph type
    fig, ax = plt.subplots()
    # ... plotting code ...
    plt.savefig(output_dir / 'new_graph.png')
```

### Custom Commands

```python
def build_custom_command(self, params):
    cmd = ['memtier_benchmark']
    # Add custom parameters
    return cmd
```

---

This workflow ensures reliable, reproducible Redis benchmarking with comprehensive reporting and visualization.

