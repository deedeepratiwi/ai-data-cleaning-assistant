from transformations.registry import TRANSFORMATION_REGISTRY


def list_transformations(_: dict) -> dict:
    return {
        "available_transformations": list(TRANSFORMATION_REGISTRY.keys())
    }
