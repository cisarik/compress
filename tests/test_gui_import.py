import importlib

from primesymbolicmdl.optimizers.image_gplite import available_image_gplite_primitive_sets


def test_gui_module_imports_headlessly() -> None:
    module = importlib.import_module("primesymbolicmdl.gui")

    assert hasattr(module, "main")
    assert hasattr(module, "parse_optional_int")


def test_gui_registry_names_include_image_aware_optimizers() -> None:
    module = importlib.import_module("primesymbolicmdl.gui")
    names = module.get_optimizer_names()

    assert "Image-GP-lite" in names
    assert "Image-SOMA" in names


def test_gui_supports_image_gplite_primitive_set_choices() -> None:
    assert available_image_gplite_primitive_sets() == ["local", "ramp", "structure", "full"]
