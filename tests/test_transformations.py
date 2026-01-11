"""
Unit tests for data transformation operations
"""
import pandas as pd
import pytest
from transformations.operations import (
    drop_null_rows,
    fill_nulls,
    cast_type,
    drop_column
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
