#!/bin/bash
# Example script to run Redis benchmarks

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Redis Benchmark Example${NC}"
echo "================================"
echo ""

# Check if Redis is running
echo "Checking Redis connection..."
if redis-cli ping > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Redis is running${NC}"
else
    echo "✗ Redis is not running. Please start Redis first:"
    echo "  redis-server"
    exit 1
fi

# Check if memtier_benchmark is installed
echo "Checking memtier_benchmark..."
if command -v memtier_benchmark > /dev/null 2>&1; then
    echo -e "${GREEN}✓ memtier_benchmark is installed${NC}"
else
    echo "✗ memtier_benchmark is not installed. Please install it first:"
    echo "  brew install memtier-benchmark  # macOS"
    echo "  sudo apt-get install memtier-benchmark  # Ubuntu/Debian"
    exit 1
fi

# Check Python dependencies
echo "Checking Python dependencies..."
if python3 -c "import matplotlib, seaborn, pandas" 2>/dev/null; then
    echo -e "${GREEN}✓ Python dependencies installed${NC}"
else
    echo "✗ Python dependencies missing. Installing..."
    pip3 install -r requirements.txt
fi

echo ""
echo "================================"
echo "Running benchmark..."
echo "================================"
echo ""

# Run the benchmark
python3 redis_benchmark.py \
  --data-sizes 64 256 1024 \
  --ratios 1:1 1:10 10:1 \
  --test-time 30 \
  --wait-between-iterations 5

echo ""
echo "================================"
echo -e "${GREEN}Benchmark complete!${NC}"
echo "================================"
echo ""
echo "Check the following directories for results:"
echo "  - logs/          : Detailed execution logs"
echo "  - results/       : JSON results file"
echo "  - results/graphs/: Visualization graphs"

