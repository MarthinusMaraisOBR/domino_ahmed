import pandas as pd
import numpy as np

# Read force predictions
forces = []
with open('test_output.txt', 'r') as f:
    current_run = {}
    for line in f:
        if 'Drag=' in line:
            parts = line.split()
            run_num = int(parts[1].replace('run_', ''))
            current_run = {'run': run_num, 'drag_pred': float(parts[2]), 'drag_true': float(parts[3])}
        elif 'Lift=' in line:
            parts = line.split()
            current_run['lift_pred'] = float(parts[2])
            current_run['lift_true'] = float(parts[3])
            forces.append(current_run)

df_forces = pd.DataFrame(forces)

# Get frontal area and coefficients for each case
frontal_areas = []
body_heights = []
body_widths = []
cd_true_values = []
cl_true_values = []

for run in df_forces['run']:
    # Read geometry file for this specific run
    geo_file = f'/data/ahmed_data/organized/coefficients/fine/geo_parameters_{run}.csv'
    geo_df = pd.read_csv(geo_file)
    
    # Extract dimensions (in mm)
    body_height = geo_df['body-height'].iloc[0]
    body_width = geo_df['body-width'].iloc[0]
    
    # Calculate frontal area (convert mm² to m²)
    frontal_area = (body_height * body_width) / 1e6
    
    body_heights.append(body_height)
    body_widths.append(body_width)
    frontal_areas.append(frontal_area)
    
    # Read coefficient file
    coeff_file = f'/data/ahmed_data/organized/coefficients/fine/force_mom_varref_{run}.csv'
    coeff_df = pd.read_csv(coeff_file)
    cd_true_values.append(coeff_df['cd'].iloc[0])
    cl_true_values.append(coeff_df['cl'].iloc[0])

# Add to dataframe
df_forces['body_height_mm'] = body_heights
df_forces['body_width_mm'] = body_widths
df_forces['frontal_area_m2'] = frontal_areas
df_forces['Cd_true_file'] = cd_true_values
df_forces['Cl_true_file'] = cl_true_values

# Calculate coefficients using individual frontal areas
df_forces['Cd_pred_calc'] = 2 * df_forces['drag_pred'] / df_forces['frontal_area_m2']
df_forces['Cd_true_calc'] = 2 * df_forces['drag_true'] / df_forces['frontal_area_m2']
df_forces['Cl_pred_calc'] = 2 * df_forces['lift_pred'] / df_forces['frontal_area_m2']
df_forces['Cl_true_calc'] = 2 * df_forces['lift_true'] / df_forces['frontal_area_m2']

# Calculate errors (comparing predicted to file values)
df_forces['Cd_error_%'] = 100 * (df_forces['Cd_pred_calc'] - df_forces['Cd_true_file']) / df_forces['Cd_true_file']
df_forces['Cl_error_%'] = 100 * (df_forces['Cl_pred_calc'] - df_forces['Cl_true_file']) / df_forces['Cl_true_file']

print("\n=== COEFFICIENT COMPARISON RESULTS ===")
print(f"\nFrontal area statistics:")
print(f"  Min: {df_forces['frontal_area_m2'].min():.6f} m²")
print(f"  Max: {df_forces['frontal_area_m2'].max():.6f} m²")
print(f"  Mean: {df_forces['frontal_area_m2'].mean():.6f} m²")

print("\nFirst 10 cases:")
print(df_forces[['run', 'frontal_area_m2', 'Cd_pred_calc', 'Cd_true_file', 'Cd_error_%']].head(10).to_string())

print("\n=== OVERALL STATISTICS ===")
print(f"Mean Cd error: {df_forces['Cd_error_%'].mean():.2f}%")
print(f"Mean absolute Cd error: {df_forces['Cd_error_%'].abs().mean():.2f}%")
print(f"Mean absolute Cl error: {df_forces['Cl_error_%'].abs().mean():.2f}%")
print(f"Cd RMSE: {np.sqrt(np.mean((df_forces['Cd_pred_calc'] - df_forces['Cd_true_file'])**2)):.4f}")
print(f"Cl RMSE: {np.sqrt(np.mean((df_forces['Cl_pred_calc'] - df_forces['Cl_true_file'])**2)):.4f}")

# Calculate R² for coefficients
from scipy import stats
r2_cd = stats.pearsonr(df_forces['Cd_true_file'], df_forces['Cd_pred_calc'])[0]**2
r2_cl = stats.pearsonr(df_forces['Cl_true_file'], df_forces['Cl_pred_calc'])[0]**2
print(f"\nR² scores:")
print(f"  Cd R²: {r2_cd:.4f}")
print(f"  Cl R²: {r2_cl:.4f}")

# Save complete results
df_forces.to_csv('coefficient_comparison.csv', index=False)
print("\n✅ Full results saved to coefficient_comparison.csv")
print("   This file includes frontal areas, predicted and actual coefficients for each case")