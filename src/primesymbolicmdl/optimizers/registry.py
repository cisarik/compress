"""Registry optimizerov pouzitelnych v CLI aj GUI."""

from __future__ import annotations

from .base import OptimizerRequest, OptimizerResult
from .gplite_adapter import GPLiteOptimizer
from .image_gplite import ImageGPLiteOptimizer
from .image_predictor import ImagePredictorOptimizer
from .image_soma import ImageSomaOptimizer
from .placeholders import make_adam_placeholder, make_gp_placeholder
from .soma import SomaOptimizer

_OPTIMIZERS = {
    "GP-lite": GPLiteOptimizer(),
    "SOMA": SomaOptimizer(),
    "GP": make_gp_placeholder(),
    "ADAM": make_adam_placeholder(),
    "Image-predictor": ImagePredictorOptimizer(),
    "Image-GP-lite": ImageGPLiteOptimizer(),
    "Image-SOMA": ImageSomaOptimizer(),
}

_ORDER = ["GP-lite", "SOMA", "GP", "ADAM", "Image-predictor", "Image-GP-lite", "Image-SOMA"]


def get_optimizer_names() -> list[str]:
    """Vrati stabilny zoznam mien pre dropdown a CLI."""

    return list(_ORDER)


def get_optimizer(name: str):
    """Vrati optimizer registrovany pod zadanym menom."""

    try:
        return _OPTIMIZERS[name]
    except KeyError as exc:
        raise ValueError(f"Unknown optimizer: {name}") from exc


def run_optimizer(name: str, request: OptimizerRequest) -> OptimizerResult:
    """Spusti optimizer podla mena a vrati normalizovany vysledok."""

    return get_optimizer(name).run(request)
