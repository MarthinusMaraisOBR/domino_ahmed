# File: check_dimensionalization.py
import numpy as np

# Check what's in your test.py and training files
print("=== CHECKING NON-DIMENSIONALIZATION CONSTANTS ===")

# From test.py (lines 26-27)
print("\nIn test.py:")
print("AIR_DENSITY = 1.0")  
print("STREAM_VELOCITY = 1.00")

# From openfoam_datapipe.py (lines 33-34)
print("\nIn openfoam_datapipe.py:")
print("AIR_DENSITY = 1.205")
print("STREAM_VELOCITY = 1")

# Your actual Ahmed dataset
print("\nYour Ahmed dataset properties:")
print("Velocity = 1 m/s")
print("Density = 1 kg/m³")
print("Kinematic viscosity = 1.5111e-5 m²/s")

print("\n=== IMPACT ANALYSIS ===")
print("If training uses density=1.205 but testing uses density=1.0:")
print(f"Force scaling error = {1.205/1.0:.3f} = 20.5% over-prediction during training")
print(f"This would cause under-prediction during testing!")
