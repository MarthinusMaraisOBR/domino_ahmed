# File: debug_force_calculation.py
import numpy as np
import pandas as pd

# Read one of your test outputs
test_file = 'test_output_exp6_100_test.txt'  # or whichever you have

# Extract a few cases to analyze
forces = []
with open(test_file, 'r') as f:
    for line in f:
        if 'Drag=' in line:
            parts = line.split()
            forces.append({
                'run': parts[1],
                'drag_pred': float(parts[2]),
                'drag_true': float(parts[3])
            })

df = pd.DataFrame(forces[:5])  # First 5 cases
print("=== FORCE COMPARISON ===")
print(df)

# Check the consistent ratio
df['ratio'] = df['drag_pred'] / df['drag_true']
print(f"\nMean ratio: {df['ratio'].mean():.4f}")
print(f"Std ratio: {df['ratio'].std():.4f}")

# If ratio is consistently ~0.84, it suggests a scaling issue
if abs(df['ratio'].mean() - 0.84) < 0.02:
    print("\n⚠️ CONSISTENT 16% UNDER-PREDICTION DETECTED!")
    print("Possible causes:")
    print("1. Density mismatch: Training with 1.205, testing with 1.0")
    print("2. Force integration missing a factor")
    print("3. Scaling factors computed with wrong constants")
