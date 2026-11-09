"""
Random Forest Land Use Regression (RF LUR) Spatiotemporal Benchmark
Ingests authentic Landsat buffer indices and CAAQMS ground PM2.5 telemetry.
Evaluates spatial holdout, temporal group k-fold, forward temporal transfer, and random CV.
"""
import os
import sys
import glob
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split, KFold, GroupKFold

script_dir = os.path.dirname(os.path.abspath(__file__))
excel_candidates = [
    os.environ.get('STATION_DATA_DIR', ''),
    os.path.abspath(os.path.join(script_dir, '../data/Cleaned_Station_Data')),
    os.path.abspath(os.path.join(script_dir, '../../../02_PROCESSED_DATA/Cleaned_Station_Data')),
    "/Users/saptarshisadhu/Desktop/papers/Paper Writing things/New folder (7)"
]
EXCEL_DIR = next((p for p in excel_candidates if p and os.path.exists(p)), excel_candidates[-1])

f14_candidates = [
    os.environ.get('REMOTE_SENSING_DIR', ''),
    os.path.abspath(os.path.join(script_dir, '../data/Remote_Sensing_Data')),
    os.path.abspath(os.path.join(script_dir, '../../../02_PROCESSED_DATA/Remote_Sensing_Data')),
    "/Users/saptarshisadhu/Desktop/papers/Paperworks/Journal/14. Impact of built environments"
]
F14_DIR = next((p for p in f14_candidates if p and os.path.exists(p)), f14_candidates[-1])

OUTPUT_METRICS_CSV = os.path.join(script_dir, 'rf_lur_benchmark_metrics.csv')

STATION_MAP = {
    'Ballygunge': 'BG',
    'Barrackpore': 'SVSPA',
    'Belur': 'BM',
    'Bidhannagar': 'BN',
    'BotanicalGarden': 'BOG',
    'Dasnagar': 'DN',
    'FortWilliam': 'FW',
    'Ghusuri': 'GH',
    'Jadavpur': 'JD',
    'Padmapukur': 'PP',
    'RabindraSarovar': 'RS',
    'Rbu': 'RBU',
    'Victoria': 'VC'
}

def load_data():
    records = []
    print("Ingesting CAAQMS daily ground means and Landsat buffer indices...")
    for reg, code in STATION_MAP.items():
        daily_pm = {}
        for yr in [2024, 2025]:
            ef = os.path.join(EXCEL_DIR, f"{code}_{yr}_MLL.xlsx")
            if os.path.exists(ef):
                try:
                    edf = pd.read_excel(ef)
                    edf['Date'] = pd.to_datetime(edf['DateTime']).dt.strftime('%Y-%m-%d')
                    d_means = edf.groupby('Date')['PM2.5'].mean().dropna().to_dict()
                    daily_pm.update(d_means)
                except Exception as e:
                    print(f"Error reading {ef}: {e}")
        
        for yr in [2024, 2025]:
            lf = os.path.join(F14_DIR, f"{reg}_Landsat_Indices_{yr}.csv")
            if os.path.exists(lf):
                try:
                    ldf = pd.read_csv(lf).dropna(subset=['NDVI', 'NDBI', 'NDWI', 'LST_Landsat_C'])
                    for _, row in ldf.iterrows():
                        d_str = str(row['date'])
                        if d_str in daily_pm and row['LST_Landsat_C'] > 10.0 and daily_pm[d_str] > 0:
                            records.append({
                                'station': reg,
                                'station_code': code,
                                'date': d_str,
                                'year': yr,
                                'NDVI': row['NDVI'],
                                'NDBI': row['NDBI'],
                                'NDWI': row['NDWI'],
                                'LST': row['LST_Landsat_C'],
                                'PM25': daily_pm[d_str]
                            })
                except Exception as e:
                    print(f"Error reading {lf}: {e}")
                    
    df = pd.DataFrame(records)
    print(f"Successfully loaded and aligned {len(df)} station-date observations.")
    return df

def run_models():
    df = load_data()
    features = ['NDVI', 'NDBI', 'NDWI', 'LST']
    X = df[features]
    y = df['PM25']
    
    results = []
    
    # 1. 5-Fold Cross Validation (Contemporaneous Spatial Evaluation)
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    cv_r2, cv_rmse, cv_mae = [], [], []
    for train_idx, test_idx in kf.split(X):
        X_tr, X_te = X.iloc[train_idx], X.iloc[test_idx]
        y_tr, y_te = y.iloc[train_idx], y.iloc[test_idx]
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        rf.fit(X_tr, y_tr)
        preds = rf.predict(X_te)
        cv_r2.append(r2_score(y_te, preds))
        cv_rmse.append(np.sqrt(mean_squared_error(y_te, preds)))
        cv_mae.append(mean_absolute_error(y_te, preds))
        
    results.append({
        'Model': 'Random Forest LUR (Conurbation-Wide)',
        'Validation_Design': '5-Fold Cross Validation (Contemporaneous)',
        'Train_N': int(len(X) * 0.8),
        'Test_N': int(len(X) * 0.2),
        'R2': np.mean(cv_r2),
        'RMSE': np.mean(cv_rmse),
        'MAE': np.mean(cv_mae),
        'Notes': 'High performance due to shared synoptic seasonality across stations'
    })
    
    # 2. Spatial Group Holdout (Leave-Stations-Out)
    gkf_s = GroupKFold(n_splits=5)
    s_r2, s_rmse, s_mae = [], [], []
    for tr_idx, te_idx in gkf_s.split(X, y, groups=df['station']):
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        rf.fit(X.iloc[tr_idx], y.iloc[tr_idx])
        preds = rf.predict(X.iloc[te_idx])
        s_r2.append(r2_score(y.iloc[te_idx], preds))
        s_rmse.append(np.sqrt(mean_squared_error(y.iloc[te_idx], preds)))
        s_mae.append(mean_absolute_error(y.iloc[te_idx], preds))
    results.append({
        'Model': 'Random Forest LUR (Conurbation-Wide)',
        'Validation_Design': 'Spatial Group Holdout (Leave-Stations-Out)',
        'Train_N': len(X),
        'Test_N': len(X),
        'R2': np.mean(s_r2),
        'RMSE': np.mean(s_rmse),
        'MAE': np.mean(s_mae),
        'Notes': 'True spatial generalization across independent monitoring stations'
    })

    # 3. Temporal Group Holdout (Leave-Dates-Out)
    gkf_t = GroupKFold(n_splits=5)
    t_r2, t_rmse, t_mae = [], [], []
    for tr_idx, te_idx in gkf_t.split(X, y, groups=df['date']):
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        rf.fit(X.iloc[tr_idx], y.iloc[tr_idx])
        preds = rf.predict(X.iloc[te_idx])
        t_r2.append(r2_score(y.iloc[te_idx], preds))
        t_rmse.append(np.sqrt(mean_squared_error(y.iloc[te_idx], preds)))
        t_mae.append(mean_absolute_error(y.iloc[te_idx], preds))
    results.append({
        'Model': 'Random Forest LUR (Conurbation-Wide)',
        'Validation_Design': 'Temporal GroupKFold (Leave-Dates-Out)',
        'Train_N': len(X),
        'Test_N': len(X),
        'R2': np.mean(t_r2),
        'RMSE': np.mean(t_rmse),
        'MAE': np.mean(t_mae),
        'Notes': 'Leave-dates-out cross-validation across independent overpass days'
    })
    
    # 4. Strict Temporal Split: Train 2024 -> Test 2025
    train_df = df[df['year'] == 2024]
    test_df = df[df['year'] == 2025]
    X_tr, y_tr = train_df[features], train_df['PM25']
    X_te, y_te = test_df[features], test_df['PM25']
    
    # A) RF Temporal
    rf_temp = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_temp.fit(X_tr, y_tr)
    preds_rf_temp = rf_temp.predict(X_te)
    results.append({
        'Model': 'Random Forest LUR (Conurbation-Wide)',
        'Validation_Design': 'Temporal Split (Train 2024 -> Test 2025)',
        'Train_N': len(train_df),
        'Test_N': len(test_df),
        'R2': r2_score(y_te, preds_rf_temp),
        'RMSE': np.sqrt(mean_squared_error(y_te, preds_rf_temp)),
        'MAE': mean_absolute_error(y_te, preds_rf_temp),
        'Notes': 'Out-of-year transferability benchmark; sensitive to annual baseline shift'
    })
    
    # B) OLS Temporal
    ols = LinearRegression()
    ols.fit(X_tr, y_tr)
    preds_ols = ols.predict(X_te)
    results.append({
        'Model': 'Linear Regression (OLS Baseline)',
        'Validation_Design': 'Temporal Split (Train 2024 -> Test 2025)',
        'Train_N': len(train_df),
        'Test_N': len(test_df),
        'R2': r2_score(y_te, preds_ols),
        'RMSE': np.sqrt(mean_squared_error(y_te, preds_ols)),
        'MAE': mean_absolute_error(y_te, preds_ols),
        'Notes': 'Parametric linear baseline under temporal transfer'
    })
    
    # C) SVR Temporal
    svr = SVR(kernel='rbf')
    svr.fit(X_tr, y_tr)
    preds_svr = svr.predict(X_te)
    results.append({
        'Model': 'Support Vector Regression (SVR)',
        'Validation_Design': 'Temporal Split (Train 2024 -> Test 2025)',
        'Train_N': len(train_df),
        'Test_N': len(test_df),
        'R2': r2_score(y_te, preds_svr),
        'RMSE': np.sqrt(mean_squared_error(y_te, preds_svr)),
        'MAE': mean_absolute_error(y_te, preds_svr),
        'Notes': 'Nonlinear support vector regressor under temporal transfer'
    })
    
    # Feature Importances from RF
    print("\nFeature Importances (Full Dataset RF):")
    rf_full = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_full.fit(X, y)
    for feat, imp in zip(features, rf_full.feature_importances_):
        print(f"  {feat:<6}: {imp*100.0:>6.2f}%")
        
    res_df = pd.DataFrame(results)
    os.makedirs(os.path.dirname(OUTPUT_METRICS_CSV), exist_ok=True)
    res_df.to_csv(OUTPUT_METRICS_CSV, index=False)
    data_out = os.path.join(script_dir, '../data/rf_lur_benchmark_metrics.csv')
    if os.path.exists(os.path.join(script_dir, '../data')):
        res_df.to_csv(data_out, index=False)
    print(f"\nSaved empirical model metrics to {OUTPUT_METRICS_CSV}")
    print(res_df[['Model', 'Validation_Design', 'R2', 'RMSE', 'MAE']])

if __name__ == "__main__":
    run_models()
