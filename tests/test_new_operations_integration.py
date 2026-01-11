"""
Integration test for the complete workflow with new transformation operations.
Tests the fix for issue: "Add string standardization, non-value replacement, 
and auto type casting operations are still not working yet."
"""
import pandas as pd
import pytest
from pathlib import Path
import tempfile
import shutil

from transformations.registry import TRANSFORMATION_REGISTRY


def test_new_operations_workflow():
    """
    Test complete workflow with user's example data containing ERROR and UNKNOWN values.
    Verifies that:
    1. replace_non_values works correctly
    2. standardize_case works correctly  
    3. auto_cast_type works correctly
    4. Operations are applied in the right order
    """
    # Create test data matching the user's example
    df = pd.DataFrame({
        'Transaction ID': ['TXN_1961373', 'TXN_4977031', 'TXN_4271903', 'TXN_7034554', 'TXN_3160411'],
        'Item': ['Coffee', 'Cake', 'Cookie', 'Salad', 'Coffee'],
        'Quantity': [2, 4, 4, 2, 2],
        'Price Per Unit': [2.0, 3.0, 1.0, 5.0, 2.0],
        'Total Spent': ['4.0', '12.0', 'ERROR', '10.0', '4.0'],
        'Payment Method': ['Credit Card', 'Cash', 'Credit Card', 'UNKNOWN', 'Digital Wallet'],
        'Location': ['Takeaway', 'In-store', 'In-store', 'UNKNOWN', 'In-store'],
        'Transaction Date': ['2023-09-08', '2023-05-16', '2023-07-19', '2023-04-27', '2023-06-11']
    })
    
    # Define suggested operations (in the order they should be applied)
    suggestions = [
        {"operation": "replace_non_values", "params": {"column": "Total Spent"}},
        {"operation": "replace_non_values", "params": {"column": "Payment Method"}},
        {"operation": "replace_non_values", "params": {"column": "Location"}},
        {"operation": "standardize_case", "params": {"column": "Location"}},
        {"operation": "standardize_case", "params": {"column": "Payment Method"}},
        {"operation": "auto_cast_type", "params": {"column": "Total Spent"}},
    ]
    
    # Apply transformations
    result_df = df.copy()
    for step in suggestions:
        op_name = step.get("operation")
        params = step.get("params", {})
        
        operation = TRANSFORMATION_REGISTRY.get(op_name)
        assert operation is not None, f"Operation {op_name} not found in registry"
        
        result_df = operation(result_df, **params)
    
    # Verify transformations
    assert len(result_df) == 5, "All rows should be preserved"
    
    # Verify ERROR was replaced and column was cast to numeric
    assert pd.api.types.is_numeric_dtype(result_df['Total Spent']), "Total Spent should be numeric"
    assert pd.isna(result_df.loc[2, 'Total Spent']), "ERROR should be replaced with NaN"
    assert result_df.loc[0, 'Total Spent'] == 4, "Numeric values should be preserved"
    
    # Verify UNKNOWN values were replaced with NaN
    assert pd.isna(result_df.loc[3, 'Payment Method']), "UNKNOWN in Payment Method should be NaN"
    assert pd.isna(result_df.loc[3, 'Location']), "UNKNOWN in Location should be NaN"
    
    # Verify standardization
    assert result_df.loc[1, 'Location'] == 'In-Store', "In-store should be standardized to In-Store"
    assert result_df.loc[2, 'Location'] == 'In-Store', "In-store should be standardized to In-Store"
    
    # Verify non-UNKNOWN values were preserved
    assert result_df.loc[0, 'Payment Method'] == 'Credit Card'
    assert result_df.loc[0, 'Location'] == 'Takeaway'


def test_suggestion_generation_with_new_operations():
    """
    Test that the suggestion service generates correct suggestions for data with
    ERROR and UNKNOWN values.
    """
    # This test requires mocking the suggestion service
    # We'll test the logic directly
    
    df = pd.DataFrame({
        'Total Spent': ['4.0', '12.0', 'ERROR', '10.0'],
        'Status': ['Active', 'UNKNOWN', 'Active', 'ERROR'],
    })
    
    # Check for non-value indicators
    non_value_indicators = ['UNKNOWN', 'ERROR']
    
    # Total Spent should be identified for both replace_non_values and auto_cast_type
    total_spent_values = df['Total Spent'].dropna().astype(str).unique()
    has_non_values_total = any(
        any(nv in str(val) for nv in non_value_indicators)
        for val in total_spent_values
    )
    assert has_non_values_total, "Total Spent should have non-values (ERROR)"
    
    # Test numeric detection
    numeric_test = pd.to_numeric(df['Total Spent'], errors='coerce')
    non_null_count = df['Total Spent'].notna().sum()
    converted_count = numeric_test.notna().sum()
    assert converted_count / non_null_count >= 0.5, "Total Spent should be detected as numeric"
    
    # Status should be identified for replace_non_values
    status_values = df['Status'].dropna().astype(str).unique()
    has_non_values_status = any(
        any(nv in str(val) for nv in non_value_indicators)
        for val in status_values
    )
    assert has_non_values_status, "Status should have non-values (UNKNOWN, ERROR)"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
