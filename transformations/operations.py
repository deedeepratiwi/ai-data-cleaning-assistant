import pandas as pd


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
