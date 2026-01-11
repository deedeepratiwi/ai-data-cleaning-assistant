"""
Unit tests for data transformation operations
"""
import pandas as pd
import numpy as np
import pytest
from transformations.operations import (
    drop_null_rows,
    fill_nulls,
    cast_type,
    drop_column,
    standardize_case,
    standardize_column_names,
    replace_non_values,
    auto_cast_type,
)


def test_drop_null_rows():
    """Test dropping rows with null values in specific column"""
    df = pd.DataFrame({
        'name': ['Alice', None, 'Charlie'],
        'age': [25, 30, 35]
    })
    
    result = drop_null_rows(df, 'name')
    
    assert len(result) == 2
    assert 'Alice' in result['name'].values
    assert 'Charlie' in result['name'].values


def test_fill_nulls():
    """Test filling null values with a specific value"""
    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, None, 35]
    })
    
    result = fill_nulls(df, 'age', 0)
    
    assert result['age'].isna().sum() == 0
    assert result['age'].iloc[1] == 0


def test_cast_type():
    """Test casting column to different type"""
    df = pd.DataFrame({
        'age': ['25', '30', '35']
    })
    
    result = cast_type(df, 'age', 'int64')
    
    assert result['age'].dtype == 'int64'
    assert result['age'].iloc[0] == 25


def test_cast_type_with_invalid_data():
    """Test casting with invalid data (should handle gracefully)"""
    df = pd.DataFrame({
        'age': ['25', 'invalid', '35']
    })
    
    # Should not raise an error due to errors='ignore'
    result = cast_type(df, 'age', 'int64')
    
    # Type should remain as object due to invalid data
    assert result['age'].dtype == 'object'


def test_drop_column():
    """Test dropping a column"""
    df = pd.DataFrame({
        'name': ['Alice', 'Bob'],
        'age': [25, 30],
        'city': ['NYC', 'LA']
    })
    
    result = drop_column(df, 'city')
    
    assert 'city' not in result.columns
    assert 'name' in result.columns
    assert 'age' in result.columns


def test_drop_nonexistent_column():
    """Test dropping a column that doesn't exist (should handle gracefully)"""
    df = pd.DataFrame({
        'name': ['Alice', 'Bob'],
        'age': [25, 30]
    })
    
    # Should not raise an error due to errors='ignore'
    result = drop_column(df, 'nonexistent')
    
    assert len(result.columns) == 2
    assert 'name' in result.columns


def test_multiple_transformations():
    """Test chaining multiple transformations"""
    df = pd.DataFrame({
        'name': ['Alice', None, 'Charlie', 'David'],
        'age': [25, None, 35, 40],
        'city': ['NYC', 'LA', None, 'Boston'],
        'temp_col': [1, 2, 3, 4]
    })
    
    # Drop rows with null names
    df = drop_null_rows(df, 'name')
    
    # Fill null ages
    df = fill_nulls(df, 'age', 0)
    
    # Fill null cities
    df = fill_nulls(df, 'city', 'Unknown')
    
    # Drop temp column
    df = drop_column(df, 'temp_col')
    
    assert len(df) == 3  # One row with null name was dropped
    assert df['age'].isna().sum() == 0
    assert df['city'].isna().sum() == 0
    assert 'temp_col' not in df.columns


if __name__ == '__main__':
    pytest.main([__file__, '-v'])


# Tests for new operations


def test_standardize_case():
    """Test standardizing string values to lowercase snake_case"""
    df = pd.DataFrame({
        'order_type': ['Takeaway', 'In-store', 'DELIVERY', 'in-store', 'TakeAway']
    })
    
    result = standardize_case(df, 'order_type')
    
    assert result['order_type'].iloc[0] == 'takeaway'
    assert result['order_type'].iloc[1] == 'in_store'
    assert result['order_type'].iloc[2] == 'delivery'
    assert result['order_type'].iloc[3] == 'in_store'
    assert result['order_type'].iloc[4] == 'takeaway'


def test_standardize_case_with_nulls():
    """Test standardizing case preserves null values"""
    df = pd.DataFrame({
        'order_type': ['Takeaway', None, 'DELIVERY', np.nan, 'in-store']
    })
    
    result = standardize_case(df, 'order_type')
    
    assert result['order_type'].iloc[0] == 'takeaway'
    assert pd.isna(result['order_type'].iloc[1])
    assert result['order_type'].iloc[2] == 'delivery'
    assert pd.isna(result['order_type'].iloc[3])
    assert result['order_type'].iloc[4] == 'in_store'


def test_standardize_case_nonexistent_column():
    """Test standardizing case on nonexistent column"""
    df = pd.DataFrame({
        'name': ['Alice', 'Bob']
    })
    
    result = standardize_case(df, 'nonexistent')
    
    # Should return unchanged dataframe
    assert len(result.columns) == 1
    assert 'name' in result.columns


def test_replace_non_values():
    """Test replacing non-value strings with NaN"""
    df = pd.DataFrame({
        'status': ['Active', 'UNKNOWN', 'Inactive', 'ERROR', 'N/A', 'Active']
    })
    
    result = replace_non_values(df, 'status')
    
    assert result['status'].iloc[0] == 'Active'
    assert pd.isna(result['status'].iloc[1])
    assert result['status'].iloc[2] == 'Inactive'
    assert pd.isna(result['status'].iloc[3])
    assert pd.isna(result['status'].iloc[4])
    assert result['status'].iloc[5] == 'Active'


def test_replace_non_values_custom_list():
    """Test replacing non-values with custom list"""
    df = pd.DataFrame({
        'status': ['Valid', 'INVALID', 'Valid', 'MISSING']
    })
    
    result = replace_non_values(df, 'status', non_values=['INVALID', 'MISSING'])
    
    assert result['status'].iloc[0] == 'Valid'
    assert pd.isna(result['status'].iloc[1])
    assert result['status'].iloc[2] == 'Valid'
    assert pd.isna(result['status'].iloc[3])


def test_replace_non_values_example_from_issue():
    """Test the exact example from the issue"""
    df = pd.DataFrame({
        'order_type': ['Takeaway', 'In-store', 'UNKNOWN', np.nan, 'ERROR']
    })
    
    result = replace_non_values(df, 'order_type')
    
    assert result['order_type'].iloc[0] == 'Takeaway'
    assert result['order_type'].iloc[1] == 'In-store'
    assert pd.isna(result['order_type'].iloc[2])  # UNKNOWN -> NaN
    assert pd.isna(result['order_type'].iloc[3])  # already NaN
    assert pd.isna(result['order_type'].iloc[4])  # ERROR -> NaN


def test_auto_cast_type_integer():
    """Test auto-casting string column with integer values"""
    df = pd.DataFrame({
        'quantity': ['5', '10', '15', '20']
    })
    
    result = auto_cast_type(df, 'quantity')
    
    assert pd.api.types.is_integer_dtype(result['quantity'].dtype)
    assert result['quantity'].iloc[0] == 5
    assert result['quantity'].iloc[3] == 20


def test_auto_cast_type_float():
    """Test auto-casting string column with float values"""
    df = pd.DataFrame({
        'price': ['19.99', '29.99', '39.50', '49.00']
    })
    
    result = auto_cast_type(df, 'price')
    
    assert pd.api.types.is_numeric_dtype(result['price'].dtype)
    assert result['price'].iloc[0] == 19.99
    assert result['price'].iloc[3] == 49.00


def test_auto_cast_type_with_nulls():
    """Test auto-casting with null values"""
    df = pd.DataFrame({
        'quantity': ['5', None, '15', '20']
    })
    
    result = auto_cast_type(df, 'quantity')
    
    assert pd.api.types.is_integer_dtype(result['quantity'].dtype)
    assert result['quantity'].iloc[0] == 5
    assert pd.isna(result['quantity'].iloc[1])
    assert result['quantity'].iloc[2] == 15


def test_auto_cast_type_mixed_data():
    """Test auto-casting doesn't convert when data is truly mixed"""
    df = pd.DataFrame({
        'status': ['Active', 'Inactive', 'Pending']
    })
    
    result = auto_cast_type(df, 'status')
    
    # Should remain as object type
    assert result['status'].dtype == 'object'
    assert result['status'].iloc[0] == 'Active'


def test_auto_cast_type_already_numeric():
    """Test auto-casting on already numeric column"""
    df = pd.DataFrame({
        'age': [25, 30, 35]
    })
    
    result = auto_cast_type(df, 'age')
    
    # Should remain unchanged
    assert pd.api.types.is_numeric_dtype(result['age'].dtype)
    assert result['age'].iloc[0] == 25


def test_combined_standardize_and_replace():
    """Test combining standardize_case and replace_non_values operations"""
    df = pd.DataFrame({
        'order_type': ['Takeaway', 'In-store', 'UNKNOWN', np.nan, 'ERROR', 'delivery']
    })
    
    # First replace non-values
    result = replace_non_values(df, 'order_type')
    # Then standardize case
    result = standardize_case(result, 'order_type')
    
    assert result['order_type'].iloc[0] == 'takeaway'
    assert result['order_type'].iloc[1] == 'in_store'
    assert pd.isna(result['order_type'].iloc[2])  # UNKNOWN -> NaN
    assert pd.isna(result['order_type'].iloc[3])  # already NaN
    assert pd.isna(result['order_type'].iloc[4])  # ERROR -> NaN
    assert result['order_type'].iloc[5] == 'delivery'


def test_full_workflow():
    """Test complete workflow with all new operations"""
    df = pd.DataFrame({
        'product': ['laptop', 'MOUSE', 'keyboard', 'UNKNOWN'],
        'price': ['999.99', '29.99', '79.99', '199.99'],
        'quantity': ['5', '10', 'N/A', '8']
    })
    
    # Replace non-values in quantity
    df = replace_non_values(df, 'quantity')
    
    # Standardize product names
    df = standardize_case(df, 'product')
    
    # Auto-cast numeric columns
    df = auto_cast_type(df, 'price')
    df = auto_cast_type(df, 'quantity')
    
    # Verify results
    assert df['product'].iloc[0] == 'laptop'
    assert df['product'].iloc[1] == 'mouse'
    assert df['product'].iloc[3] == 'unknown'  # UNKNOWN is a valid product name after standardization
    
    assert pd.api.types.is_numeric_dtype(df['price'].dtype)
    assert df['price'].iloc[0] == 999.99
    
    assert pd.api.types.is_integer_dtype(df['quantity'].dtype)
    assert df['quantity'].iloc[0] == 5
    assert pd.isna(df['quantity'].iloc[2])  # N/A was replaced with NaN


def test_standardize_case_with_trailing_spaces():
    """Test that standardize_case removes trailing spaces"""
    df = pd.DataFrame({
        'location': ['New York  ', '  Los Angeles', ' Chicago ', 'Boston']
    })
    
    result = standardize_case(df, 'location')
    
    assert result['location'].iloc[0] == 'new_york'
    assert result['location'].iloc[1] == 'los_angeles'
    assert result['location'].iloc[2] == 'chicago'
    assert result['location'].iloc[3] == 'boston'


def test_standardize_column_names():
    """Test standardizing column names to lowercase snake_case"""
    df = pd.DataFrame({
        'Transaction ID': [1, 2, 3],
        'Payment Method': ['Cash', 'Card', 'Digital'],
        'Total-Spent': [10.0, 20.0, 30.0],
        'Customer Name  ': ['Alice', 'Bob', 'Charlie']  # with trailing spaces
    })
    
    result = standardize_column_names(df)
    
    assert 'transaction_id' in result.columns
    assert 'payment_method' in result.columns
    assert 'total_spent' in result.columns
    assert 'customer_name' in result.columns
    assert 'Transaction ID' not in result.columns
    assert 'Payment Method' not in result.columns
