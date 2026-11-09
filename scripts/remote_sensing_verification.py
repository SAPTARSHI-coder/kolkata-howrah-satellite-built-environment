# Standalone Verification Script for Landsat Remote Sensing & Built Environment
import os, glob
import pandas as pd
import numpy as np

script_dir = os.path.dirname(os.path.abspath(__file__))
candidate_dirs = [
    os.environ.get('REMOTE_SENSING_DIR', ''),
    os.path.abspath(os.path.join(script_dir, '../data/Remote_Sensing_Data')),
    os.path.abspath(os.path.join(script_dir, '../../../02_PROCESSED_DATA/Remote_Sensing_Data')),
    '/Users/saptarshisadhu/Desktop/papers/02_PROCESSED_DATA/Remote_Sensing_Data'
]
base_dir = next((p for p in candidate_dirs if p and os.path.exists(p)), candidate_dirs[-1])

files_2024 = sorted(glob.glob(os.path.join(base_dir, '*_Landsat_Indices_2024.csv')))
results = []
for f in files_2024:
    stn = os.path.basename(f).replace('_Landsat_Indices_2024.csv', '')
    df24 = pd.read_csv(f).dropna(subset=['NDVI', 'NDBI', 'NDWI', 'LST_Landsat_C'])
    # Filter physical LST (>10 C) to remove -123.15 C cloud/fill artifact and deduplicate dates
    df24 = df24[df24['LST_Landsat_C'] > 10.0].groupby('date', as_index=False).mean(numeric_only=True)
    f25 = os.path.join(base_dir, f'{stn}_Landsat_Indices_2025.csv')
    if os.path.exists(f25):
        df25 = pd.read_csv(f25).dropna(subset=['NDVI', 'NDBI', 'NDWI', 'LST_Landsat_C'])
        df25 = df25[df25['LST_Landsat_C'] > 10.0].groupby('date', as_index=False).mean(numeric_only=True)
    else:
        df25 = pd.DataFrame()
    results.append({
        'Station': stn,
        'N_Days_2024': len(df24),
        'NDVI_2024': round(df24['NDVI'].mean(), 4),
        'NDBI_2024': round(df24['NDBI'].mean(), 4),
        'NDWI_2024': round(df24['NDWI'].mean(), 4),
        'LST_C_2024': round(df24['LST_Landsat_C'].mean(), 2),
        'N_Days_2025': len(df25),
        'NDVI_2025': round(df25['NDVI'].mean(), 4) if not df25.empty else np.nan,
        'NDBI_2025': round(df25['NDBI'].mean(), 4) if not df25.empty else np.nan,
        'NDWI_2025': round(df25['NDWI'].mean(), 4) if not df25.empty else np.nan,
        'LST_C_2025': round(df25['LST_Landsat_C'].mean(), 2) if not df25.empty else np.nan
    })
df_res = pd.DataFrame(results)

out_csv = os.path.join(script_dir, 'satellite_ground_reconciliation.csv')
out_csv_clean = os.path.join(script_dir, 'satellite_ground_reconciliation_screened.csv')
out_data_csv = os.path.join(script_dir, '../data/satellite_ground_reconciliation.csv')
out_data_clean = os.path.join(script_dir, '../data/satellite_ground_reconciliation_screened.csv')

df_res.to_csv(out_csv, index=False)
df_res.to_csv(out_csv_clean, index=False)
if os.path.exists(os.path.join(script_dir, '../data')):
    df_res.to_csv(out_data_csv, index=False)
    df_res.to_csv(out_data_clean, index=False)

print('Remote sensing verification executed successfully. Output saved to:', out_csv)
print(df_res.to_string(index=False))
