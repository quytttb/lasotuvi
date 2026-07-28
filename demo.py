#!/usr/bin/env python
"""Demo: build a Zi Wei Dou Shu chart."""
from lasotuvi.chart_builder import build_earth_plate
from lasotuvi.heaven_plate import HeavenPlate

day, month, year = 15, 8, 1990
hour = 1  # Zi
gender = 1  # male
is_solar = True
timezone = 7
name = "Nguyễn Văn A"

plate = build_earth_plate(day, month, year, hour, gender, is_solar, timezone)
heaven = HeavenPlate(day, month, year, hour, gender, name, plate, is_solar, timezone)

print(f"Name: {name}")
print(f"Life palace: {plate.life_palace} ({plate.palaces[plate.life_palace].palace_name})")
print(f"Body palace: {plate.body_palace}")
print(f"Bureau: {heaven.bureau_name}")
print(f"Life master: {heaven.life_master}")
print(f"Body master: {heaven.body_master}")
print(f"Natal element: {heaven.natal_element_name}")
print(f"Relation: {heaven.generation_control_status}")
print("\nStars in Life palace:")
for star in plate.palaces[plate.life_palace].stars:
    bright = f" ({star.get('brightness')})" if star.get("brightness") else ""
    print(f"  - {star['name']}{bright}")
