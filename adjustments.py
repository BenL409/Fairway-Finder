from weather_test import data
import math


def get_wind_adjustment(wind_mph, wind_deg, hole_heading):
    angle_diff = wind_deg - hole_heading
    radians = math.radians(angle_diff)
    
    headwind_factor = math.cos(radians)
    effective_wind = wind_mph * headwind_factor
    if effective_wind > 0:
        return round(effective_wind * 1.0)  # Tailwind adjustment
    elif effective_wind < 0:
        return round(effective_wind * 0.5)  # Headwind adjustment
    else:
        return 0  # No adjustment for crosswind

def get_wind_type(wind_deg, hole_heading):
    
    diff = abs(wind_deg - hole_heading) % 360
    if diff > 180:
        diff = 360 - diff
    if diff < 45:
        return "headwind"
    elif diff > 135:
        return "tailwind"
    else:
        return "crosswind"

def get_temp_adjustment(temp_c):
    base_temp = 15
    difference = base_temp - temp_c
    adjustment = (difference / 5) * 2
    return round(adjustment)




