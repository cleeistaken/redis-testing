# Redis Benchmark Tool - Documentation Index

Welcome to the Redis Benchmark Tool! This index will help you navigate the documentation.

## 🚀 Quick Navigation

### For New Users

1. **[INSTALL.md](INSTALL.md)** - Complete installation guide
2. **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
3. **[README.md](README.md)** - Full documentation

### For Experienced Users

1. **[README.md](README.md)** - Command reference and examples
2. **[WORKFLOW.md](WORKFLOW.md)** - Technical workflow details
3. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Project overview

## 📚 Documentation Files

### Essential Documentation

| File | Purpose | When to Read |
|------|---------|--------------|
| **[README.md](README.md)** | Complete user guide | After installation |
| **[QUICKSTART.md](QUICKSTART.md)** | 5-minute tutorial | First time use |
| **[INSTALL.md](INSTALL.md)** | Installation instructions | Before starting |

### Technical Documentation

| File | Purpose | When to Read |
|------|---------|--------------|
| **[WORKFLOW.md](WORKFLOW.md)** | Technical workflow | Understanding internals |
| **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** | Project overview | Getting context |
| **[INDEX.md](INDEX.md)** | This file | Navigation |

## 🛠️ Script Files

### Main Scripts

| File | Purpose | Usage |
|------|---------|-------|
| **redis_benchmark.py** | Main benchmark script | `python redis_benchmark.py --help` |
| **visualize.py** | Visualization module | Imported automatically |
| **test_setup.py** | Setup verification | `python test_setup.py` |

### Helper Scripts

| File | Purpose | Usage |
|------|---------|-------|
| **run_example.sh** | Quick example | `./run_example.sh` |
| **run_comprehensive_test.sh** | Full benchmark | `./run_comprehensive_test.sh` |
| **view_results.sh** | Results viewer | `./view_results.sh` |

## 📋 Configuration Files

| File | Purpose |
|------|---------|
| **requirements.txt** | Python dependencies |
| **Pipfile** | Pipenv configuration |
| **example_config.json** | Sample configuration |
| **.gitignore** | Git ignore rules |

## 🎯 Common Tasks

### Installation

```bash
# 1. Check prerequisites
python test_setup.py

# 2. If missing, follow INSTALL.md
open INSTALL.md
```

### First Run

```bash
# 1. Read quick start
open QUICKSTART.md

# 2. Run example
./run_example.sh

# 3. View results
./view_results.sh
```

### Custom Benchmark

```bash
# 1. Read README for options
python redis_benchmark.py --help

# 2. Run custom benchmark
python redis_benchmark.py \
  --data-sizes 64 256 1024 \
  --ratios 1:1 1:10 10:1

# 3. Check results
ls -la results/graphs/
```

### Troubleshooting

```bash
# 1. Verify setup
python test_setup.py

# 2. Check INSTALL.md troubleshooting section
open INSTALL.md

# 3. Review logs
ls -lt logs/*.log | head -1 | xargs tail -50
```

## 📖 Reading Path by Role

### System Administrator

1. [INSTALL.md](INSTALL.md) - Install and configure
2. [QUICKSTART.md](QUICKSTART.md) - Quick validation
3. [README.md](README.md) - Command reference
4. Run: `./run_example.sh`

### Developer

1. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Project overview
2. [WORKFLOW.md](WORKFLOW.md) - Technical details
3. [README.md](README.md) - API and usage
4. Review: `redis_benchmark.py` and `visualize.py`

### Performance Engineer

1. [QUICKSTART.md](QUICKSTART.md) - Quick start
2. [README.md](README.md) - Advanced options
3. [WORKFLOW.md](WORKFLOW.md) - Understand metrics
4. Customize: Create your own test scripts

### Manager/Stakeholder

1. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - What it does
2. [QUICKSTART.md](QUICKSTART.md) - See it in action
3. Review: Sample graphs in `results/graphs/`

## 🔍 Finding Information

### Installation Issues

- **File**: [INSTALL.md](INSTALL.md)
- **Section**: Troubleshooting
- **Also check**: `test_setup.py` output

### Command-Line Options

- **File**: [README.md](README.md)
- **Section**: Command-Line Options
- **Also run**: `python redis_benchmark.py --help`

### Understanding Results

- **File**: [README.md](README.md)
- **Section**: Interpreting Results
- **Also check**: [WORKFLOW.md](WORKFLOW.md) - Data Flow

### Graph Explanations

- **File**: [README.md](README.md)
- **Section**: Visualization Graphs
- **Also check**: `visualize.py` docstrings

### Example Configurations

- **File**: [README.md](README.md)
- **Section**: Example Workflows
- **Also check**: `example_config.json`

### Technical Details

- **File**: [WORKFLOW.md](WORKFLOW.md)
- **Sections**: All
- **Also check**: Source code comments

## 📊 Output Files Guide

### After Running Benchmark

```
redis-testing/
├── logs/
│   └── benchmark_YYYYMMDD_HHMMSS.log    ← Detailed execution log
├── results/
│   ├── benchmark_results_YYYYMMDD_HHMMSS.json  ← Raw data
│   └── graphs/
│       ├── summary_dashboard.png         ← START HERE
│       ├── throughput_by_data_size.png   ← Performance trends
│       ├── latency_by_data_size.png      ← Latency trends
│       ├── throughput_by_ratio.png       ← Ratio comparison
│       ├── throughput_heatmap.png        ← Quick overview
│       ├── latency_heatmap.png           ← Latency overview
│       ├── get_set_comparison.png        ← Operation comparison
│       └── bandwidth_analysis.png        ← Network usage
```

### Which File to Check

| Question | File to Check |
|----------|---------------|
| Did it work? | `logs/benchmark_*.log` |
| What were the results? | Terminal output or `view_results.sh` |
| Which config was best? | `results/graphs/summary_dashboard.png` |
| How does data size affect performance? | `results/graphs/throughput_by_data_size.png` |
| How does ratio affect performance? | `results/graphs/throughput_by_ratio.png` |
| Raw data for analysis? | `results/benchmark_results_*.json` |

## 🎓 Learning Path

### Beginner Path

1. ✅ Install prerequisites ([INSTALL.md](INSTALL.md))
2. ✅ Verify setup (`python test_setup.py`)
3. ✅ Read quick start ([QUICKSTART.md](QUICKSTART.md))
4. ✅ Run example (`./run_example.sh`)
5. ✅ View results (`./view_results.sh`)
6. ✅ Understand output ([README.md](README.md) - Interpreting Results)

### Intermediate Path

1. ✅ Complete beginner path
2. ✅ Read full README ([README.md](README.md))
3. ✅ Try custom configurations
4. ✅ Experiment with different ratios and sizes
5. ✅ Compare results across runs
6. ✅ Understand all graph types

### Advanced Path

1. ✅ Complete intermediate path
2. ✅ Read workflow documentation ([WORKFLOW.md](WORKFLOW.md))
3. ✅ Review source code (`redis_benchmark.py`, `visualize.py`)
4. ✅ Create custom test scripts
5. ✅ Modify visualization code
6. ✅ Integrate with CI/CD

## 🔧 Customization Guide

### Custom Test Script

```bash
# Create your own test script
cat > my_test.sh << 'EOF'
#!/bin/bash
python redis_benchmark.py \
  --data-sizes 128 512 2048 \
  --ratios 1:1 1:5 5:1 \
  --test-time 90 \
  --benchmark-clients 75
EOF

chmod +x my_test.sh
./my_test.sh
```

### Custom Configuration File

```bash
# Copy example config
cp example_config.json my_config.json

# Edit as needed
nano my_config.json

# Use in script (modify redis_benchmark.py to load JSON)
```

### Custom Visualizations

Edit `visualize.py` to add new graph types:

```python
def plot_my_custom_graph(df, output_dir):
    # Your custom visualization
    pass

# Add to generate_visualizations()
```

## 📞 Support Resources

### Self-Help

1. Run diagnostics: `python test_setup.py`
2. Check logs: `tail -50 logs/benchmark_*.log`
3. Review troubleshooting: [INSTALL.md](INSTALL.md) - Troubleshooting

### Documentation

1. Search README: [README.md](README.md)
2. Check workflow: [WORKFLOW.md](WORKFLOW.md)
3. Review examples: [QUICKSTART.md](QUICKSTART.md)

## 🎯 Quick Reference Card

### Essential Commands

```bash
# Verify setup
python test_setup.py

# Run example
./run_example.sh

# Custom benchmark
python redis_benchmark.py --data-sizes 64 256 --ratios 1:1

# View results
./view_results.sh

# Check help
python redis_benchmark.py --help
```

### Essential Files

- **Main script**: `redis_benchmark.py`
- **Documentation**: `README.md`
- **Quick start**: `QUICKSTART.md`
- **Installation**: `INSTALL.md`

### Essential Directories

- **Logs**: `logs/`
- **Results**: `results/`
- **Graphs**: `results/graphs/`

## 📝 Version Information

- **Created**: November 2024
- **Python Version**: 3.13+ (3.8+ supported)
- **Redis Version**: Any recent version
- **memtier_benchmark**: Latest version

## 🚦 Status Indicators

When running benchmarks, watch for:

- ✅ **SUCCESS** - Test completed successfully
- ❌ **FAILED** - Test encountered an error
- ⚠️ **WARNING** - Non-critical issue

Check logs for details on any failures.

---

**Need help?** Start with [QUICKSTART.md](QUICKSTART.md) or run `python test_setup.py` to diagnose issues.

**Ready to begin?** Run `./run_example.sh` to see it in action!

**Want to learn more?** Read [README.md](README.md) for comprehensive documentation.

