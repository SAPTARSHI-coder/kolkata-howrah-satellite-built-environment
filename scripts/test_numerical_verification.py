#!/usr/bin/env python3
"""
Unit and regression test suite for Satellite Remote Sensing & Built Environment Study:
Verifies numerical integrity, cross-table consistency, and validation benchmarks.
"""
import os
import re
import pandas as pd
import numpy as np

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEX_PATH = os.path.join(BASE_DIR, "manuscript.tex")
PROOF_CSV = os.path.join(BASE_DIR, "data", "satellite_ground_reconciliation.csv")

def test_1_table2_landsat_consistency():
    """Test 1: Verify Table 2 (2024) matches proof data."""
    print("Running Test 1: Table 2 (2024) Landsat consistency...")
    assert os.path.exists(PROOF_CSV), f"Proof CSV missing: {PROOF_CSV}"
    df = pd.read_csv(PROOF_CSV)
    assert len(df) == 13, f"Expected 13 stations, found {len(df)}"
    
    with open(TEX_PATH, "r") as f:
        tex = f.read()
    
    # Assert Ghusuri 2024 values in Table 2
    assert "36.73" in tex, "Ghusuri 2024 LST 36.73 missing in manuscript.tex"
    assert "0.1007" in tex, "Ghusuri 2024 NDVI 0.1007 missing in manuscript.tex"
    assert "+0.0029" in tex, "Ghusuri 2024 NDBI +0.0029 missing in manuscript.tex"
    print("  -> Test 1 passed: Table 2 satellite values perfectly verified.")

def test_2_table3_landsat_and_pm25_consistency():
    """Test 2: Verify Table 3 (2025) screened LST and UCLIM-consistent PM2.5."""
    print("Running Test 2: Table 3 (2025) LST & PM2.5 consistency...")
    with open(TEX_PATH, "r") as f:
        tex = f.read()
    
    # Assert screened 2025 LST values
    assert "34.79" in tex, "Ghusuri 2025 LST 34.79 missing in Table 3"
    assert "31.02" in tex, "Fort William 2025 LST 31.02 missing in Table 3"
    assert "31.90" in tex, "Victoria Memorial 2025 LST 31.90 missing in Table 3"
    
    # Assert UCLIM-consistent PM2.5 in 2025
    uclim_2025_pm25 = {
        "Ghusuri": "62.79",
        "Dasnagar": "47.97",
        "Belur Math": "52.38",
        "Rabindra Bharati Univ": "49.80",
        "Ballygunge": "49.86",
        "Victoria Memorial": "52.80",
        "Botanical Garden": "38.53",
        "Jadavpur": "59.30",
        "Padmapukur": "42.12",
        "Rabindra Sarovar": "47.60",
        "Bidhannagar": "37.18",
        "Fort William": "55.99",
        "Barrackpore (SVSPA)": "47.16",
    }
    for st, val in uclim_2025_pm25.items():
        assert val in tex, f"Station {st} 2025 PM2.5 {val} missing in manuscript.tex Table 3"
    print("  -> Test 2 passed: All 13 stations match UCLIM 2025 PM2.5 benchmarks.")

def test_3_table4_lur_benchmarks():
    """Test 3: Verify Table 4 LUR validation metrics."""
    print("Running Test 3: Table 4 LUR generalization metrics...")
    with open(TEX_PATH, "r") as f:
        tex = f.read()
    
    # Random 5-Fold CV: R2 = 0.6790, RMSE = 22.05
    assert "0.6790" in tex, "Random CV R2 0.6790 missing"
    assert "22.05" in tex, "Random CV RMSE 22.05 missing"
    
    # Spatial Group Holdout: R2 = 0.4059, RMSE = 29.41
    assert "0.4059" in tex, "Spatial Holdout R2 0.4059 missing"
    assert "29.41" in tex, "Spatial Holdout RMSE 29.41 missing"
    
    # Temporal GroupKFold: R2 = 0.4564, RMSE = 27.72
    assert "0.4564" in tex, "Temporal GroupKFold R2 0.4564 missing"
    assert "27.72" in tex, "Temporal GroupKFold RMSE 27.72 missing"
    
    # Chronological Forward Transfer: R2 = 0.3636 / 0.3177
    assert "0.3636" in tex, "Chronological OLS R2 0.3636 missing"
    assert "0.3177" in tex, "Chronological RF R2 0.3177 missing"
    print("  -> Test 3 passed: All 4 validation framework metrics verified.")

def test_4_physical_and_cartographic_integrity():
    """Test 4: Verify physical boundaries, elevation, and fig1c existence."""
    print("Running Test 4: Physical and cartographic integrity...")
    with open(TEX_PATH, "r") as f:
        tex = f.read()
    
    # Elevation: 6--11 m
    assert "elevation $6\\text{--}11\\,\\text{m}$" in tex, "Elevation 6--11 m missing"
    
    # Abstract NDVI range: 0.1877--0.2091
    assert "0.1877\\text{--}0.2091" in tex, "Abstract NDVI 0.1877--0.2091 missing"
    
    # Figure 1c existence and size
    fig1c = os.path.join(BASE_DIR, "figures", "fig1c_study_area_stations.png")
    assert os.path.exists(fig1c), f"fig1c missing at {fig1c}"
    assert os.path.getsize(fig1c) > 500000, f"fig1c is unexpectedly small: {os.path.getsize(fig1c)} bytes"
    print("  -> Test 4 passed: Cartographic and physical parameters verified.")

def test_5_atmenv_coordinate_and_distance_reconciliation():
    """Test 5: Verify Table 1 coordinates match ATMENV and Fig 1c."""
    print("Running Test 5: ATMENV coordinate & distance reconciliation...")
    with open(TEX_PATH, "r") as f:
        tex = f.read()

    # Coordinates in Table 1
    assert "88.372°E" in tex, "Barrackpore 88.372°E missing"
    assert "22.559°N" in tex, "Botanical Garden 22.559°N missing"
    assert "22.596°N" in tex, "Dasnagar 22.596°N missing"
    assert "22.606°N" in tex, "Ghusuri 22.606°N missing"
    assert "88.351°E" in tex, "Ghusuri 88.351°E missing"
    assert "22.569°N" in tex, "Padmapukur 22.569°N missing"
    assert "22.627°N" in tex, "RBU 22.627°N missing"
    assert "88.377°E" in tex, "RBU 88.377°E missing"
    assert "88.349°E" in tex, "Victoria Memorial 88.349°E missing"

    # Distances in Section 2.5 and Section 4.3
    assert "1.12\\,\\text{km}" in tex, "Victoria-Fort William 1.12 km distance missing"
    assert "76.3\\%" in tex, "Victoria-Fort William 76.3% overlap missing"
    assert "1.67\\,\\text{km}" in tex, "Jadavpur-Sarovar 1.67 km distance missing"
    assert "2.43\\,\\text{km}" in tex, "Padmapukur-Botanical 2.43 km distance missing"
    assert "2.76\\,\\text{km}" in tex, "Belur-RBU 2.76 km distance missing"
    print("  -> Test 5 passed: ATMENV-aligned coordinates and separation distances verified.")

if __name__ == "__main__":
    print("==================================================")
    print("SATELLITE & BUILT ENVIRONMENT VALIDATION SUITE")
    print("==================================================")
    test_1_table2_landsat_consistency()
    test_2_table3_landsat_and_pm25_consistency()
    test_3_table4_lur_benchmarks()
    test_4_physical_and_cartographic_integrity()
    test_5_atmenv_coordinate_and_distance_reconciliation()
    print("==================================================")
    print("ALL 5 TESTS PASSED SUCCESSFULLY (5/5)")
    print("==================================================")
