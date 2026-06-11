"""Abstrakcie a registry optimizerov pre vyskumne behy."""

from .base import Optimizer, OptimizerRequest, OptimizerResult
from .registry import get_optimizer, get_optimizer_names, run_optimizer

__all__ = [
    "Optimizer",
    "OptimizerRequest",
    "OptimizerResult",
    "get_optimizer",
    "get_optimizer_names",
    "run_optimizer",
]
