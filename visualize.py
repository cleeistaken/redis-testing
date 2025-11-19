#!/usr/bin/env python3
"""
Visualization module for Redis benchmark results

Generates various graphs and charts to visualize benchmark performance.
"""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import seaborn as sns
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import logging


def setup_plot_style():
    """Configure matplotlib and seaborn styling"""
    sns.set_theme(style="whitegrid")
    sns.set_palette("husl")
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 10


def prepare_dataframe(results: List[Dict[str, Any]]) -> pd.DataFrame:
    """Convert results to pandas DataFrame for easier plotting"""
    data = []
    
    for result in results:
        if not result.get('success'):
            continue
        
        metrics = result.get('benchmark_metrics', {})
        
        row = {
            'data_size': result['data_size'],
            'ratio': result['ratio'],
            'ops_per_sec': metrics.get('ops_per_sec', 0),
            'latency_avg': metrics.get('latency_avg', 0),
            'get_ops_per_sec': metrics.get('get_ops_per_sec', 0),
            'set_ops_per_sec': metrics.get('set_ops_per_sec', 0),
            'get_latency_avg': metrics.get('get_latency_avg', 0),
            'set_latency_avg': metrics.get('set_latency_avg', 0),
            'bandwidth_kb_sec': metrics.get('bandwidth_kb_sec', 0),
            'hits_per_sec': metrics.get('hits_per_sec', 0),
            'misses_per_sec': metrics.get('misses_per_sec', 0),
        }
        data.append(row)
    
    return pd.DataFrame(data)


def plot_throughput_by_data_size(df: pd.DataFrame, output_dir: Path):
    """Plot throughput vs data size for different ratios"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    for ratio in df['ratio'].unique():
        ratio_data = df[df['ratio'] == ratio].sort_values('data_size')
        ax.plot(ratio_data['data_size'], ratio_data['ops_per_sec'], 
                marker='o', linewidth=2, markersize=8, label=f'Ratio {ratio}')
    
    ax.set_xlabel('Data Size (bytes)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Operations per Second', fontsize=12, fontweight='bold')
    ax.set_title('Throughput vs Data Size by Ratio', fontsize=14, fontweight='bold')
    ax.legend(title='SET:GET Ratio', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xscale('log')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'throughput_by_data_size.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    logging.info(f"Generated: throughput_by_data_size.png")


def plot_latency_by_data_size(df: pd.DataFrame, output_dir: Path):
    """Plot latency vs data size for different ratios"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    for ratio in df['ratio'].unique():
        ratio_data = df[df['ratio'] == ratio].sort_values('data_size')
        ax.plot(ratio_data['data_size'], ratio_data['latency_avg'], 
                marker='s', linewidth=2, markersize=8, label=f'Ratio {ratio}')
    
    ax.set_xlabel('Data Size (bytes)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Average Latency (ms)', fontsize=12, fontweight='bold')
    ax.set_title('Latency vs Data Size by Ratio', fontsize=14, fontweight='bold')
    ax.legend(title='SET:GET Ratio', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xscale('log')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'latency_by_data_size.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    logging.info(f"Generated: latency_by_data_size.png")


def plot_throughput_by_ratio(df: pd.DataFrame, output_dir: Path):
    """Plot throughput comparison across ratios for different data sizes"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    data_sizes = sorted(df['data_size'].unique())
    x = range(len(df['ratio'].unique()))
    width = 0.8 / len(data_sizes)
    
    for i, data_size in enumerate(data_sizes):
        size_data = df[df['data_size'] == data_size]
        ratios = size_data['ratio'].tolist()
        ops = size_data['ops_per_sec'].tolist()
        
        positions = [pos + i * width for pos in x]
        ax.bar(positions, ops, width, label=f'{data_size} bytes', alpha=0.8)
    
    ax.set_xlabel('SET:GET Ratio', fontsize=12, fontweight='bold')
    ax.set_ylabel('Operations per Second', fontsize=12, fontweight='bold')
    ax.set_title('Throughput Comparison by Ratio', fontsize=14, fontweight='bold')
    ax.set_xticks([pos + width * len(data_sizes) / 2 for pos in x])
    ax.set_xticklabels(df['ratio'].unique())
    ax.legend(title='Data Size', fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'throughput_by_ratio.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    logging.info(f"Generated: throughput_by_ratio.png")


def plot_heatmap_throughput(df: pd.DataFrame, output_dir: Path):
    """Create a heatmap of throughput across data sizes and ratios"""
    pivot_table = df.pivot(index='ratio', columns='data_size', values='ops_per_sec')
    
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(pivot_table, annot=True, fmt='.0f', cmap='YlOrRd', 
                cbar_kws={'label': 'Operations per Second'}, ax=ax)
    
    ax.set_xlabel('Data Size (bytes)', fontsize=12, fontweight='bold')
    ax.set_ylabel('SET:GET Ratio', fontsize=12, fontweight='bold')
    ax.set_title('Throughput Heatmap', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'throughput_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    logging.info(f"Generated: throughput_heatmap.png")


def plot_heatmap_latency(df: pd.DataFrame, output_dir: Path):
    """Create a heatmap of latency across data sizes and ratios"""
    pivot_table = df.pivot(index='ratio', columns='data_size', values='latency_avg')
    
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(pivot_table, annot=True, fmt='.2f', cmap='YlGnBu', 
                cbar_kws={'label': 'Average Latency (ms)'}, ax=ax)
    
    ax.set_xlabel('Data Size (bytes)', fontsize=12, fontweight='bold')
    ax.set_ylabel('SET:GET Ratio', fontsize=12, fontweight='bold')
    ax.set_title('Latency Heatmap', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'latency_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    logging.info(f"Generated: latency_heatmap.png")


def plot_get_set_comparison(df: pd.DataFrame, output_dir: Path):
    """Plot GET vs SET performance comparison"""
    # Filter data that has both GET and SET metrics
    df_filtered = df[(df['get_ops_per_sec'] > 0) & (df['set_ops_per_sec'] > 0)]
    
    if df_filtered.empty:
        logging.warning("No GET/SET comparison data available")
        return
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Throughput comparison
    x = range(len(df_filtered))
    width = 0.35
    
    ax1.bar([i - width/2 for i in x], df_filtered['get_ops_per_sec'], 
            width, label='GET', alpha=0.8, color='skyblue')
    ax1.bar([i + width/2 for i in x], df_filtered['set_ops_per_sec'], 
            width, label='SET', alpha=0.8, color='salmon')
    
    labels = [f"{row['data_size']}B\n{row['ratio']}" 
              for _, row in df_filtered.iterrows()]
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=45, ha='right')
    ax1.set_xlabel('Data Size / Ratio', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Operations per Second', fontsize=12, fontweight='bold')
    ax1.set_title('GET vs SET Throughput', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Latency comparison
    ax2.bar([i - width/2 for i in x], df_filtered['get_latency_avg'], 
            width, label='GET', alpha=0.8, color='skyblue')
    ax2.bar([i + width/2 for i in x], df_filtered['set_latency_avg'], 
            width, label='SET', alpha=0.8, color='salmon')
    
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, rotation=45, ha='right')
    ax2.set_xlabel('Data Size / Ratio', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Average Latency (ms)', fontsize=12, fontweight='bold')
    ax2.set_title('GET vs SET Latency', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'get_set_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    logging.info(f"Generated: get_set_comparison.png")


def plot_bandwidth_analysis(df: pd.DataFrame, output_dir: Path):
    """Plot bandwidth utilization"""
    if df['bandwidth_kb_sec'].sum() == 0:
        logging.warning("No bandwidth data available")
        return
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    for ratio in df['ratio'].unique():
        ratio_data = df[df['ratio'] == ratio].sort_values('data_size')
        ax.plot(ratio_data['data_size'], ratio_data['bandwidth_kb_sec'], 
                marker='D', linewidth=2, markersize=8, label=f'Ratio {ratio}')
    
    ax.set_xlabel('Data Size (bytes)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Bandwidth (KB/sec)', fontsize=12, fontweight='bold')
    ax.set_title('Bandwidth Utilization by Data Size', fontsize=14, fontweight='bold')
    ax.legend(title='SET:GET Ratio', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xscale('log')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'bandwidth_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    logging.info(f"Generated: bandwidth_analysis.png")


def plot_summary_dashboard(df: pd.DataFrame, summary: Dict[str, Any], output_dir: Path):
    """Create a comprehensive summary dashboard"""
    fig = plt.figure(figsize=(20, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # 1. Overall throughput by data size
    ax1 = fig.add_subplot(gs[0, :2])
    for ratio in df['ratio'].unique():
        ratio_data = df[df['ratio'] == ratio].sort_values('data_size')
        ax1.plot(ratio_data['data_size'], ratio_data['ops_per_sec'], 
                marker='o', linewidth=2, label=f'{ratio}')
    ax1.set_xlabel('Data Size (bytes)')
    ax1.set_ylabel('Ops/sec')
    ax1.set_title('Throughput by Data Size', fontweight='bold')
    ax1.legend(title='Ratio', ncol=2)
    ax1.grid(True, alpha=0.3)
    ax1.set_xscale('log')
    
    # 2. Summary statistics box
    ax2 = fig.add_subplot(gs[0, 2])
    ax2.axis('off')
    summary_text = f"""
    BENCHMARK SUMMARY
    
    Total Tests: {summary['total_tests']}
    Successful: {summary['successful_tests']}
    Failed: {summary['failed_tests']}
    
    Data Sizes: {len(summary['by_data_size'])}
    Ratios: {len(summary['by_ratio'])}
    
    Max Throughput:
    {df['ops_per_sec'].max():.0f} ops/sec
    
    Min Latency:
    {df['latency_avg'].min():.2f} ms
    """
    ax2.text(0.1, 0.5, summary_text, fontsize=10, family='monospace',
             verticalalignment='center')
    
    # 3. Latency by data size
    ax3 = fig.add_subplot(gs[1, :2])
    for ratio in df['ratio'].unique():
        ratio_data = df[df['ratio'] == ratio].sort_values('data_size')
        ax3.plot(ratio_data['data_size'], ratio_data['latency_avg'], 
                marker='s', linewidth=2, label=f'{ratio}')
    ax3.set_xlabel('Data Size (bytes)')
    ax3.set_ylabel('Latency (ms)')
    ax3.set_title('Latency by Data Size', fontweight='bold')
    ax3.legend(title='Ratio', ncol=2)
    ax3.grid(True, alpha=0.3)
    ax3.set_xscale('log')
    
    # 4. Throughput distribution
    ax4 = fig.add_subplot(gs[1, 2])
    ax4.hist(df['ops_per_sec'], bins=15, color='skyblue', edgecolor='black', alpha=0.7)
    ax4.set_xlabel('Ops/sec')
    ax4.set_ylabel('Frequency')
    ax4.set_title('Throughput Distribution', fontweight='bold')
    ax4.grid(True, alpha=0.3, axis='y')
    
    # 5. Performance by ratio (box plot)
    ax5 = fig.add_subplot(gs[2, :2])
    df_sorted = df.sort_values('ratio')
    sns.boxplot(data=df_sorted, x='ratio', y='ops_per_sec', ax=ax5, palette='Set2')
    ax5.set_xlabel('SET:GET Ratio')
    ax5.set_ylabel('Ops/sec')
    ax5.set_title('Throughput Distribution by Ratio', fontweight='bold')
    ax5.grid(True, alpha=0.3, axis='y')
    
    # 6. Latency distribution
    ax6 = fig.add_subplot(gs[2, 2])
    ax6.hist(df['latency_avg'], bins=15, color='salmon', edgecolor='black', alpha=0.7)
    ax6.set_xlabel('Latency (ms)')
    ax6.set_ylabel('Frequency')
    ax6.set_title('Latency Distribution', fontweight='bold')
    ax6.grid(True, alpha=0.3, axis='y')
    
    # Add overall title
    fig.suptitle('Redis Benchmark Dashboard', fontsize=16, fontweight='bold', y=0.995)
    
    plt.savefig(output_dir / 'summary_dashboard.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    logging.info(f"Generated: summary_dashboard.png")


def generate_visualizations(results: List[Dict[str, Any]], summary: Dict[str, Any], 
                           config: Dict[str, Any]):
    """Generate all visualization graphs"""
    logging.info("Generating visualizations...")
    
    # Setup
    setup_plot_style()
    
    # Use graphs_dir from config if provided, otherwise use default
    if 'graphs_dir' in config:
        output_dir = Path(config['graphs_dir'])
    else:
        output_dir = Path(config.get('results_dir', 'results')) / 'graphs'
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Prepare data
    df = prepare_dataframe(results)
    
    if df.empty:
        logging.warning("No successful results to visualize")
        return
    
    # Generate all plots
    try:
        plot_throughput_by_data_size(df, output_dir)
        plot_latency_by_data_size(df, output_dir)
        plot_throughput_by_ratio(df, output_dir)
        plot_heatmap_throughput(df, output_dir)
        plot_heatmap_latency(df, output_dir)
        plot_get_set_comparison(df, output_dir)
        plot_bandwidth_analysis(df, output_dir)
        plot_summary_dashboard(df, summary, output_dir)
        
        logging.info(f"All visualizations saved to {output_dir}")
        print(f"\nVisualizations saved to: {output_dir}")
        
    except Exception as e:
        logging.error(f"Error generating visualizations: {str(e)}")
        raise


if __name__ == '__main__':
    # This module is meant to be imported, not run directly
    print("This module provides visualization functions for redis_benchmark.py")
    print("Run redis_benchmark.py to generate benchmarks and visualizations.")

