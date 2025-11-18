#!/usr/bin/env python3
"""
Setup verification script for Redis Benchmark Tool

This script checks if all prerequisites are installed and configured correctly.
"""

import sys
import subprocess
import importlib.util
from pathlib import Path


class Colors:
    """ANSI color codes"""
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


def print_header(text):
    """Print a formatted header"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.NC}")
    print(f"{Colors.BLUE}{text}{Colors.NC}")
    print(f"{Colors.BLUE}{'='*60}{Colors.NC}\n")


def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.NC}")


def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.NC}")


def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.NC}")


def check_command(command, name):
    """Check if a command is available"""
    try:
        result = subprocess.run(
            [command, '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.split('\n')[0] if result.stdout else 'unknown'
            print_success(f"{name} is installed: {version}")
            return True
        else:
            print_error(f"{name} is not installed")
            return False
    except FileNotFoundError:
        print_error(f"{name} is not installed")
        return False
    except Exception as e:
        print_error(f"Error checking {name}: {str(e)}")
        return False


def check_redis_connection(host='localhost', port=6379):
    """Check if Redis is accessible"""
    try:
        result = subprocess.run(
            ['redis-cli', '-h', host, '-p', str(port), 'PING'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and 'PONG' in result.stdout:
            print_success(f"Redis is running on {host}:{port}")
            return True
        else:
            print_error(f"Redis is not responding on {host}:{port}")
            return False
    except FileNotFoundError:
        print_error("redis-cli is not installed")
        return False
    except Exception as e:
        print_error(f"Error connecting to Redis: {str(e)}")
        return False


def check_python_package(package_name):
    """Check if a Python package is installed"""
    spec = importlib.util.find_spec(package_name)
    if spec is not None:
        try:
            module = importlib.import_module(package_name)
            version = getattr(module, '__version__', 'unknown')
            print_success(f"{package_name} is installed: {version}")
            return True
        except Exception as e:
            print_warning(f"{package_name} is installed but couldn't get version: {str(e)}")
            return True
    else:
        print_error(f"{package_name} is not installed")
        return False


def check_file_exists(filepath, description):
    """Check if a file exists"""
    path = Path(filepath)
    if path.exists():
        print_success(f"{description} exists: {filepath}")
        return True
    else:
        print_error(f"{description} not found: {filepath}")
        return False


def main():
    """Main verification function"""
    print_header("Redis Benchmark Tool - Setup Verification")
    
    all_checks_passed = True
    
    # Check Python version
    print("Checking Python version...")
    python_version = sys.version.split()[0]
    major, minor = map(int, python_version.split('.')[:2])
    if major >= 3 and minor >= 8:
        print_success(f"Python version is compatible: {python_version}")
    else:
        print_error(f"Python version is too old: {python_version} (need 3.8+)")
        all_checks_passed = False
    
    print("\nChecking system commands...")
    
    # Check Redis
    if not check_command('redis-server', 'Redis server'):
        all_checks_passed = False
        print_warning("  Install: brew install redis (macOS) or apt-get install redis-server (Linux)")
    
    if not check_command('redis-cli', 'Redis CLI'):
        all_checks_passed = False
    
    # Check memtier_benchmark
    if not check_command('memtier_benchmark', 'memtier_benchmark'):
        all_checks_passed = False
        print_warning("  Install: brew install memtier-benchmark (macOS) or apt-get install memtier-benchmark (Linux)")
    
    print("\nChecking Redis connection...")
    if not check_redis_connection():
        print_warning("  Start Redis: redis-server &")
        all_checks_passed = False
    
    print("\nChecking Python packages...")
    
    required_packages = ['matplotlib', 'seaborn', 'pandas']
    for package in required_packages:
        if not check_python_package(package):
            all_checks_passed = False
    
    if not all(check_python_package(pkg) for pkg in required_packages):
        print_warning("  Install packages: pip install -r requirements.txt")
    
    print("\nChecking project files...")
    
    required_files = [
        ('redis_benchmark.py', 'Main benchmark script'),
        ('visualize.py', 'Visualization module'),
        ('requirements.txt', 'Requirements file'),
        ('README.md', 'Documentation'),
    ]
    
    for filepath, description in required_files:
        if not check_file_exists(filepath, description):
            all_checks_passed = False
    
    # Check if directories can be created
    print("\nChecking directory permissions...")
    try:
        Path('logs').mkdir(exist_ok=True)
        Path('results').mkdir(exist_ok=True)
        print_success("Can create logs/ and results/ directories")
    except Exception as e:
        print_error(f"Cannot create directories: {str(e)}")
        all_checks_passed = False
    
    # Final summary
    print_header("Verification Summary")
    
    if all_checks_passed:
        print_success("All checks passed! You're ready to run benchmarks.")
        print("\nQuick start:")
        print("  ./run_example.sh")
        print("\nOr manually:")
        print("  python redis_benchmark.py --data-sizes 64 256 --ratios 1:1")
        return 0
    else:
        print_error("Some checks failed. Please install missing components.")
        print("\nInstallation guide:")
        print("  1. Install Redis: brew install redis")
        print("  2. Install memtier: brew install memtier-benchmark")
        print("  3. Install Python packages: pip install -r requirements.txt")
        print("  4. Start Redis: redis-server &")
        print("\nSee README.md for detailed instructions.")
        return 1


if __name__ == '__main__':
    sys.exit(main())

