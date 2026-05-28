#!/usr/bin/env python3
"""
Volvo V50 2.4i — Drive Profile Analyzer
========================================
Analyzes CAN bus data in real-time to classify driving style
as Eco, Normal, or Sport. Uses throttle position, RPM behavior,
acceleration patterns, and fuel consumption metrics.

The V50 B5244S doesn't have electronic drive mode selection like newer
Volvo models, but this analyzer inffers the driver's style from the data.

Useful for:
- Dashboard display of current driving style
- Fuel economy coaching
- Self-assessment of driving habits
- Long-term driving style analysis via logged data

Algorithm:
- RPM variance (high revs = sporty)
- Throttle change rate (aggressive throttle = sporty)
- Average throttle position
- Shift points (high RPM shifts = sporty)
- Fuel consumption rate
- Brake usage frequency (from speed decreases)

Author: v50-developer agent
Date: 2026-05-28
"""

import argparse
import json
import logging
import math
import time
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple

from v50_can_decoder import V50State, MESSAGE_DEFINITIONS

logger = logging.getLogger('v50.drive_profile')


# =============================================================================
# Drive Profile Classification
# =============================================================================

class DriveProfile(Enum):
    """V50 driving style classification."""
    ECO = "eco"
    NORMAL = "normal"
    SPORT = "sport"
    
    @property
    def display_name(self) -> str:
        return {
            "eco": "🌿 ECO",
            "normal": "🚗 NORMAL",
            "sport": "🏁 SPORT"
        }.get(self.value, self.value)
    
    @property
    def color(self) -> str:
        """Color for dashboard display."""
        return {
            "eco": "#00AA44",      # Green
            "normal": "#0066CC",   # Blue
            "sport": "#CC0000",    # Red
        }.get(self.value, "#888888")


@dataclass
class ProfileMetrics:
    """Current metrics used for drive profile classification."""
    # Rolling window metrics
    avg_throttle: float = 0.0        # Average throttle position (0-100%)
    throttle_variance: float = 0.0   # Variance of throttle changes
    throttle_change_rate: float = 0.0  # How quickly throttle changes
    avg_rpm: float = 0.0             # Average RPM
    rpm_variance: float = 0.0        # RPM variance (higher = more sporty)
    avg_load: float = 0.0            # Average engine load
    est_consumption_lh: float = 0.0  # Estimated L/h consumption
    brake_events: int = 0            # Brake event count in window
    shift_rpm_avg: float = 0.0       # Average RPM at gear shifts
    
    # Derived score (0-100, where 0=eco, 50=normal, 100=sport)
    profile_score: float = 50.0
    
    # Current classification
    profile: DriveProfile = DriveProfile.NORMAL
    
    # Confidence (0-1, how confident in the classification)
    confidence: float = 0.5


class DriveProfileAnalyzer:
    """Real-time driving style analyzer from V50 CAN bus data.
    
    Uses rolling windows of CAN bus data points to classify
    the current driving style as Eco, Normal, or Sport.
    
    Window sizes:
    - Short window (10s): Quick response, noisy
    - Medium window (30s): Balanced (primary)
    - Long window (120s): Trend analysis
    """
    
    # Window sizes in samples (at 2 Hz update rate)
    SHORT_WINDOW = 20       # 10 seconds
    MEDIUM_WINDOW = 60      # 30 seconds
    LONG_WINDOW = 240       # 120 seconds
    
    # Scoring thresholds
    ECO_THRESHOLD = 30       # Score < 30 = ECO
    SPORT_THRESHOLD = 65    # Score > 65 = SPORT
    # Between = NORMAL
    
    # Scoring weights
    WEIGHTS = {
        'avg_throttle': 0.20,
        'throttle_variance': 0.15,
        'throttle_change': 0.15,
        'avg_rpm': 0.15,
        'rpm_variance': 0.10,
        'avg_load': 0.10,
        'consumption': 0.10,
        'brake_events': 0.05,
    }
    
    def __init__(self):
        # Rolling data buffers
        self.throttle_history = deque(maxlen=self.LONG_WINDOW)
        self.rpm_history = deque(maxlen=self.LONG_WINDOW)
        self.load_history = deque(maxlen=self.LONG_WINDOW)
        self.speed_history = deque(maxlen=self.LONG_WINDOW)
        self.consumption_history = deque(maxlen=self.LONG_WINDOW)
        
        # Track throttle changes
        self._prev_throttle = 0.0
        self._throttle_changes = deque(maxlen=self.LONG_WINDOW)
        
        # Track brake events (speed decreasing)
        self._prev_speed = 0.0
        self._speed_decreases = deque(maxlen=self.LONG_WINDOW)
        
        # Track gear shifts
        self._prev_gear = 0
        self._shift_rpms = deque(maxlen=20)
        
        # Profile state
        self.metrics = ProfileMetrics()
        self.update_count = 0
        self.last_update = time.time()
        
        # History for logging
        self.profile_history = deque(maxlen=1000)  # Last 500s of profile data
    
    def update(self, state: V50State) -> ProfileMetrics:
        """Update the drive profile analysis with new vehicle state.
        
        Should be called at a regular interval (2 Hz recommended).
        """
        now = time.time()
        
        # Only process if vehicle is moving (speed > 2 km/h)
        if state.speed_kmh < 2.0:
            self.metrics.profile = DriveProfile.NORMAL
            self.metrics.confidence = 0.3  # Low confidence at standstill
            return self.metrics
        
        # Add data points to history
        self.throttle_history.append(state.throttle_pct)
        self.rpm_history.append(state.rpm)
        self.load_history.append(state.engine_load_pct)
        self.speed_history.append(state.speed_kmh)
        
        # Calculate instantaneous consumption (L/h from MAF)
        from v50_can_decoder import calculate_fuel_consumption
        consumption = calculate_fuel_consumption(state.rpm, state.maf_g_per_s)
        self.consumption_history.append(consumption)
        
        # Track throttle changes
        throttle_change = abs(state.throttle_pct - self._prev_throttle)
        self._throttle_changes.append(throttle_change)
        self._prev_throttle = state.throttle_pct
        
        # Track speed decreases (brake proxy)
        speed_change = state.speed_kmh - self._prev_speed
        self._speed_decreases.append(min(0, speed_change))  # Only negative (braking)
        self._prev_speed = state.speed_kmh
        
        # Track gear shifts
        if state.gear != self._prev_gear and self._prev_gear > 0:
            self._shift_rpms.append(state.rpm)
        self._prev_gear = state.gear
        
        # Calculate metrics from medium window
        self._calculate_metrics()
        
        # Classify profile
        self._classify_profile()
        
        self.update_count += 1
        self.last_update = now
        
        # Record history
        self.profile_history.append({
            'time': now,
            'profile': self.metrics.profile.value,
            'score': self.metrics.profile_score,
            'confidence': self.metrics.confidence,
        })
        
        return self.metrics
    
    def _calculate_metrics(self):
        """Calculate profile metrics from data windows."""
        # Use medium window for primary metrics
        n = min(len(self.throttle_history), self.MEDIUM_WINDOW)
        if n < 5:
            return
        
        # Throttle metrics
        throttle_data = list(self.throttle_history)[-n:]
        self.metrics.avg_throttle = sum(throttle_data) / n
        
        if n > 1:
            mean = self.metrics.avg_throttle
            self.metrics.throttle_variance = sum((x - mean)**2 for x in throttle_data) / (n - 1)
        
        # Throttle change rate
        changes = list(self._throttle_changes)[-n:]
        if changes:
            self.metrics.throttle_change_rate = sum(changes) / len(changes)
        
        # RPM metrics
        rpm_data = list(self.rpm_history)[-n:]
        self.metrics.avg_rpm = sum(rpm_data) / n
        
        if n > 1:
            mean_rpm = self.metrics.avg_rpm
            self.metrics.rpm_variance = sum((x - mean_rpm)**2 for x in rpm_data) / (n - 1)
        
        # Engine load
        load_data = list(self.load_history)[-n:]
        self.metrics.avg_load = sum(load_data) / n
        
        # Consumption
        cons_data = list(self.consumption_history)[-n:]
        if cons_data:
            self.metrics.est_consumption_lh = sum(cons_data) / len(cons_data)
        
        # Brake events (significant speed decreases > 5 km/h in 0.5s)
        speed_decreases = list(self._speed_decreases)[-n:]
        self.metrics.brake_events = sum(1 for d in speed_decreases if d < -5.0)
        
        # Average shift RPM
        if self._shift_rpms:
            self.metrics.shift_rpm_avg = sum(self._shift_rpms) / len(self._shift_rpms)
    
    def _classify_profile(self):
        """Classify driving profile based on calculated metrics."""
        # Normalize each metric to 0-100 scale
        scores = {}
        
        # Average throttle: 0-20% = eco, 20-50% = normal, 50-100% = sport
        scores['avg_throttle'] = min(100, self.metrics.avg_throttle * 1.5)
        
        # Throttle variance: Low = eco, high = sporty
        scores['throttle_variance'] = min(100, self.metrics.throttle_variance * 3.0)
        
        # Throttle change rate: Slow = eco, aggressive = sporty
        scores['throttle_change'] = min(100, self.metrics.throttle_change_rate * 5.0)
        
        # Average RPM: <2000 = eco, 2000-3000 = normal, >3000 = sporty
        rpm_score = max(0, (self.metrics.avg_rpm - 800) / 40)
        scores['avg_rpm'] = min(100, rpm_score)
        
        # RPM variance: Steady = eco, Variable = sporty
        scores['rpm_variance'] = min(100, math.sqrt(self.metrics.rpm_variance) * 0.15)
        
        # Engine load: Low = eco, high = sporty
        scores['avg_load'] = min(100, self.metrics.avg_load * 1.2)
        
        # Consumption: <3 L/h = eco, 3-8 = normal, >8 = sporty  
        scores['consumption'] = min(100, max(0, (self.metrics.est_consumption_lh - 1.5) * 10))
        
        # Brake events: Few = eco/normal, many = sporty
        scores['brake_events'] = min(100, self.metrics.brake_events * 15)
        
        # Weighted score
        total_score = 0
        for key, weight in self.WEIGHTS.items():
            if key == 'brake_events':
                total_score += scores.get('brake_events', 0) * weight
            else:
                total_score += scores.get(key, 0) * weight
        
        self.metrics.profile_score = max(0, min(100, total_score))
        
        # Classify
        if self.metrics.profile_score < self.ECO_THRESHOLD:
            self.metrics.profile = DriveProfile.ECO
        elif self.metrics.profile_score > self.SPORT_THRESHOLD:
            self.metrics.profile = DriveProfile.SPORT
        else:
            self.metrics.profile = DriveProfile.NORMAL
        
        # Confidence: higher when further from thresholds
        if self.metrics.profile == DriveProfile.ECO:
            self.metrics.confidence = min(1.0, (self.ECO_THRESHOLD - self.metrics.profile_score) / 30)
        elif self.metrics.profile == DriveProfile.SPORT:
            self.metrics.confidence = min(1.0, (self.metrics.profile_score - self.SPORT_THRESHOLD) / 35)
        else:
            # Normal: confidence peaks at 50, drops near thresholds
            dist_to_eco = self.metrics.profile_score - self.ECO_THRESHOLD
            dist_to_sport = self.SPORT_THRESHOLD - self.metrics.profile_score
            min_dist = min(dist_to_eco, dist_to_sport)
            self.metrics.confidence = min(1.0, min_dist / 17.5)
    
    def get_profile_trend(self, window: int = 60) -> str:
        """Get the trend of the driving profile over a time window.
        
        Returns: 'towards_eco', 'stable', or 'towards_sport'
        """
        if len(self.profile_history) < window:
            return 'stable'
        
        recent = list(self.profile_history)[-window:]
        
        # Simple linear regression on scores
        n = len(recent)
        sum_x = sum(range(n))
        sum_y = sum(r['score'] for r in recent)
        sum_xy = sum(i * recent[i]['score'] for i in range(n))
        sum_x2 = sum(i**2 for i in range(n))
        
        if n * sum_x2 - sum_x**2 == 0:
            return 'stable'
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)
        
        if slope < -0.5:
            return 'towards_eco'
        elif slope > 0.5:
            return 'towards_sport'
        else:
            return 'stable'
    
    def get_stats(self) -> Dict:
        """Get analyzer statistics."""
        return {
            "profile": self.metrics.profile.value,
            "profile_display": self.metrics.profile.display_name,
            "score": round(self.metrics.profile_score, 1),
            "confidence": round(self.metrics.confidence, 2),
            "trend": self.get_profile_trend(),
            "avg_throttle": round(self.metrics.avg_throttle, 1),
            "avg_rpm": round(self.metrics.avg_rpm, 0),
            "avg_load": round(self.metrics.avg_load, 1),
            "consumption_lh": round(self.metrics.est_consumption_lh, 1),
            "brake_events": self.metrics.brake_events,
            "shift_rpm_avg": round(self.metrics.shift_rpm_avg, 0),
            "updates": self.update_count,
        }
    
    def render_console(self) -> str:
        """Render a console-friendly drive profile display."""
        m = self.metrics
        profile = m.profile
        
        # Profile score bar
        bar_len = 40
        eco_len = int(self.ECO_THRESHOLD / 100 * bar_len)
        sport_start = int(self.SPORT_THRESHOLD / 100 * bar_len)
        score_pos = int(m.profile_score / 100 * bar_len)
        
        bar = list('─' * bar_len)
        for i in range(eco_len):
            bar[i] = '─'
        for i in range(sport_start, bar_len):
            bar[i] = '─'
        if 0 <= score_pos < bar_len:
            bar[score_pos] = '▲'
        bar_str = ''.join(bar)
        
        trend_arrow = {
            'towards_eco': '↘',
            'stable': '→',
            'towards_sport': '↗'
        }.get(self.get_profile_trend(), '→')
        
        lines = [
            f"""  🚗 Drive Profile: {profile.display_name} (Score: {m.profile_score:.0f}/100 {trend_arrow})""",
            f"""  [{bar_str}]""",
            f"""   ECO          NORMAL          SPORT""",
            f"""""",
            f"  Throttle: {m.avg_throttle:>5.1f}% avg | {m.throttle_change_rate:>5.1f}%/s change",
            f"  RPM:     {m.avg_rpm:>5.0f} avg | Variance: {math.sqrt(m.rpm_variance):.0f}",
            f"  Load:    {m.avg_load:>5.1f}% | Consumption: {m.est_consumption_lh:.1f} L/h",
            f"  Brakes:  {m.brake_events} events | Shift RPM: {m.shift_rpm_avg:.0f}",
            f"  Confidence: {m.confidence:.0%}",
        ]
        
        return '\n'.join(lines)


# =============================================================================
# Fuel Economy Tracker (extends the drive profile)
# =============================================================================

class FuelEconomyTracker:
    """Tracks fuel economy from CAN bus data.
    
    Calculates:
    - Instant L/100km (from MAF and speed)
    - Rolling average L/100km
    - Trip fuel consumption
    - Estimated range
    """
    
    def __init__(self, tank_capacity_liters: float = 60.0):
        self.tank_capacity = tank_capacity_liters
        self.state = V50State()
        
        # Trip counters
        self.trip_start_km = 0.0
        self.trip_fuel_liters = 0.0
        self.trip_duration_s = 0.0
        self.trip_started = False
        
        # Rolling averages
        self._consumption_samples = deque(maxlen=120)  # 1 min at 2Hz
        self._speed_samples = deque(maxlen=120)
        
        # Current
        self.instant_l100km = 0.0
        self.avg_l100km = 0.0
        self.estimated_range_km = 0.0
    
    def update(self, state: V50State, dt: float = 0.5):
        """Update fuel economy calculations.
        
        Args:
            state: Current V50State
            dt: Time delta since last update (seconds)
        """
        from v50_can_decoder import calculate_fuel_consumption
        
        # Instant consumption (L/h)
        consumption_lh = calculate_fuel_consumption(state.rpm, state.maf_g_per_s)
        
        self._consumption_samples.append(consumption_lh)
        self._speed_samples.append(state.speed_kmh)
        
        # Convert L/h to L/100km
        if state.speed_kmh > 5:
            self.instant_l100km = (consumption_lh / state.speed_kmh) * 100
        else:
            self.instant_l100km = 0 if state.speed_kmh < 1 else consumption_lh * 10  # Idle equivalent
        
        # Rolling average L/100km
        if self._consumption_samples and self._speed_samples:
            avg_lh = sum(self._consumption_samples) / len(self._consumption_samples)
            avg_speed = sum(self._speed_samples) / len(self._speed_samples)
            if avg_speed > 5:
                self.avg_l100km = (avg_lh / avg_speed) * 100
        
        # Trip tracking
        if not self.trip_started and state.speed_kmh > 2:
            self.trip_start_km = state.odometer_km
            self.trip_fuel_liters = 0
            self.trip_duration_s = 0
            self.trip_started = True
        
        if self.trip_started:
            self.trip_fuel_liters += consumption_lh * (dt / 3600)  # L/h * seconds = liters
            self.trip_duration_s += dt
        
        # Estimated range
        if self.instant_l100km > 0 and state.fuel_level_pct > 0:
            fuel_remaining = (state.fuel_level_pct / 100) * self.tank_capacity_liters
            self.estimated_range_km = (fuel_remaining / self.avg_l100km) * 100 if self.avg_l100km > 0 else 0
        else:
            self.estimated_range_km = 0
    
    def reset_trip(self):
        """Reset trip counters."""
        self.trip_fuel_liters = 0
        self.trip_duration_s = 0
        self.trip_started = False
    
    def get_stats(self) -> Dict:
        """Get fuel economy statistics."""
        trip_km = self.state.odometer_km - self.trip_start_km if self.trip_started else 0
        trip_l100km = (self.trip_fuel_liters / trip_km * 100) if trip_km > 0.5 else 0
        
        return {
            "instant_l100km": round(self.instant_l100km, 1),
            "avg_l100km": round(self.avg_l100km, 1),
            "trip_km": round(trip_km, 1),
            "trip_liters": round(self.trip_fuel_liters, 2),
            "trip_l100km": round(trip_l100km, 1),
            "trip_duration_min": round(self.trip_duration_s / 60, 1),
            "estimated_range_km": round(self.estimated_range_km, 0),
        }


# =============================================================================
# Main (for testing)
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description='V50 Drive Profile Analyzer')
    parser.add_argument('--simulate', action='store_true',
                       help='Run with simulated driving data')
    parser.add_argument('--eco', action='store_true',
                       help='Simulate eco driving style')
    parser.add_argument('--sport', action='store_true',
                       help='Simulate sporty driving style')
    parser.add_argument('--verbose', '-v', action='store_true')
    
    args = parser.parse_args()
    
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
    
    if args.simulate:
        analyzer = DriveProfileAnalyzer()
        fuel_tracker = FuelEconomyTracker()
        state = V50State()
        
        print("V50 Drive Profile Analyzer — Simulation")
        print("Simulating:", "ECO" if args.eco else "SPORT" if args.sport else "NORMAL", "driving")
        print("Press Ctrl+C to stop\n")
        
        import random
        t = 0
        
        try:
            while True:
                if args.eco:
                    rpm = 1200 + 400 * random.random()
                    speed = 40 + 30 * random.random()
                    throttle = 10 + 15 * random.random()
                elif args.sport:
                    rpm = 3000 + 2000 * random.random()
                    speed = 80 + 60 * random.random()
                    throttle = 50 + 40 * random.random()
                else:
                    rpm = 1800 + 1500 * abs((t * 0.08) % 2 - 1)
                    speed = 60 + 40 * abs((t * 0.05) % 2 - 1)
                    throttle = 25 + 30 * abs((t * 0.12) % 2 - 1)
                
                # Update state
                rpm_data = int(rpm / 0.25).to_bytes(2, 'little') + b'\x00' * 6
                speed_data = int(speed / 0.01).to_bytes(2, 'little') + b'\x00' * 6
                throttle_data = bytes([int(throttle / 0.390625)]) + b'\x00' * 7
                temp_data = bytes([90 + 40]) + b'\x00' * 7
                load_data = bytes([int(min(throttle * 1.1, 100) / 0.390625)]) + b'\x00' * 7
                maf_data = int(rpm * 0.003 * 100).to_bytes(2, 'little') + b'\x00' * 6
                fuel_data = bytes([int(65 / 0.390625)]) + b'\x00' * 7
                odo_data = int(142500 + t * 0.014).to_bytes(4, 'little') + b'\x00' * 4
                
                state.update(0x0C0, rpm_data)
                state.update(0x0E0, speed_data)
                state.update(0x0D0, throttle_data)
                state.update(0x0C8, temp_data)
                state.update(0x0D8, load_data)
                state.update(0x0F0, fuel_data)
                state.update(0x328, odo_data)
                
                # Analyze
                metrics = analyzer.update(state)
                fuel_tracker.update(state)
                
                # Display
                print(f"\033[2J\033[H")  # Clear screen
                print(state.summary())
                print()
                print(analyzer.render_console())
                print()
                fuel_stats = fuel_tracker.get_stats()
                print(f"  ⛽ Instant: {fuel_stats['instant_l100km']:.1f} L/100km | Avg: {fuel_stats['avg_l100km']:.1f} L/100km")
                print(f"  ⛽ Range:  {fuel_stats['estimated_range_km']:.0f} km | Trip: {fuel_stats['trip_l100km']:.1f} L/100km")
                
                t += 1
                time.sleep(0.5)
        
        except KeyboardInterrupt:
            print("\nStopped.")
            print("\nFinal stats:")
            print(json.dumps(analyzer.get_stats(), indent=2))
    
    else:
        parser.print_help()
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
