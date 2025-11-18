#!/usr/bin/env python3
"""
Redis Benchmark Script using memtier_benchmark

This script runs comprehensive Redis benchmarks with different data sizes and read/write ratios.
It handles population, testing, cleaning, and generates detailed reports with visualizations.
"""

import argparse
import subprocess
import json
import time
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Tuple
import re


class RedisMemtierBenchmark:
    """Main class for running Redis benchmarks with memtier_benchmark"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.results = []
        self.setup_logging()
        
    def setup_logging(self):
        """Configure logging for the benchmark"""
        log_dir = Path(self.config.get('log_dir', 'logs'))
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f'benchmark_{timestamp}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Benchmark started with config: {json.dumps(self.config, indent=2)}")
        
    def build_populate_command(self, data_size: int) -> List[str]:
        """Build the memtier command for populating the database"""
        cmd = [
            'memtier_benchmark',
            '--server', self.config['redis_host'],
            '--port', str(self.config['redis_port']),
            '--protocol', self.config.get('protocol', 'redis'),
            '--clients', str(self.config.get('populate_clients', 50)),
            '--threads', str(self.config.get('populate_threads', 4)),
            '--requests', str(self.config.get('populate_requests', 10000)),
            '--data-size', str(data_size),
            '--key-pattern', self.config.get('key_pattern', 'R:R'),
            '--ratio', '1:0',  # Write-only for population
            '--pipeline', str(self.config.get('pipeline', 1)),
        ]
        
        # Add authentication if provided
        if self.config.get('redis_password'):
            cmd.extend(['--authenticate', self.config['redis_password']])
            
        # Add JSON output
        cmd.extend(['--json-out-file', '/tmp/memtier_populate.json'])
        
        return cmd
    
    def build_benchmark_command(self, data_size: int, ratio: str) -> List[str]:
        """Build the memtier command for running the benchmark"""
        cmd = [
            'memtier_benchmark',
            '--server', self.config['redis_host'],
            '--port', str(self.config['redis_port']),
            '--protocol', self.config.get('protocol', 'redis'),
            '--clients', str(self.config.get('benchmark_clients', 50)),
            '--threads', str(self.config.get('benchmark_threads', 4)),
            '--requests', str(self.config.get('benchmark_requests', 10000)),
            '--data-size', str(data_size),
            '--key-pattern', self.config.get('key_pattern', 'R:R'),
            '--ratio', ratio,
            '--pipeline', str(self.config.get('pipeline', 1)),
            '--test-time', str(self.config.get('test_time', 60)),
        ]
        
        # Add authentication if provided
        if self.config.get('redis_password'):
            cmd.extend(['--authenticate', self.config['redis_password']])
            
        # Add JSON output
        cmd.extend(['--json-out-file', '/tmp/memtier_benchmark.json'])
        
        return cmd
    
    def run_command(self, cmd: List[str], operation: str) -> Tuple[bool, str]:
        """Execute a memtier command and capture output"""
        self.logger.info(f"Running {operation}: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.config.get('command_timeout', 600)
            )
            
            if result.returncode == 0:
                self.logger.info(f"{operation} completed successfully")
                return True, result.stdout
            else:
                self.logger.error(f"{operation} failed with return code {result.returncode}")
                self.logger.error(f"Error output: {result.stderr}")
                return False, result.stderr
                
        except subprocess.TimeoutExpired:
            self.logger.error(f"{operation} timed out")
            return False, "Command timed out"
        except Exception as e:
            self.logger.error(f"{operation} failed with exception: {str(e)}")
            return False, str(e)
    
    def parse_memtier_output(self, output: str, json_file: str) -> Dict[str, Any]:
        """Parse memtier output and extract key metrics"""
        metrics = {}
        
        # Try to read JSON output first
        try:
            json_path = Path(json_file)
            if json_path.exists():
                with open(json_path, 'r') as f:
                    json_data = json.load(f)
                    
                # Extract key metrics from JSON
                if 'ALL STATS' in json_data:
                    stats = json_data['ALL STATS']
                    metrics['ops_per_sec'] = stats.get('Totals', {}).get('Ops/sec', 0)
                    metrics['hits_per_sec'] = stats.get('Totals', {}).get('Hits/sec', 0)
                    metrics['misses_per_sec'] = stats.get('Totals', {}).get('Misses/sec', 0)
                    metrics['latency_avg'] = stats.get('Totals', {}).get('Latency', 0)
                    metrics['bandwidth_kb_sec'] = stats.get('Totals', {}).get('KB/sec', 0)
                    
                    # GET and SET specific metrics
                    if 'Gets' in stats:
                        metrics['get_latency_avg'] = stats['Gets'].get('Latency', 0)
                        metrics['get_ops_per_sec'] = stats['Gets'].get('Ops/sec', 0)
                    
                    if 'Sets' in stats:
                        metrics['set_latency_avg'] = stats['Sets'].get('Latency', 0)
                        metrics['set_ops_per_sec'] = stats['Sets'].get('Ops/sec', 0)
                        
        except Exception as e:
            self.logger.warning(f"Failed to parse JSON output: {str(e)}")
        
        # Fallback: parse text output
        if not metrics:
            metrics = self.parse_text_output(output)
        
        return metrics
    
    def parse_text_output(self, output: str) -> Dict[str, Any]:
        """Parse text output as fallback"""
        metrics = {}
        
        # Extract throughput
        throughput_match = re.search(r'Totals\s+(\d+\.\d+)', output)
        if throughput_match:
            metrics['ops_per_sec'] = float(throughput_match.group(1))
        
        # Extract latency
        latency_match = re.search(r'Latency\s+(\d+\.\d+)', output)
        if latency_match:
            metrics['latency_avg'] = float(latency_match.group(1))
        
        return metrics
    
    def flush_redis(self):
        """Flush the Redis database"""
        self.logger.info("Flushing Redis database...")
        
        try:
            cmd = ['redis-cli', '-h', self.config['redis_host'], '-p', str(self.config['redis_port'])]
            
            if self.config.get('redis_password'):
                cmd.extend(['-a', self.config['redis_password']])
            
            cmd.append('FLUSHALL')
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self.logger.info("Redis database flushed successfully")
                return True
            else:
                self.logger.error(f"Failed to flush Redis: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to flush Redis: {str(e)}")
            return False
    
    def run_single_benchmark(self, data_size: int, ratio: str) -> Dict[str, Any]:
        """Run a single benchmark iteration"""
        self.logger.info(f"\n{'='*80}")
        self.logger.info(f"Starting benchmark: data_size={data_size}, ratio={ratio}")
        self.logger.info(f"{'='*80}")
        
        result = {
            'data_size': data_size,
            'ratio': ratio,
            'timestamp': datetime.now().isoformat(),
            'success': False
        }
        
        try:
            # Step 1: Flush database
            if self.config.get('flush_before_test', True):
                if not self.flush_redis():
                    result['error'] = 'Failed to flush database'
                    return result
                time.sleep(2)  # Wait for flush to complete
            
            # Step 2: Populate database
            self.logger.info("Step 1/2: Populating database...")
            populate_cmd = self.build_populate_command(data_size)
            success, output = self.run_command(populate_cmd, "Population")
            
            if not success:
                result['error'] = 'Population failed'
                return result
            
            result['populate_metrics'] = self.parse_memtier_output(output, '/tmp/memtier_populate.json')
            
            # Wait between populate and benchmark
            wait_time = self.config.get('wait_between_operations', 5)
            self.logger.info(f"Waiting {wait_time} seconds before benchmark...")
            time.sleep(wait_time)
            
            # Step 3: Run benchmark
            self.logger.info("Step 2/2: Running benchmark...")
            benchmark_cmd = self.build_benchmark_command(data_size, ratio)
            success, output = self.run_command(benchmark_cmd, "Benchmark")
            
            if not success:
                result['error'] = 'Benchmark failed'
                return result
            
            result['benchmark_metrics'] = self.parse_memtier_output(output, '/tmp/memtier_benchmark.json')
            result['success'] = True
            
        except Exception as e:
            self.logger.error(f"Benchmark failed with exception: {str(e)}")
            result['error'] = str(e)
        
        return result
    
    def run_all_benchmarks(self):
        """Run all benchmark permutations"""
        data_sizes = self.config['data_sizes']
        ratios = self.config['ratios']
        
        total_tests = len(data_sizes) * len(ratios)
        current_test = 0
        
        self.logger.info(f"Starting {total_tests} benchmark tests")
        self.logger.info(f"Data sizes: {data_sizes}")
        self.logger.info(f"Ratios: {ratios}")
        
        for data_size in data_sizes:
            for ratio in ratios:
                current_test += 1
                self.logger.info(f"\nProgress: {current_test}/{total_tests}")
                
                result = self.run_single_benchmark(data_size, ratio)
                self.results.append(result)
                
                # Wait between iterations
                if current_test < total_tests:
                    wait_time = self.config.get('wait_between_iterations', 10)
                    self.logger.info(f"Waiting {wait_time} seconds before next iteration...")
                    time.sleep(wait_time)
        
        self.logger.info(f"\nAll benchmarks completed. Total tests: {total_tests}")
        return self.results
    
    def save_results(self):
        """Save results to JSON file"""
        results_dir = Path(self.config.get('results_dir', 'results'))
        results_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_file = results_dir / f'benchmark_results_{timestamp}.json'
        
        with open(results_file, 'w') as f:
            json.dump({
                'config': self.config,
                'results': self.results,
                'summary': self.generate_summary()
            }, f, indent=2)
        
        self.logger.info(f"Results saved to {results_file}")
        return results_file


def generate_summary(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate summary statistics from results"""
    summary = {
        'total_tests': len(results),
        'successful_tests': sum(1 for r in results if r.get('success', False)),
        'failed_tests': sum(1 for r in results if not r.get('success', False)),
        'by_data_size': {},
        'by_ratio': {}
    }
    
    # Aggregate by data size
    for result in results:
        if not result.get('success'):
            continue
            
        data_size = result['data_size']
        ratio = result['ratio']
        
        if data_size not in summary['by_data_size']:
            summary['by_data_size'][data_size] = {
                'count': 0,
                'avg_ops_per_sec': 0,
                'avg_latency': 0
            }
        
        if ratio not in summary['by_ratio']:
            summary['by_ratio'][ratio] = {
                'count': 0,
                'avg_ops_per_sec': 0,
                'avg_latency': 0
            }
        
        metrics = result.get('benchmark_metrics', {})
        ops = metrics.get('ops_per_sec', 0)
        latency = metrics.get('latency_avg', 0)
        
        # Update data size stats
        ds_stats = summary['by_data_size'][data_size]
        ds_stats['count'] += 1
        ds_stats['avg_ops_per_sec'] = (ds_stats['avg_ops_per_sec'] * (ds_stats['count'] - 1) + ops) / ds_stats['count']
        ds_stats['avg_latency'] = (ds_stats['avg_latency'] * (ds_stats['count'] - 1) + latency) / ds_stats['count']
        
        # Update ratio stats
        r_stats = summary['by_ratio'][ratio]
        r_stats['count'] += 1
        r_stats['avg_ops_per_sec'] = (r_stats['avg_ops_per_sec'] * (r_stats['count'] - 1) + ops) / r_stats['count']
        r_stats['avg_latency'] = (r_stats['avg_latency'] * (r_stats['count'] - 1) + latency) / r_stats['count']
    
    return summary


def print_text_report(results: List[Dict[str, Any]], summary: Dict[str, Any]):
    """Print a formatted text report"""
    print("\n" + "="*100)
    print("REDIS BENCHMARK RESULTS SUMMARY")
    print("="*100)
    
    print(f"\nTotal Tests: {summary['total_tests']}")
    print(f"Successful: {summary['successful_tests']}")
    print(f"Failed: {summary['failed_tests']}")
    
    print("\n" + "-"*100)
    print("DETAILED RESULTS")
    print("-"*100)
    
    print(f"\n{'Data Size':<15} {'Ratio':<15} {'Ops/sec':<20} {'Latency (ms)':<20} {'Status':<15}")
    print("-"*100)
    
    for result in results:
        data_size = result['data_size']
        ratio = result['ratio']
        success = result.get('success', False)
        
        if success:
            metrics = result.get('benchmark_metrics', {})
            ops = metrics.get('ops_per_sec', 0)
            latency = metrics.get('latency_avg', 0)
            status = "SUCCESS"
            print(f"{data_size:<15} {ratio:<15} {ops:<20.2f} {latency:<20.2f} {status:<15}")
        else:
            error = result.get('error', 'Unknown error')
            print(f"{data_size:<15} {ratio:<15} {'N/A':<20} {'N/A':<20} FAILED: {error}")
    
    print("\n" + "-"*100)
    print("SUMMARY BY DATA SIZE")
    print("-"*100)
    
    print(f"\n{'Data Size':<20} {'Avg Ops/sec':<25} {'Avg Latency (ms)':<25}")
    print("-"*100)
    
    for data_size, stats in sorted(summary['by_data_size'].items()):
        print(f"{data_size:<20} {stats['avg_ops_per_sec']:<25.2f} {stats['avg_latency']:<25.2f}")
    
    print("\n" + "-"*100)
    print("SUMMARY BY RATIO")
    print("-"*100)
    
    print(f"\n{'Ratio':<20} {'Avg Ops/sec':<25} {'Avg Latency (ms)':<25}")
    print("-"*100)
    
    for ratio, stats in sorted(summary['by_ratio'].items()):
        print(f"{ratio:<20} {stats['avg_ops_per_sec']:<25.2f} {stats['avg_latency']:<25.2f}")
    
    print("\n" + "="*100)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Redis Benchmark Tool using memtier_benchmark',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic benchmark with default settings
  python redis_benchmark.py --data-sizes 64 256 1024 --ratios 1:1 1:10 10:1
  
  # Custom Redis connection
  python redis_benchmark.py --host 192.168.1.100 --port 6380 --password mypass \\
    --data-sizes 128 512 --ratios 1:1 5:1
  
  # Extended benchmark with custom timing
  python redis_benchmark.py --data-sizes 64 256 512 1024 --ratios 1:1 1:5 1:10 \\
    --test-time 120 --wait-between-iterations 30
        """
    )
    
    # Redis connection settings
    parser.add_argument('--host', default='localhost', help='Redis host (default: localhost)')
    parser.add_argument('--port', type=int, default=6379, help='Redis port (default: 6379)')
    parser.add_argument('--password', default=None, help='Redis password')
    
    # Benchmark parameters
    parser.add_argument('--data-sizes', type=int, nargs='+', required=True,
                        help='List of data sizes in bytes (e.g., 64 256 1024)')
    parser.add_argument('--ratios', type=str, nargs='+', required=True,
                        help='List of SET:GET ratios (e.g., 1:1 1:10 10:1)')
    
    # Memtier settings
    parser.add_argument('--populate-clients', type=int, default=50,
                        help='Number of clients for population (default: 50)')
    parser.add_argument('--populate-threads', type=int, default=4,
                        help='Number of threads for population (default: 4)')
    parser.add_argument('--populate-requests', type=int, default=10000,
                        help='Number of requests per client for population (default: 10000)')
    
    parser.add_argument('--benchmark-clients', type=int, default=50,
                        help='Number of clients for benchmark (default: 50)')
    parser.add_argument('--benchmark-threads', type=int, default=4,
                        help='Number of threads for benchmark (default: 4)')
    parser.add_argument('--benchmark-requests', type=int, default=10000,
                        help='Number of requests per client for benchmark (default: 10000)')
    parser.add_argument('--test-time', type=int, default=60,
                        help='Test duration in seconds (default: 60)')
    
    parser.add_argument('--pipeline', type=int, default=1,
                        help='Pipeline depth (default: 1)')
    parser.add_argument('--key-pattern', default='R:R',
                        help='Key pattern (default: R:R for random)')
    
    # Timing settings
    parser.add_argument('--wait-between-operations', type=int, default=5,
                        help='Wait time between populate and benchmark (default: 5s)')
    parser.add_argument('--wait-between-iterations', type=int, default=10,
                        help='Wait time between test iterations (default: 10s)')
    
    # Other settings
    parser.add_argument('--no-flush', action='store_true',
                        help='Do not flush database before each test')
    parser.add_argument('--log-dir', default='logs', help='Log directory (default: logs)')
    parser.add_argument('--results-dir', default='results', help='Results directory (default: results)')
    parser.add_argument('--no-visualize', action='store_true',
                        help='Skip generating visualization graphs')
    
    args = parser.parse_args()
    
    # Build configuration
    config = {
        'redis_host': args.host,
        'redis_port': args.port,
        'redis_password': args.password,
        'data_sizes': args.data_sizes,
        'ratios': args.ratios,
        'populate_clients': args.populate_clients,
        'populate_threads': args.populate_threads,
        'populate_requests': args.populate_requests,
        'benchmark_clients': args.benchmark_clients,
        'benchmark_threads': args.benchmark_threads,
        'benchmark_requests': args.benchmark_requests,
        'test_time': args.test_time,
        'pipeline': args.pipeline,
        'key_pattern': args.key_pattern,
        'wait_between_operations': args.wait_between_operations,
        'wait_between_iterations': args.wait_between_iterations,
        'flush_before_test': not args.no_flush,
        'log_dir': args.log_dir,
        'results_dir': args.results_dir,
    }
    
    # Run benchmarks
    benchmark = RedisMemtierBenchmark(config)
    results = benchmark.run_all_benchmarks()
    
    # Save results
    results_file = benchmark.save_results()
    
    # Generate summary
    summary = generate_summary(results)
    
    # Print text report
    print_text_report(results, summary)
    
    # Generate visualizations
    if not args.no_visualize:
        try:
            from visualize import generate_visualizations
            generate_visualizations(results, summary, config)
        except ImportError:
            logging.warning("Visualization module not available. Install matplotlib and seaborn to enable visualizations.")
        except Exception as e:
            logging.error(f"Failed to generate visualizations: {str(e)}")
    
    print(f"\nResults saved to: {results_file}")
    print("Benchmark completed successfully!")


if __name__ == '__main__':
    main()

