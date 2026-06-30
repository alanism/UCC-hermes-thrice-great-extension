import importlib

import pytest


def require_product_module(module_name: str, missing_code: str):
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError as exc:
        expected_root = module_name.split(".", 1)[0]
        if exc.name == expected_root or str(exc.name).startswith(expected_root + "."):
            missing_expected_module = True
        else:
            raise
    if missing_expected_module:
        pytest.fail(
            f"{missing_code}: expected production module {module_name} does not exist yet",
            pytrace=False,
        )
