"""
Generate professional visualizations for the Smart Refrigerator Monitoring System.
Creates 7 high-resolution charts suitable for the internship report.
"""

import json
import csv
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import numpy as np
from collections import Counter, defaultdict


def load_data():
    """Load simulation data from files."""
    fridge_readings = []
    food_readings = []
    inventory_readings = []
    alerts = []
    
    try:
        with open("refrigerator_readings.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                fridge_readings.append(row)
        
        with open("food_freshness_readings.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                food_readings.append(row)
        
        with open("inventory_readings.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                inventory_readings.append(row)
        
        with open("system_alerts.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                alerts.append(row)
        
        with open("refrigerator_analytics.json", "r") as f:
            analytics = json.load(f)
    except FileNotFoundError:
        print("Error: Data files not found. Please run smart_refrigerator_monitoring.py first.")
        return None, None, None, None, None
    
    return fridge_readings, food_readings, inventory_readings, alerts, analytics


def create_temperature_humidity_chart(fridge_readings):
    """Chart 1: Temperature and Humidity Monitoring."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Chart 1: Refrigerator Temperature and Humidity Monitoring', fontsize=16, fontweight='bold')
    
    # Sample readings for clarity
    sample_readings = fridge_readings[::100]
    indices = range(len(sample_readings))
    temperatures = [float(r['temperature']) for r in sample_readings]
    humidities = [float(r['humidity']) for r in sample_readings]
    
    # Temperature chart
    ax1.plot(indices, temperatures, marker='o', linestyle='-', linewidth=2, markersize=6, color='#e74c3c')
    ax1.axhline(y=3, color='green', linestyle='--', linewidth=2, label='Optimal (3°C)')
    ax1.fill_between(indices, 2, 4, alpha=0.2, color='green', label='Safe Range (2-4°C)')
    ax1.set_title('Temperature Trend', fontweight='bold', pad=20)
    ax1.set_ylabel('Temperature (°C)', fontweight='bold')
    ax1.set_xlabel('Reading Index', fontweight='bold')
    ax1.legend(loc='best')
    ax1.grid(True, alpha=0.3)
    
    # Humidity chart
    ax2.plot(indices, humidities, marker='s', linestyle='-', linewidth=2, markersize=6, color='#3498db')
    ax2.axhline(y=65, color='green', linestyle='--', linewidth=2, label='Optimal (65%)')
    ax2.fill_between(indices, 60, 70, alpha=0.2, color='green', label='Safe Range (60-70%)')
    ax2.set_title('Humidity Trend', fontweight='bold', pad=20)
    ax2.set_ylabel('Humidity (%)', fontweight='bold')
    ax2.set_xlabel('Reading Index', fontweight='bold')
    ax2.legend(loc='best')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('chart_01_temperature_humidity.png', dpi=300, bbox_inches='tight')
    print("✓ Chart 1: Temperature and Humidity - Created")
    plt.close()


def create_food_freshness_chart(food_readings):
    """Chart 2: Food Freshness Status Distribution."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Chart 2: Food Freshness Status and Quality Distribution', fontsize=16, fontweight='bold')
    
    # Freshness level distribution
    freshness_counts = Counter(r['freshness_level'] for r in food_readings)
    colors_freshness = {'Fresh': '#2ecc71', 'Good': '#f39c12', 'Expiring Soon': '#e67e22', 'Expired': '#e74c3c'}
    freshness_colors = [colors_freshness.get(level, '#95a5a6') for level in freshness_counts.keys()]
    ax1.pie(freshness_counts.values(), labels=freshness_counts.keys(), autopct='%1.1f%%',
            colors=freshness_colors, startangle=90)
    ax1.set_title('Food Freshness Distribution', fontweight='bold', pad=20)
    
    # Quality score distribution
    sample_readings = food_readings[::100]
    quality_scores = [float(r['quality_score']) for r in sample_readings]
    indices = range(len(sample_readings))
    ax2.plot(indices, quality_scores, marker='D', linestyle='-', linewidth=2, markersize=6, color='#9b59b6')
    ax2.axhline(y=80, color='green', linestyle='--', linewidth=2, label='Good Quality (80%)')
    ax2.fill_between(indices, 0, quality_scores, alpha=0.3, color='#9b59b6')
    ax2.set_title('Quality Score Trend', fontweight='bold', pad=20)
    ax2.set_ylabel('Quality Score', fontweight='bold')
    ax2.set_xlabel('Reading Index', fontweight='bold')
    ax2.set_ylim(0, 105)
    ax2.legend(loc='best')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('chart_02_food_freshness.png', dpi=300, bbox_inches='tight')
    print("✓ Chart 2: Food Freshness - Created")
    plt.close()


def create_inventory_status_chart(inventory_readings):
    """Chart 3: Inventory Level Status Distribution."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Chart 3: Inventory Level Status and Quantity Distribution', fontsize=16, fontweight='bold')
    
    # Inventory level distribution
    level_counts = Counter(r['inventory_level'] for r in inventory_readings)
    colors_inv = {'Adequate': '#2ecc71', 'Low': '#f39c12', 'Critical': '#e74c3c', 'Overstocked': '#3498db'}
    inv_colors = [colors_inv.get(level, '#95a5a6') for level in level_counts.keys()]
    ax1.bar(level_counts.keys(), level_counts.values(), color=inv_colors, edgecolor='black', linewidth=1.5)
    ax1.set_title('Inventory Level Distribution', fontweight='bold', pad=20)
    ax1.set_ylabel('Number of Readings', fontweight='bold')
    ax1.set_xlabel('Inventory Level', fontweight='bold')
    ax1.tick_params(axis='x', rotation=45)
    
    # Quantity distribution
    sample_readings = inventory_readings[::100]
    quantities = [int(r['quantity']) for r in sample_readings]
    indices = range(len(sample_readings))
    ax2.plot(indices, quantities, marker='o', linestyle='-', linewidth=2, markersize=6, color='#16a085')
    ax2.fill_between(indices, 0, quantities, alpha=0.3, color='#16a085')
    ax2.set_title('Inventory Quantity Trend', fontweight='bold', pad=20)
    ax2.set_ylabel('Quantity (Units)', fontweight='bold')
    ax2.set_xlabel('Reading Index', fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('chart_03_inventory_status.png', dpi=300, bbox_inches='tight')
    print("✓ Chart 3: Inventory Status - Created")
    plt.close()


def create_alert_analysis_chart(alerts):
    """Chart 4: Alert Analysis and Distribution."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Chart 4: System Alert Analysis', fontsize=16, fontweight='bold')
    
    # Alert type distribution
    alert_type_counts = Counter(a['alert_type'] for a in alerts)
    ax1.barh(list(alert_type_counts.keys()), list(alert_type_counts.values()), 
             color='#e74c3c', edgecolor='black', linewidth=1.5)
    ax1.set_title('Alert Type Distribution', fontweight='bold', pad=20)
    ax1.set_xlabel('Number of Alerts', fontweight='bold')
    
    # Severity distribution
    severity_counts = Counter(a['severity'] for a in alerts)
    colors_severity = {'CRITICAL': '#e74c3c', 'WARNING': '#f39c12', 'INFO': '#3498db'}
    severity_colors = [colors_severity.get(sev, '#95a5a6') for sev in severity_counts.keys()]
    ax2.pie(severity_counts.values(), labels=severity_counts.keys(), autopct='%1.1f%%',
            colors=severity_colors, startangle=90)
    ax2.set_title('Alert Severity Distribution', fontweight='bold', pad=20)
    
    # Alerts over time (sample every 50 alerts)
    sample_alerts = alerts[::50]
    alert_indices = range(len(sample_alerts))
    ax3.plot(alert_indices, range(len(sample_alerts)), marker='o', linestyle='-', 
             linewidth=2, markersize=6, color='#e74c3c')
    ax3.fill_between(alert_indices, 0, range(len(sample_alerts)), alpha=0.3, color='#e74c3c')
    ax3.set_title('Alert Accumulation Over Time', fontweight='bold', pad=20)
    ax3.set_ylabel('Cumulative Alerts', fontweight='bold')
    ax3.set_xlabel('Alert Index (sampled)', fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    # Alert count by type (top 10)
    alert_type_counts_sorted = dict(sorted(alert_type_counts.items(), key=lambda x: x[1], reverse=True)[:10])
    ax4.barh(list(alert_type_counts_sorted.keys()), list(alert_type_counts_sorted.values()), 
             color='#f39c12', edgecolor='black', linewidth=1.5)
    ax4.set_title('Top 10 Alert Types by Frequency', fontweight='bold', pad=20)
    ax4.set_xlabel('Number of Alerts', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('chart_04_alert_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Chart 4: Alert Analysis - Created")
    plt.close()


def create_door_power_status_chart(fridge_readings):
    """Chart 5: Door and Power Status Monitoring."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Chart 5: Door Opening and Power Status Monitoring', fontsize=16, fontweight='bold')
    
    # Door opening frequency
    door_opens = sum(1 for r in fridge_readings if r['door_open'] == 'True')
    door_closed = len(fridge_readings) - door_opens
    door_data = [door_closed, door_opens]
    colors_door = ['#2ecc71', '#e74c3c']
    ax1.pie(door_data, labels=['Door Closed', 'Door Open'], autopct='%1.1f%%',
            colors=colors_door, startangle=90)
    ax1.set_title('Door Status Distribution', fontweight='bold', pad=20)
    
    # Power status distribution
    power_status_counts = Counter(r['power_status'] for r in fridge_readings)
    colors_power = {'Normal': '#2ecc71', 'Abnormal': '#e74c3c'}
    power_colors = [colors_power.get(status, '#95a5a6') for status in power_status_counts.keys()]
    ax2.bar(power_status_counts.keys(), power_status_counts.values(), 
            color=power_colors, edgecolor='black', linewidth=1.5)
    ax2.set_title('Power Status Distribution', fontweight='bold', pad=20)
    ax2.set_ylabel('Number of Readings', fontweight='bold')
    ax2.set_xlabel('Power Status', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('chart_05_door_power_status.png', dpi=300, bbox_inches='tight')
    print("✓ Chart 5: Door and Power Status - Created")
    plt.close()


def create_system_performance_chart(analytics):
    """Chart 6: System Performance Metrics Dashboard."""
    fig = plt.figure(figsize=(14, 8))
    gs = GridSpec(2, 2, figure=fig)
    fig.suptitle('Chart 6: Refrigerator System Performance Dashboard', fontsize=16, fontweight='bold')
    
    fridge_stats = analytics['refrigerator_statistics']
    freshness_stats = analytics['food_freshness_statistics']
    inventory_stats = analytics['inventory_statistics']
    alert_stats = analytics['alert_statistics']
    
    # Temperature and humidity metrics
    ax1 = fig.add_subplot(gs[0, 0])
    metrics = ['Avg Temp\n(°C)', 'Avg Humidity\n(%)', 'Door Opens', 'Power Issues']
    values = [
        fridge_stats['avg_temperature'],
        fridge_stats['avg_humidity'],
        fridge_stats['total_door_opens'],
        fridge_stats['power_issues']
    ]
    colors_metrics = ['#e74c3c', '#3498db', '#f39c12', '#c0392b']
    bars = ax1.bar(metrics, values, color=colors_metrics, edgecolor='black', linewidth=1.5)
    ax1.set_title('Environmental Metrics', fontweight='bold', pad=20)
    ax1.set_ylabel('Value', fontweight='bold')
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1f}', ha='center', va='bottom', fontweight='bold')
    
    # Food quality metrics
    ax2 = fig.add_subplot(gs[0, 1])
    quality_metrics = ['Avg Quality\nScore', 'Min Quality\nScore', 'Max Quality\nScore']
    quality_values = [
        freshness_stats['avg_quality_score'],
        freshness_stats['min_quality_score'],
        freshness_stats['max_quality_score']
    ]
    colors_quality = ['#2ecc71', '#f39c12', '#3498db']
    bars = ax2.bar(quality_metrics, quality_values, color=colors_quality, edgecolor='black', linewidth=1.5)
    ax2.set_title('Food Quality Metrics', fontweight='bold', pad=20)
    ax2.set_ylabel('Score', fontweight='bold')
    ax2.set_ylim(0, 105)
    for bar, val in zip(bars, quality_values):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1f}', ha='center', va='bottom', fontweight='bold')
    
    # Inventory distribution
    ax3 = fig.add_subplot(gs[1, 0])
    inv_dist = inventory_stats['inventory_level_distribution']
    inv_labels = list(inv_dist.keys())
    inv_values = list(inv_dist.values())
    colors_inv = {'Adequate': '#2ecc71', 'Low': '#f39c12', 'Critical': '#e74c3c', 'Overstocked': '#3498db'}
    inv_colors = [colors_inv.get(label, '#95a5a6') for label in inv_labels]
    ax3.pie(inv_values, labels=inv_labels, autopct='%1.1f%%',
            colors=inv_colors, startangle=90)
    ax3.set_title('Inventory Level Distribution', fontweight='bold', pad=20)
    
    # Alert summary
    ax4 = fig.add_subplot(gs[1, 1])
    alert_types = list(alert_stats['severity_distribution'].keys())
    alert_values = list(alert_stats['severity_distribution'].values())
    colors_alerts = {'CRITICAL': '#e74c3c', 'WARNING': '#f39c12', 'INFO': '#3498db'}
    alert_colors = [colors_alerts.get(alert_type, '#95a5a6') for alert_type in alert_types]
    bars = ax4.bar(alert_types, alert_values, color=alert_colors, edgecolor='black', linewidth=1.5)
    ax4.set_title('Alert Severity Summary', fontweight='bold', pad=20)
    ax4.set_ylabel('Count', fontweight='bold')
    for bar, val in zip(bars, alert_values):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(val)}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('chart_06_system_performance.png', dpi=300, bbox_inches='tight')
    print("✓ Chart 6: System Performance - Created")
    plt.close()


def create_comprehensive_dashboard(fridge_readings, food_readings, inventory_readings, alerts, analytics):
    """Chart 7: Comprehensive System Dashboard."""
    fig = plt.figure(figsize=(16, 12))
    gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.3)
    fig.suptitle('Chart 7: Comprehensive Smart Refrigerator Monitoring Dashboard', 
                 fontsize=18, fontweight='bold', y=0.995)
    
    # 1. Temperature distribution
    ax1 = fig.add_subplot(gs[0, 0])
    temperatures = [float(r['temperature']) for r in fridge_readings]
    ax1.hist(temperatures, bins=20, color='#e74c3c', edgecolor='black', alpha=0.7)
    ax1.axvline(np.mean(temperatures), color='green', linestyle='--', linewidth=2, label='Mean')
    ax1.set_title('Temperature Distribution', fontweight='bold', fontsize=10)
    ax1.set_xlabel('Temp (°C)', fontsize=8)
    ax1.set_ylabel('Frequency', fontsize=8)
    ax1.legend(fontsize=7)
    
    # 2. Humidity distribution
    ax2 = fig.add_subplot(gs[0, 1])
    humidities = [float(r['humidity']) for r in fridge_readings]
    ax2.hist(humidities, bins=20, color='#3498db', edgecolor='black', alpha=0.7)
    ax2.axvline(np.mean(humidities), color='green', linestyle='--', linewidth=2, label='Mean')
    ax2.set_title('Humidity Distribution', fontweight='bold', fontsize=10)
    ax2.set_xlabel('Humidity (%)', fontsize=8)
    ax2.set_ylabel('Frequency', fontsize=8)
    ax2.legend(fontsize=7)
    
    # 3. Freshness distribution
    ax3 = fig.add_subplot(gs[0, 2])
    freshness_counts = Counter(r['freshness_level'] for r in food_readings)
    colors_fresh = {'Fresh': '#2ecc71', 'Good': '#f39c12', 'Expiring Soon': '#e67e22', 'Expired': '#e74c3c'}
    fresh_colors = [colors_fresh.get(level, '#95a5a6') for level in freshness_counts.keys()]
    ax3.pie(freshness_counts.values(), labels=freshness_counts.keys(), autopct='%1.0f%%',
            colors=fresh_colors, textprops={'fontsize': 8})
    ax3.set_title('Freshness Status', fontweight='bold', fontsize=10)
    
    # 4. Inventory levels
    ax4 = fig.add_subplot(gs[1, 0])
    level_counts = Counter(r['inventory_level'] for r in inventory_readings)
    colors_inv = {'Adequate': '#2ecc71', 'Low': '#f39c12', 'Critical': '#e74c3c', 'Overstocked': '#3498db'}
    inv_colors = [colors_inv.get(level, '#95a5a6') for level in level_counts.keys()]
    ax4.bar(range(len(level_counts)), list(level_counts.values()), color=inv_colors, edgecolor='black', linewidth=1)
    ax4.set_xticks(range(len(level_counts)))
    ax4.set_xticklabels(list(level_counts.keys()), fontsize=8, rotation=45)
    ax4.set_title('Inventory Levels', fontweight='bold', fontsize=10)
    ax4.set_ylabel('Count', fontsize=8)
    
    # 5. Alert severity
    ax5 = fig.add_subplot(gs[1, 1])
    severity_counts = Counter(a['severity'] for a in alerts)
    colors_sev = {'CRITICAL': '#e74c3c', 'WARNING': '#f39c12', 'INFO': '#3498db'}
    sev_colors = [colors_sev.get(sev, '#95a5a6') for sev in severity_counts.keys()]
    ax5.pie(severity_counts.values(), labels=severity_counts.keys(), autopct='%1.0f%%',
            colors=sev_colors, textprops={'fontsize': 8})
    ax5.set_title('Alert Severity', fontweight='bold', fontsize=10)
    
    # 6. Door status
    ax6 = fig.add_subplot(gs[1, 2])
    door_opens = sum(1 for r in fridge_readings if r['door_open'] == 'True')
    door_closed = len(fridge_readings) - door_opens
    ax6.pie([door_closed, door_opens], labels=['Closed', 'Open'], autopct='%1.0f%%',
            colors=['#2ecc71', '#e74c3c'], textprops={'fontsize': 8})
    ax6.set_title('Door Status', fontweight='bold', fontsize=10)
    
    # 7. Temperature trend
    ax7 = fig.add_subplot(gs[2, 0])
    sample_temps = [float(r['temperature']) for r in fridge_readings[::100]]
    ax7.plot(range(len(sample_temps)), sample_temps, marker='o', linestyle='-', 
             linewidth=1.5, markersize=4, color='#e74c3c')
    ax7.axhline(y=3, color='green', linestyle='--', linewidth=1, alpha=0.7)
    ax7.set_title('Temperature Trend', fontweight='bold', fontsize=10)
    ax7.set_ylabel('Temp (°C)', fontsize=8)
    ax7.set_xlabel('Reading', fontsize=8)
    ax7.grid(True, alpha=0.3)
    
    # 8. Humidity trend
    ax8 = fig.add_subplot(gs[2, 1])
    sample_hums = [float(r['humidity']) for r in fridge_readings[::100]]
    ax8.plot(range(len(sample_hums)), sample_hums, marker='s', linestyle='-', 
             linewidth=1.5, markersize=4, color='#3498db')
    ax8.axhline(y=65, color='green', linestyle='--', linewidth=1, alpha=0.7)
    ax8.set_title('Humidity Trend', fontweight='bold', fontsize=10)
    ax8.set_ylabel('Humidity (%)', fontsize=8)
    ax8.set_xlabel('Reading', fontsize=8)
    ax8.grid(True, alpha=0.3)
    
    # 9. Alert types
    ax9 = fig.add_subplot(gs[2, 2])
    alert_type_counts = Counter(a['alert_type'] for a in alerts)
    top_alerts = dict(sorted(alert_type_counts.items(), key=lambda x: x[1], reverse=True)[:5])
    ax9.barh(list(top_alerts.keys()), list(top_alerts.values()), 
             color='#e74c3c', edgecolor='black', linewidth=1)
    ax9.set_title('Top Alert Types', fontweight='bold', fontsize=10)
    ax9.set_xlabel('Count', fontsize=8)
    
    plt.savefig('chart_07_comprehensive_dashboard.png', dpi=300, bbox_inches='tight')
    print("✓ Chart 7: Comprehensive Dashboard - Created")
    plt.close()


def main():
    """Main entry point."""
    print("\n" + "="*80)
    print("GENERATING PROFESSIONAL VISUALIZATIONS")
    print("Smart Refrigerator Monitoring System")
    print("="*80)
    
    fridge_readings, food_readings, inventory_readings, alerts, analytics = load_data()
    
    if fridge_readings is None:
        return
    
    create_temperature_humidity_chart(fridge_readings)
    create_food_freshness_chart(food_readings)
    create_inventory_status_chart(inventory_readings)
    create_alert_analysis_chart(alerts)
    create_door_power_status_chart(fridge_readings)
    create_system_performance_chart(analytics)
    create_comprehensive_dashboard(fridge_readings, food_readings, inventory_readings, alerts, analytics)
    
    print("\n" + "="*80)
    print("✓ ALL VISUALIZATIONS GENERATED SUCCESSFULLY")
    print("="*80)
    print("\nGenerated files:")
    print("  1. chart_01_temperature_humidity.png")
    print("  2. chart_02_food_freshness.png")
    print("  3. chart_03_inventory_status.png")
    print("  4. chart_04_alert_analysis.png")
    print("  5. chart_05_door_power_status.png")
    print("  6. chart_06_system_performance.png")
    print("  7. chart_07_comprehensive_dashboard.png")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
