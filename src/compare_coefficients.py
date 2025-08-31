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

# Read geometric parameters - corrected path
geo_df = pd.read_csv('/data/ahmed_data/organized/coefficients/fine/geo_parameters_1.csv')
# Frontal area = body-height * body-width (in mm, so convert to m)
frontal_area = (geo_df['body-height'].iloc[0] * geo_df['body-width'].iloc[0]) / 1e6
print(f"Frontal area: {frontal_area:.6f} m²")

# Calculate coefficients (velocity=1, density=1)
df_forces['Cd_pred'] = 2 * df_forces['drag_pred'] / frontal_area
df_forces['Cd_true'] = 2 * df_forces['drag_true'] / frontal_area
df_forces['Cl_pred'] = 2 * df_forces['lift_pred'] / frontal_area
df_forces['Cl_true'] = 2 * df_forces['lift_true'] / frontal_area

# Read actual coefficient values from files - corrected path
cd_true_values = []
cl_true_values = []
for run in df_forces['run']:
    coeff_file = f'/data/ahmed_data/organized/coefficients/fine/force_mom_varref_{run}.csv'
    try:
        coeff_df = pd.read_csv(coeff_file)
        cd_true_values.append(coeff_df['cd'].iloc[0])
        cl_true_values.append(coeff_df['cl'].iloc[0])
    except:
        cd_true_values.append(np.nan)
        cl_true_values.append(np.nan)

df_forces['Cd_file'] = cd_true_values
df_forces['Cl_file'] = cl_true_values

# Calculate errors
df_forces['Cd_error_%'] = 100 * (df_forces['Cd_pred'] - df_forces['Cd_file']) / df_forces['Cd_file']
df_forces['Cl_error_%'] = 100 * (df_forces['Cl_pred'] - df_forces['Cl_file']) / df_forces['Cl_file']

print("\nCoefficient Comparison (first 10 cases):")
print(df_forces[['run', 'Cd_pred', 'Cd_file', 'Cd_error_%', 'Cl_pred', 'Cl_file', 'Cl_error_%']].head(10))

print("\nStatistics:")
print(f"Mean Cd error: {df_forces['Cd_error_%'].mean():.2f}%")
print(f"Mean absolute Cl error: {df_forces['Cl_error_%'].abs().mean():.2f}%")
print(f"Cd RMSE: {np.sqrt(np.mean((df_forces['Cd_pred'] - df_forces['Cd_file'])**2)):.4f}")
print(f"Cl RMSE: {np.sqrt(np.mean((df_forces['Cl_pred'] - df_forces['Cl_file'])**2)):.4f}")

# Save results
df_forces.to_csv('coefficient_comparison.csv', index=False)
print("\nResults saved to coefficient_comparison.csv")