import pandas as pd
import numpy as np


def drop_null_rows(df: pd.DataFrame, column: str) -> pd.DataFrame:
    return df.dropna(subset=[column])


def fill_nulls(df: pd.DataFrame, column: str, value) -> pd.DataFrame:
    df[column] = df[column].fillna(value)
    return df


def cast_type(df: pd.DataFrame, column: str, dtype: str) -> pd.DataFrame:
    df[column] = df[column].astype(dtype, errors="ignore")
    return df


def drop_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    return df.drop(columns=[column], errors="ignore")


def _to_snake_case(text: str) -> str:
    """
    Helper function to convert text to lowercase snake_case.
    Removes trailing/leading spaces, converts spaces and hyphens to underscores.
    
    Args:
        text: String to convert
        
    Returns:
        Lowercase snake_case string
        
    Example:
        'In-store  ' -> 'in_store'
        'Credit Card' -> 'credit_card'
    """
    return text.strip().replace(' ', '_').replace('-', '_').lower()


def standardize_case(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Standardize string values to lowercase snake_case (e.g., 'In-store' -> 'in_store', 'Credit Card' -> 'credit_card').
    Also removes trailing spaces.
    Only affects non-null string values.
    """
    if column not in df.columns:
        return df
    
    # Only process if the column contains string-like values
    if df[column].dtype == 'object':
        df[column] = df[column].apply(
            lambda x: _to_snake_case(x) if isinstance(x, str) and pd.notna(x) else x
        )
    
    return df


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names to lowercase snake_case.
    Removes trailing spaces and converts spaces and hyphens to underscores.
    Example: 'Payment Method' -> 'payment_method', 'Total-Spent' -> 'total_spent'
    """
    df.columns = [_to_snake_case(col) for col in df.columns]
    return df


def replace_non_values(df: pd.DataFrame, column: str, non_values: list = None) -> pd.DataFrame:
    """
    Replace non-value strings (like 'UNKNOWN', 'ERROR', 'N/A', etc.) with NaN.
    
    Args:
        df: DataFrame to modify
        column: Column name to process
        non_values: List of strings to treat as non-values. If None, uses default list.
    
    Note:
        Default list includes empty strings ('') and whitespace (' ') as non-values.
        If your data legitimately uses these, provide a custom non_values list.
    """
    if column not in df.columns:
        return df
    
    # Default list of common non-value indicators
    if non_values is None:
        non_values = [
            'UNKNOWN', 'unknown', 'Unknown',
            'ERROR', 'error', 'Error',
            'N/A', 'n/a', 'NA', 'na',
            'NULL', 'null', 'Null',
            'NONE', 'none', 'None',
            'NIL', 'nil', 'Nil',
            '-', '--', '---',
            '', ' '
        ]
    
    # Replace non-values with NaN
    df[column] = df[column].replace(non_values, np.nan)
    
    return df


def auto_cast_type(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Automatically detect and cast column type if it contains numeric values stored as strings.
    Tries to cast to int first, then float, otherwise leaves as is.
    
    Note:
        Uses pandas nullable integer type (Int64) which requires pandas >= 1.0.0
    """
    if column not in df.columns:
        return df
    
    # Only process object (string) columns
    if df[column].dtype != 'object':
        return df
    
    # Create a copy of non-null values for testing
    non_null_values = df[column].dropna()
    
    if len(non_null_values) == 0:
        return df
    
    # Try to convert to numeric
    try:
        # Attempt to convert to numeric
        numeric_values = pd.to_numeric(non_null_values, errors='coerce')
        
        # Check if all non-null values were successfully converted
        if numeric_values.notna().all():
            # Check if all values are integers
            if (numeric_values % 1 == 0).all():
                df[column] = pd.to_numeric(df[column], errors='coerce').astype('Int64')
            else:
                df[column] = pd.to_numeric(df[column], errors='coerce')
    except (ValueError, TypeError):
        # If conversion fails due to type issues, leave as is
        pass
    
    return df


def auto_cast_datetime(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Automatically detect and cast column type if it contains date/datetime values stored as strings.
    Attempts to parse various date formats and convert to datetime64[ns].
    
    Args:
        df: DataFrame to process
        column: Column name to process
    
    Returns:
        DataFrame with column cast to datetime if successful, otherwise unchanged
    
    Note:
        Uses pandas to_datetime for flexible parsing.
        Handles common date formats like:
        - 2023-01-15, 2023/01/15
        - 01-15-2023, 01/15/2023
        - 15-Jan-2023, Jan 15, 2023
        - ISO 8601 formats
    """
    if column not in df.columns:
        return df
    
    # Only process object (string) columns
    if df[column].dtype != 'object':
        return df
    
    # Create a copy of non-null values for testing
    non_null_values = df[column].dropna()
    
    if len(non_null_values) == 0:
        return df
    
    # Try to convert to datetime
    try:
        # Test conversion on non-null values
        test_conversion = pd.to_datetime(non_null_values, errors='coerce')
        
        # Check if at least 80% of non-null values were successfully converted
        # (some flexibility for mixed content)
        success_rate = test_conversion.notna().sum() / len(test_conversion)
        
        if success_rate >= 0.8:
            # Convert the entire column
            df[column] = pd.to_datetime(df[column], errors='coerce')
    except (ValueError, TypeError, Exception):
        # If conversion fails, leave as is
        pass
    
    return df
