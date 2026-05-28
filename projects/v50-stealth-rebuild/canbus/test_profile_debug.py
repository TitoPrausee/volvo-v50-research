#!/usr/bin/env python3
"""Debug drive profile scoring for sport pattern."""
import sys
import math
sys.path.insert(0, '/opt/data/home/vehicle-database/projects/v50-stealth-rebuild/canbus')

from v50_drive_profile import DriveProfileAnalyzer, DriveProfile
from v50_can_decoder import V50State

analyzer = DriveProfileAnalyzer()
for i in range(30):
    state = V50State()
    state.rpm = 4500 + i * 30
    state.throttle_pct = 75.0
    state.speed_kmh = 160.0 - i * 0.5
    state.engine_load_pct = 85.0
    state.maf_g_per_s = 120.0
    analyzer.update(state)

analyzer._calculate_metrics()

# Reproduce scoring logic
scores = {}
scores['avg_throttle'] = min(100, analyzer.metrics.avg_throttle * 1.5)
scores['throttle_variance'] = min(100, analyzer.metrics.throttle_variance * 3.0)
scores['throttle_change'] = min(100, analyzer.metrics.throttle_change_rate * 5.0)
rpm_score = max(0, (analyzer.metrics.avg_rpm - 800) / 40)
scores['avg_rpm'] = min(100, rpm_score)
scores['rpm_variance'] = min(100, math.sqrt(analyzer.metrics.rpm_variance) * 0.15)
scores['avg_load'] = min(100, analyzer.metrics.avg_load * 1.2)
scores['consumption'] = min(100, max(0, (analyzer.metrics.est_consumption_lh - 0.5) * 12))
scores['brake_events'] = min(100, analyzer.metrics.brake_events * 15)

print("Individual scores:")
for k, v in scores.items():
    w = analyzer.WEIGHTS.get(k, 0)
    weighted = v * w
    print(f"  {k:25s}: raw={v:6.1f}  weight={w:.2f}  weighted={weighted:5.2f}")

total = sum(scores.get(k, 0) * w for k, w in analyzer.WEIGHTS.items() if k != 'brake_events')
total += scores.get('brake_events', 0) * analyzer.WEIGHTS.get('brake_events', 0)
print(f"\nTotal weighted score: {total:.1f}")
print(f"Profile: {analyzer.metrics.profile.name}")
print(f"Profile score: {analyzer.metrics.profile_score:.1f}")

# Metrics debug
print(f"\nMetrics detail:")
print(f"  avg_throttle: {analyzer.metrics.avg_throttle:.1f}")
print(f"  throttle_variance: {analyzer.metrics.throttle_variance:.1f}")
print(f"  throttle_change_rate: {analyzer.metrics.throttle_change_rate:.1f}")
print(f"  avg_rpm: {analyzer.metrics.avg_rpm:.0f}")
print(f"  rpm_variance: {analyzer.metrics.rpm_variance:.0f}")
print(f"  avg_load: {analyzer.metrics.avg_load:.1f}")
print(f"  est_consumption_lh: {analyzer.metrics.est_consumption_lh:.1f}")
print(f"  brake_events: {analyzer.metrics.brake_events}")