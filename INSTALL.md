# Installation Guide

Complete installation instructions for the Redis Benchmark Tool.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [macOS Installation](#macos-installation)
3. [Linux Installation](#linux-installation)
4. [Python Setup](#python-setup)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements

- **OS**: macOS 10.14+, Ubuntu 18.04+, or similar Linux distribution
- **Python**: 3.8 or higher (3.13 recommended)
- **RAM**: 2GB minimum, 4GB+ recommended
- **Disk**: 500MB for software, additional space for results
- **Network**: Local or network access to Redis instance

### Software Dependencies

- Redis Server (any recent version)
- memtier_benchmark
- Python 3.8+
- pip (Python package manager)

## macOS Installation

### Step 1: Install Homebrew (if not already installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install Redis

```bash
# Install Redis
brew install redis

# Verify installation
redis-server --version

# Start Redis (option 1: foreground)
redis-server

# Start Redis (option 2: background)
brew services start redis

# Test Redis
redis-cli ping
# Should return: PONG
```

### Step 3: Install memtier_benchmark

```bash
# Install memtier_benchmark
brew install memtier-benchmark

# Verify installation
memtier_benchmark --version
```

### Step 4: Install Python Dependencies

```bash
# Navigate to project directory
cd /path/to/redis-testing

# Option 1: Using pip
pip3 install -r requirements.txt

# Option 2: Using pipenv
pip3 install pipenv
pipenv install
pipenv shell
```

### Step 5: Verify Setup

```bash
# Run verification script
python3 test_setup.py

# If all checks pass, you're ready!
```

## Linux Installation

### Ubuntu/Debian

#### Step 1: Update Package Lists

```bash
sudo apt-get update
```

#### Step 2: Install Redis

```bash
# Install Redis
sudo apt-get install -y redis-server

# Start Redis
sudo systemctl start redis-server

# Enable Redis to start on boot
sudo systemctl enable redis-server

# Verify Redis is running
redis-cli ping
# Should return: PONG
```

#### Step 3: Install memtier_benchmark

```bash
# Install dependencies
sudo apt-get install -y build-essential autoconf automake libpcre3-dev libevent-dev pkg-config zlib1g-dev

# Clone and build memtier_benchmark
cd /tmp
git clone https://github.com/RedisLabs/memtier_benchmark.git
cd memtier_benchmark
autoreconf -ivf
./configure
make
sudo make install

# Verify installation
memtier_benchmark --version
```

#### Step 4: Install Python and Dependencies

```bash
# Install Python 3 and pip
sudo apt-get install -y python3 python3-pip

# Navigate to project directory
cd /path/to/redis-testing

# Install Python packages
pip3 install -r requirements.txt
```

#### Step 5: Verify Setup

```bash
python3 test_setup.py
```

### CentOS/RHEL

#### Step 1: Install Redis

```bash
# Install EPEL repository
sudo yum install -y epel-release

# Install Redis
sudo yum install -y redis

# Start Redis
sudo systemctl start redis
sudo systemctl enable redis

# Verify
redis-cli ping
```

#### Step 2: Install memtier_benchmark

```bash
# Install dependencies
sudo yum install -y gcc make autoconf automake pcre-devel libevent-devel openssl-devel git

# Build from source (same as Ubuntu instructions above)
cd /tmp
git clone https://github.com/RedisLabs/memtier_benchmark.git
cd memtier_benchmark
autoreconf -ivf
./configure
make
sudo make install
```

#### Step 3: Install Python Dependencies

```bash
# Install Python 3 and pip
sudo yum install -y python3 python3-pip

# Install packages
cd /path/to/redis-testing
pip3 install -r requirements.txt
```

## Python Setup

### Using pip (Recommended for most users)

```bash
# Install packages globally
pip3 install -r requirements.txt

# Or install for current user only
pip3 install --user -r requirements.txt
```

### Using pipenv (Recommended for development)

```bash
# Install pipenv
pip3 install pipenv

# Install project dependencies
pipenv install

# Activate virtual environment
pipenv shell

# Now you can run scripts
python redis_benchmark.py --help
```

### Using virtualenv

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

## Verification

### Quick Verification

Run the automated setup verification script:

```bash
python3 test_setup.py
```

This will check:
- ✓ Python version
- ✓ Redis server installed
- ✓ Redis CLI installed
- ✓ memtier_benchmark installed
- ✓ Redis connection
- ✓ Python packages (matplotlib, seaborn, pandas)
- ✓ Project files
- ✓ Directory permissions

### Manual Verification

#### 1. Check Python Version

```bash
python3 --version
# Should be 3.8 or higher
```

#### 2. Check Redis

```bash
# Check if Redis is installed
redis-server --version

# Check if Redis is running
redis-cli ping
# Should return: PONG

# If not running, start it
redis-server &
```

#### 3. Check memtier_benchmark

```bash
memtier_benchmark --version
# Should show version information
```

#### 4. Check Python Packages

```bash
python3 -c "import matplotlib; print(f'matplotlib: {matplotlib.__version__}')"
python3 -c "import seaborn; print(f'seaborn: {seaborn.__version__}')"
python3 -c "import pandas; print(f'pandas: {pandas.__version__}')"
```

#### 5. Test Benchmark Script

```bash
# Show help
python3 redis_benchmark.py --help

# Run quick test (if Redis is running)
python3 redis_benchmark.py --data-sizes 64 --ratios 1:1 --test-time 10
```

## Troubleshooting

### Redis Issues

#### Redis won't start

```bash
# Check if Redis is already running
ps aux | grep redis-server

# Check Redis logs
tail -f /usr/local/var/log/redis.log  # macOS
tail -f /var/log/redis/redis-server.log  # Linux

# Try starting with verbose output
redis-server --loglevel verbose
```

#### Connection refused

```bash
# Check if Redis is listening
netstat -an | grep 6379

# Check Redis configuration
redis-cli CONFIG GET bind
redis-cli CONFIG GET port

# Try connecting with explicit host/port
redis-cli -h 127.0.0.1 -p 6379 ping
```

#### Permission denied

```bash
# Check Redis data directory permissions
ls -la /var/lib/redis  # Linux
ls -la /usr/local/var/db/redis  # macOS

# Fix permissions if needed
sudo chown redis:redis /var/lib/redis  # Linux
```

### memtier_benchmark Issues

#### Command not found

```bash
# Check if installed
which memtier_benchmark

# Check PATH
echo $PATH

# If installed but not in PATH, use full path
/usr/local/bin/memtier_benchmark --version
```

#### Build errors (Linux)

```bash
# Install missing dependencies
sudo apt-get install -y build-essential autoconf automake libpcre3-dev libevent-dev pkg-config zlib1g-dev

# Clean and rebuild
cd memtier_benchmark
make clean
autoreconf -ivf
./configure
make
sudo make install
```

### Python Issues

#### Module not found

```bash
# Verify pip installation
pip3 list | grep -E "matplotlib|seaborn|pandas"

# Reinstall if needed
pip3 install --upgrade matplotlib seaborn pandas

# Check Python path
python3 -c "import sys; print('\n'.join(sys.path))"
```

#### Version conflicts

```bash
# Create isolated environment
python3 -m venv venv_redis
source venv_redis/bin/activate
pip install -r requirements.txt
```

#### Permission errors

```bash
# Install for user only
pip3 install --user -r requirements.txt

# Or use sudo (not recommended)
sudo pip3 install -r requirements.txt
```

### Performance Issues

#### Slow benchmarks

- Reduce test time: `--test-time 30`
- Reduce requests: `--benchmark-requests 5000`
- Check system resources: `top` or `htop`
- Close other applications

#### Out of memory

- Reduce data sizes
- Reduce number of clients: `--benchmark-clients 25`
- Configure Redis maxmemory
- Monitor with: `redis-cli INFO memory`

### Visualization Issues

#### No graphs generated

```bash
# Check if matplotlib backend is working
python3 -c "import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt; print('OK')"

# Install missing dependencies
pip3 install --upgrade matplotlib seaborn pandas

# Check results directory
ls -la results/graphs/
```

#### Display errors

```bash
# Use non-interactive backend (already set in visualize.py)
export MPLBACKEND=Agg
python3 redis_benchmark.py --data-sizes 64 --ratios 1:1
```

## Post-Installation

### Configure Redis (Optional)

```bash
# Edit Redis configuration
sudo nano /etc/redis/redis.conf  # Linux
nano /usr/local/etc/redis.conf  # macOS

# Recommended settings for benchmarking:
# maxmemory 2gb
# maxmemory-policy allkeys-lru
# save ""  # Disable persistence for pure performance testing
```

### Create Aliases (Optional)

Add to `~/.bashrc` or `~/.zshrc`:

```bash
alias redis-bench='cd /path/to/redis-testing && python3 redis_benchmark.py'
alias redis-results='cd /path/to/redis-testing && ./view_results.sh'
alias redis-test='cd /path/to/redis-testing && python3 test_setup.py'
```

### Schedule Regular Benchmarks (Optional)

```bash
# Add to crontab
crontab -e

# Run benchmark daily at 2 AM
0 2 * * * cd /path/to/redis-testing && python3 redis_benchmark.py --data-sizes 64 256 1024 --ratios 1:1 1:10 10:1
```

## Next Steps

After successful installation:

1. Read [QUICKSTART.md](QUICKSTART.md) for a 5-minute introduction
2. Run the example: `./run_example.sh`
3. Read [README.md](README.md) for comprehensive documentation
4. Explore [WORKFLOW.md](WORKFLOW.md) to understand the internals

## Getting Help

If you encounter issues:

1. Run `python3 test_setup.py` to diagnose problems
2. Check the troubleshooting section above
3. Review logs in `logs/` directory
4. Check Redis logs
5. Verify all prerequisites are installed

## Uninstallation

To remove the benchmark tool:

```bash
# Remove Python packages (if using virtualenv)
deactivate
rm -rf venv

# Remove project directory
cd ..
rm -rf redis-testing

# Optionally remove Redis and memtier_benchmark
brew uninstall redis memtier-benchmark  # macOS
sudo apt-get remove redis-server  # Linux
```

---

**Installation complete!** You're ready to benchmark Redis. 🚀

