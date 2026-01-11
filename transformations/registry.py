from transformations.operations import (
    drop_null_rows,
    fill_nulls,
    cast_type,
    drop_column,
)


TRANSFORMATION_REGISTRY = {
    "drop_null_rows": drop_null_rows,
    "fill_nulls": fill_nulls,
    "cast_type": cast_type,
    "drop_column": drop_column,
}
