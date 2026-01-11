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


TRANSFORMATION_REGISTRY = {
    "drop_null_rows": drop_null_rows,
    "fill_nulls": fill_nulls,
    "cast_type": cast_type,
    "drop_column": drop_column,
    "standardize_case": standardize_case,
    "standardize_column_names": standardize_column_names,
    "replace_non_values": replace_non_values,
    "auto_cast_type": auto_cast_type,
}
