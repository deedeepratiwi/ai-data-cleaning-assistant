def generate_suggestions(payload: dict) -> dict:
    profiling = payload["profiling"]

    suggestions = []

    for col, stats in profiling["column_stats"].items():
        if stats["null_count"] > 0:
            suggestions.append(
                {
                    "operation": "fill_nulls",
                    "params": {
                        "column": col,
                        "value": 0,
                    },
                }
            )

    return {"suggestions": suggestions}
