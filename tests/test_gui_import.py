import importlib


def test_gui_module_imports_headlessly() -> None:
    module = importlib.import_module("primesymbolicmdl.gui")

    assert hasattr(module, "main")
    assert hasattr(module, "parse_optional_int")
