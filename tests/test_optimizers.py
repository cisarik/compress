from primesymbolicmdl.optimizers import OptimizerRequest, get_optimizer_names, run_optimizer


def test_optimizer_registry_names_are_stable() -> None:
    assert get_optimizer_names() == ["GP-lite", "SOMA", "GP", "ADAM", "Image-predictor", "Image-GP-lite", "Image-SOMA"]


def test_can_run_gplite_optimizer_on_tiny_data() -> None:
    request = OptimizerRequest(
        data=b"\x00\x01\x02\x03",
        width_bits=8,
        seed=1234,
        population_size=8,
        generations=4,
        max_index=3,
        strict_lower=False,
    )
    result = run_optimizer("GP-lite", request)

    assert result.status == "ok"
    assert result.optimizer_name == "GP-lite"


def test_can_run_soma_optimizer_on_tiny_data() -> None:
    request = OptimizerRequest(
        data=b"\x00\x01\x02\x03",
        width_bits=8,
        seed=1234,
        population_size=8,
        generations=4,
        max_index=3,
        strict_lower=False,
    )
    result = run_optimizer("SOMA", request)

    assert result.status == "ok"
    assert result.optimizer_name == "SOMA"


def test_placeholders_return_not_implemented() -> None:
    request = OptimizerRequest(
        data=b"\x00\x01",
        width_bits=8,
        seed=1234,
        population_size=4,
        generations=2,
        max_index=1,
        strict_lower=False,
    )

    gp_result = run_optimizer("GP", request)
    adam_result = run_optimizer("ADAM", request)

    assert gp_result.status == "not_implemented"
    assert adam_result.status == "not_implemented"


def test_can_run_image_predictor_optimizer_on_tiny_image() -> None:
    request = OptimizerRequest(
        data=b"\x00\x40\x80\xc0",
        width_bits=8,
        seed=1234,
        population_size=8,
        generations=4,
        max_index=3,
        strict_lower=False,
        metadata={"image_width": 2, "image_height": 2, "dataset_name": "tiny"},
    )
    result = run_optimizer("Image-predictor", request)

    assert result.status == "ok"
    assert result.optimizer_name == "Image-predictor"


def test_can_run_image_gplite_optimizer_on_tiny_image() -> None:
    request = OptimizerRequest(
        data=b"\x00\x40\x80\xc0",
        width_bits=8,
        seed=1234,
        population_size=8,
        generations=4,
        max_index=3,
        strict_lower=False,
        metadata={"image_width": 2, "image_height": 2, "dataset_name": "tiny"},
    )
    result = run_optimizer("Image-GP-lite", request)

    assert result.status == "ok"
    assert result.optimizer_name == "Image-GP-lite"


def test_can_run_image_soma_optimizer_on_tiny_image() -> None:
    request = OptimizerRequest(
        data=b"\x00\x40\x80\xc0",
        width_bits=8,
        seed=1234,
        population_size=8,
        generations=4,
        max_index=3,
        strict_lower=False,
        metadata={"image_width": 2, "image_height": 2, "dataset_name": "tiny"},
    )
    result = run_optimizer("Image-SOMA", request)

    assert result.status == "ok"
    assert result.optimizer_name == "Image-SOMA"
