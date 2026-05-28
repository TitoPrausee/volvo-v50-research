#!/usr/bin/env python3
"""Test drive profile with realistic throttle data."""
import sys
sys.path.insert(0, '/opt/data/home/vehicle-database/projects/v50-stealth-rebuild/canbus')

from v50_drive_profile import DriveProfileAnalyzer, DriveProfile
from v50_can_decoder import V50State

analyzer = DriveProfileAnalyzer()

# Eco drive test: low throttle, low RPM, steady speed
print("=== ECO DRIVE TEST ===")
for i in range(30):
    state = V50State()
    state.rpm = 1800 + i * 5
    state.throttle_pct = 15.0
    state.speed_kmh = 80.0
    state.engine_load_pct = 30.0
    state.maf_g_per_s = 10.0
    analyzer.update(state)

analyzer._calculate_metrics()
profile = analyzer.metrics.profile
score = analyzer.metrics.profile_score
print(f"  Profile: {profile.name}, Score: {score:.1f}")
print(f"  Metrics: throttle_avg={analyzer.metrics.avg_throttle:.1f}%, "
      f"rpm_avg={analyzer.metrics.avg_rpm:.0f}")

# Sport drive test: high throttle, high RPM
print("\n=== SPORT DRIVE TEST ===")
analyzer2 = DriveProfileAnalyzer()
for i in range(30):
    state = V50State()
    state.rpm = 4500 + i * 30
    state.throttle_pct = 75.0
    state.speed_kmh = 160.0 - i * 0.5
    state.engine_load_pct = 85.0
    state.maf_g_per_s = 120.0
    analyzer2.update(state)

analyzer2._calculate_metrics()
profile2 = analyzer2.metrics.profile
score2 = analyzer2.metrics.profile_score
print(f"  Profile: {profile2.name}, Score: {score2:.1f}")
print(f"  Metrics: throttle_avg={analyzer2.metrics.avg_throttle:.1f}%, "
      f"rpm_avg={analyzer2.metrics.avg_rpm:.0f}")

# Normal drive test
print("\n=== NORMAL DRIVE TEST ===")
analyzer3 = DriveProfileAnalyzer()
for i in range(30):
    state = V50State()
    state.rpm = 2500
    state.throttle_pct = 35.0
    state.speed_kmh = 100.0
    state.engine_load_pct = 50.0
    state.maf_g_per_s = 40.0
    analyzer3.update(state)

analyzer3._calculate_metrics()
profile3 = analyzer3.metrics.profile
score3 = analyzer3.metrics.profile_score
print(f"  Profile: {profile3.name}, Score: {score3:.1f}")
print(f"  Metrics: throttle_avg={analyzer3.metrics.avg_throttle:.1f}%, "
      f"rpm_avg={analyzer3.metrics.avg_rpm:.0f}")