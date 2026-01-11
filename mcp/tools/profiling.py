import pandas as pd


def run_profiling(payload: dict) -> dict:
    df = pd.DataFrame(payload["data"])

    column_stats = {
        col: {
            "null_count": int(df[col].isna().sum()),
            "dtype": str(df[col].dtype),
        }
        for col in df.columns
    }

    return {
        "row_count": len(df),
        "column_stats": column_stats,
    }
