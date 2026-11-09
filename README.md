# Coupling Satellite Remote Sensing and Ground-Based Monitoring: Built Environment Characteristics and Urban Air Quality across 13 Stations in Kolkata and Howrah

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Target: Building and Environment](https://img.shields.io/badge/Journal-Building%20and%20Environment%20(Elsevier%2C%20Q1)-0073B1.svg)](https://www.sciencedirect.com/journal/building-and-environment)

This repository contains the complete open-source reproducibility pipelines, quality-controlled datasets, satellite buffer extractions, and analysis scripts accompanying the research manuscript:

> **"Coupling Satellite Remote Sensing and Ground-Based Monitoring: Built Environment Characteristics and Urban Air Quality across 13 Stations in Kolkata and Howrah"**  
> **Author:** Saptarshi Sadhu (Sole Author)  
> **Affiliation:** School of Engineering and Technology, Adamas University, Kolkata 700126, West Bengal, India  
> **Correspondence:** `saptarshi1.sadhu@stu.adamasuniversity.ac.in` | `saptarshisadhuofficial@gmail.com`  
> **Target Journal:** *Building and Environment* (Elsevier, Q1, Impact Factor: 7.1, CiteScore: 12.8)

---

## 📌 Research Overview

Urban built environment characteristics---including land surface temperature (LST), vegetation canopy greenness, and surface imperviousness---substantially modulate localized air pollution dispersion across tropical South Asian megacities. This study couples **Landsat-8/9 Operational Land Imager (OLI)** and **Thermal Infrared Sensor (TIRS)** observations with ground-based **Continuous Ambient Air Quality Monitoring Systems (CAAQMS)** across 13 stations in the Kolkata–Howrah conurbation during 2024 and 2025 ($16.1 \times 10^{6}$ raw telemetry records; $N = 1,108$ aligned station-overpass observations).

### Core Scientific Contributions:
1. **Multi-Sensor Satellite Buffering:** Integrates 30 m Landsat-8/9 spectral indices (NDVI, NDBI, NDWI, LST) and Sentinel-5P TROPOMI tropospheric columns within 3 km radial footprints centered on statutory CAAQMS monitors.
2. **Simpson's Paradox Resolution:** Disentangles the spatiotemporal sign reversal between temporal seasonality (cool winter boundary-layer inversions causing negative LST vs. particulate slope) and cross-station spatial correlation (industrial heat and particulate co-emission creating positive spatial correlation, $r = +0.62$).
3. **Vegetative Buffering Threshold:** Identifies a non-linear threshold effect ($\text{NDVI} \ge 0.20$) where particulate mass drops markedly via source exclusion and aerodynamic separation, critically distinguishing spatial buffering from unrealistic dry deposition claims.
4. **Validation Leakage Benchmark:** Empirically demonstrates that contemporaneous random 5-fold cross-validation inflates predictive skill ($R^2 = 0.6790$) via conurbation-wide synoptic date leakage, whereas Spatial Group Holdout ($R^2 = 0.4059$) and chronological forward transfer ($2024 \to 2025$, $R^2 = 0.3177\text{--}0.3636$) reflect true out-of-sample generalization.

---

## 🗺️ Monitoring Network & Satellite Buffer Architecture (13 Stations)

| Code | Station Name | Bank | Latitude (°N) | Longitude (°E) | Elevation | Dominant Built Environment Archetype |
|:---:|:---|:---:|:---:|:---:|:---:|:---|
| **BG** | Ballygunge | East | 22.526°N | 88.369°E | 8 m | Compact mid-rise residential, dense street grid |
| **SVSPA** | Barrackpore | North | 22.766°N | 88.372°E | 11 m | Suburban mixed, open tree canopy, peri-urban |
| **BM** | Belur Math | West | 22.636°N | 88.352°E | 9 m | Riparian riverbank frontage, adjacent foundry belt |
| **BN** | Bidhannagar | East | 22.580°N | 88.433°E | 6 m | Planned commercial IT corridor, asphalt avenues |
| **BOG** | Botanical Garden | West | 22.559°N | 88.291°E | 7 m | Protected botanical garden, multi-layered canopy |
| **DN** | Dasnagar | West | 22.596°N | 88.312°E | 8 m | Heavy industrial foundry basin, unpaved roads |
| **FW** | Fort William | East | 22.553°N | 88.344°E | 9 m | Urban parkland (Maidan), dense grass & trees |
| **GH** | Ghusuri | West | 22.606°N | 88.351°E | 7 m | Heavy metal recycling, rerolling mills, freight |
| **JD** | Jadavpur | East | 22.499°N | 88.371°E | 7 m | University campus green patches, dense street canyons |
| **PP** | Padmapukur | West | 22.569°N | 88.312°E | 6 m | Water treatment works, open reservoirs, foundry proximity |
| **RBU** | Rabindra Bharati Univ. | East | 22.627°N | 88.377°E | 8 m | Heavy traffic intersection (BT Road), arterial diesel |
| **RS** | Rabindra Sarovar | East | 22.508°N | 88.358°E | 7 m | National lake system (73 ha), perimeter tree canopy |
| **VC** | Victoria Memorial | East | 22.544°N | 88.349°E | 8 m | Protected heritage memorial garden, urban parkland |

---

## 📁 Repository Directory Structure

```text
kolkata-howrah-satellite-built-environment/
├── README.md                                 <-- Master Documentation
├── LICENSE                                   <-- MIT License
├── requirements.txt                          <-- Python dependencies
├── .gitignore                                <-- Git exclusion filters
│
├── data/
│   ├── Cleaned_Station_Data/                 <-- 26 station-year CAAQMS telemetry workbooks (2024 & 2025)
│   ├── Remote_Sensing_Data/                  <-- Landsat-8/9 30 m buffer indices & Sentinel-5P CSVs
│   ├── rf_lur_benchmark_metrics.csv          <-- Empirical LUR validation metrics (4 paradigms)
│   ├── satellite_ground_reconciliation.csv   <-- Clean clear-sky satellite-ground comparison table
│   └── empirical_satellite_reconciliation.csv<-- Multi-sensor spectral and particulate dataset
│
├── figures/                                  <-- High-resolution publication figures (Fig 1 to Fig 8)
│   ├── fig1a_study_area_india.png
│   ├── fig1b_study_area_wb.png
│   ├── fig1c_study_area_stations.png
│   ├── fig2a_spatial_ndvi.png ... fig2d_spatial_ndwi.png
│   ├── fig3a_box_ndvi.png ... fig3d_box_pm25.png
│   ├── fig4a_regr_ndvi.png ... fig4c_regr_ndbi.png
│   ├── fig5a_binned_pm25.png, fig5b_binned_pm10.png
│   ├── fig6a_pdp_pm25.png, fig6b_pdp_o3.png
│   ├── fig7a_3d_interaction.png, fig7b_interaction_heatmap.png
│   └── fig8_lur_validation_benchmarks.png
│
└── scripts/                                  <-- Standalone reproduction pipelines
    ├── remote_sensing_verification.py        <-- Data extraction and multi-station reconciliation
    ├── rf_lur_spatial_temporal_model.py      <-- 4-way LUR validation benchmark execution
    ├── reconstruct_fig8.py                   <-- Generates validation benchmark & importance plots
    ├── generate_fig1c_buffer_map.py          <-- Generates 3 km buffer cartographic overview
    ├── test_numerical_verification.py        <-- Automated unit test suite (5/5 tests)
    └── run_pipeline.sh                       <-- Complete end-to-end execution script
```

---

## 🚀 Quickstart & Reproducibility Instructions

### 1. Environment Setup
```bash
git clone https://github.com/SAPTARSHI-coder/kolkata-howrah-satellite-built-environment.git
cd kolkata-howrah-satellite-built-environment
pip install -r requirements.txt
```

### 2. Run Remote Sensing Verification & Data Reconciliation
```bash
python scripts/remote_sensing_verification.py
```

### 3. Run Random Forest Land Use Regression (LUR) Benchmark
```bash
python scripts/rf_lur_spatial_temporal_model.py
```

### 4. Execute Complete Automated Validation Suite
```bash
python scripts/test_numerical_verification.py
```

---

## ⚖️ License & Citation

Distributed under the **MIT License**. See `LICENSE` for details.

If you utilize the datasets, buffer indices, or validation benchmarking code, please cite:
```bibtex
@article{sadhu2026satellite,
  title={Coupling Satellite Remote Sensing and Ground-Based Monitoring: Built Environment Characteristics and Urban Air Quality across 13 Stations in Kolkata and Howrah},
  author={Sadhu, Saptarshi},
  journal={Building and Environment},
  year={2026},
  publisher={Elsevier}
}
```
