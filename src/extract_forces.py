import re

# Read the test output
test_output = """
Drag= run_451 0.015251859 0.020506265
Lift= run_451 -0.0050089946 -0.008251523
Drag= run_452 0.013661954 0.016773319
Lift= run_452 -0.0009903582 -0.0011722692
# ... add all your test output here
"""

# Parse the output
drag_data = []
lift_data = []

with open('test_output.txt', 'r') as f:
    for line in f:
        if line.startswith('Drag='):
            parts = line.split()
            run = parts[1]
            pred = float(parts[2])
            true = float(parts[3])
            drag_data.append({'run': run, 'pred': pred, 'true': true})
        elif line.startswith('Lift='):
            parts = line.split()
            run = parts[1]
            pred = float(parts[2])
            true = float(parts[3])
            lift_data.append({'run': run, 'pred': pred, 'true': true})

# Calculate statistics
import numpy as np

drag_pred = [d['pred'] for d in drag_data]
drag_true = [d['true'] for d in drag_data]
lift_pred = [l['pred'] for l in lift_data]
lift_true = [l['true'] for l in lift_data]

print(f"Drag - Mean Absolute Error: {np.mean(np.abs(np.array(drag_pred) - np.array(drag_true))):.6f}")
print(f"Lift - Mean Absolute Error: {np.mean(np.abs(np.array(lift_pred) - np.array(lift_true))):.6f}")
print(f"Drag - Mean Relative Error: {np.mean(np.abs((np.array(drag_pred) - np.array(drag_true))/np.array(drag_true))):.2%}")
print(f"Lift - Mean Relative Error: {np.mean(np.abs((np.array(lift_pred) - np.array(lift_true))/np.array(lift_true))):.2%}")
