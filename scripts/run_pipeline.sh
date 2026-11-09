#!/bin/bash
# Standalone execution wrapper for satellite verification and LUR modeling
PYTHON_EXE="/Users/saptarshisadhu/miniconda3/envs/EDA/bin/python"
if [ ! -f "$PYTHON_EXE" ]; then
    PYTHON_EXE="python3"
fi

echo "Executing remote_sensing_verification.py..."
$PYTHON_EXE "remote_sensing_verification.py"
echo "Executing rf_lur_spatial_temporal_model.py..."
$PYTHON_EXE "rf_lur_spatial_temporal_model.py"
echo "Executing test_numerical_verification.py..."
$PYTHON_EXE "test_numerical_verification.py"
echo "Execution finished with status: $?"
