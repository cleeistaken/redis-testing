#!/bin/bash
# Helper script to view benchmark results

echo "Redis Benchmark Results Viewer"
echo "==============================="
echo ""

# Check if results exist
if [ ! -d "results" ]; then
    echo "No results directory found. Run a benchmark first!"
    exit 1
fi

# Count results
result_count=$(ls results/*.json 2>/dev/null | wc -l)
if [ $result_count -eq 0 ]; then
    echo "No results found. Run a benchmark first!"
    exit 1
fi

echo "Found $result_count benchmark result(s)"
echo ""

# Show menu
echo "What would you like to view?"
echo "1) Latest results summary (JSON)"
echo "2) Latest log file"
echo "3) List all results"
echo "4) Open graphs folder"
echo "5) Show latest results as table"
echo ""
read -p "Enter choice (1-5): " choice

case $choice in
    1)
        echo ""
        echo "Latest Results:"
        echo "==============="
        latest=$(ls -t results/*.json | head -1)
        echo "File: $latest"
        echo ""
        cat "$latest" | python3 -m json.tool | less
        ;;
    2)
        echo ""
        echo "Latest Log:"
        echo "==========="
        latest_log=$(ls -t logs/*.log 2>/dev/null | head -1)
        if [ -z "$latest_log" ]; then
            echo "No logs found"
        else
            echo "File: $latest_log"
            echo ""
            less "$latest_log"
        fi
        ;;
    3)
        echo ""
        echo "All Results:"
        echo "============"
        ls -lht results/*.json
        ;;
    4)
        echo ""
        if [ -d "results/graphs" ]; then
            echo "Opening graphs folder..."
            if [[ "$OSTYPE" == "darwin"* ]]; then
                open results/graphs/
            elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
                xdg-open results/graphs/ 2>/dev/null || echo "Please open: results/graphs/"
            else
                echo "Please open: results/graphs/"
            fi
        else
            echo "No graphs found. Make sure visualizations were generated."
        fi
        ;;
    5)
        echo ""
        echo "Latest Results Summary:"
        echo "======================="
        latest=$(ls -t results/*.json | head -1)
        echo "File: $latest"
        echo ""
        python3 << 'EOF'
import json
import sys

try:
    with open(sys.argv[1], 'r') as f:
        data = json.load(f)
    
    print("\nConfiguration:")
    print(f"  Data Sizes: {data['config']['data_sizes']}")
    print(f"  Ratios: {data['config']['ratios']}")
    print(f"  Test Time: {data['config']['test_time']}s")
    
    print("\nSummary:")
    summary = data['summary']
    print(f"  Total Tests: {summary['total_tests']}")
    print(f"  Successful: {summary['successful_tests']}")
    print(f"  Failed: {summary['failed_tests']}")
    
    print("\n{:<15} {:<15} {:<20} {:<20}".format("Data Size", "Ratio", "Ops/sec", "Latency (ms)"))
    print("-" * 70)
    
    for result in data['results']:
        if result.get('success'):
            metrics = result.get('benchmark_metrics', {})
            print("{:<15} {:<15} {:<20.2f} {:<20.2f}".format(
                result['data_size'],
                result['ratio'],
                metrics.get('ops_per_sec', 0),
                metrics.get('latency_avg', 0)
            ))
    
except Exception as e:
    print(f"Error reading results: {e}")
EOF
python3 -c "import sys; exec(open('/dev/stdin').read())" "$latest"
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

