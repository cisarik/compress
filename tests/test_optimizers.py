from primesymbolicmdl.optimizers import OptimizerRequest, get_optimizer_names, run_optimizer


def test_optimizer_registry_names_are_stable() -> None:
    assert get_optimizer_names() == ["GP-lite", "SOMA", "GP", "ADAM"]


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
