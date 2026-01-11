import pandas as pd


def apply_transformations(df: pd.DataFrame, suggestions: list[dict]) -> pd.DataFrame:
    """
    Apply cleaning transformations based on suggestions.

    Expected suggestion format:
    {
      "type": "drop_nulls" | "fill_nulls" | "cast_type" | "drop_column",
      "column": "col_name",
      "value": optional
    }
    """

    for s in suggestions:
        action = s.get("type")
        col = s.get("column")

        if action == "drop_nulls" and col in df.columns:
            df = df[df[col].notna()]

        elif action == "fill_nulls" and col in df.columns:
            df[col] = df[col].fillna(s.get("value"))

        elif action == "cast_type" and col in df.columns:
            try:
                df[col] = df[col].astype(s.get("value"))
            except Exception:
                pass  # safe failure

        elif action == "drop_column" and col in df.columns:
            df = df.drop(columns=[col])

    return df
