"""Cestne placeholder implementacie pre buduce optimizery."""

from __future__ import annotations

from .base import OptimizerRequest, OptimizerResult


class PlaceholderOptimizer:
    """Jednoduchy neimplementovany optimizer s honest fallbackom."""

    def __init__(self, optimizer_name: str, explanation: str) -> None:
        self._optimizer_name = optimizer_name
        self._explanation = explanation

    def name(self) -> str:
        """Vrati registrovany nazov placeholdera."""

        return self._optimizer_name

    def available(self) -> bool:
        """Placeholder sa zobrazuje v GUI, ale nie je plne implementovany."""

        return False

    def run(self, request: OptimizerRequest) -> OptimizerResult:
        """Vrati honest raw fallback namiesto predstieranej optimalizacie."""

        raw_bits = len(request.data) * 8
        return OptimizerResult(
            optimizer_name=self._optimizer_name,
            status="not_implemented",
            best_model="raw_fallback",
            raw_bits=raw_bits,
            total_bits=raw_bits,
            saving_bits=0,
            ratio_vs_raw=1.0,
            history=[],
            details={
                "message": self._explanation,
                "experimental": True,
            },
        )


def make_gp_placeholder() -> PlaceholderOptimizer:
    """Vrati placeholder pre buduci bohaty geneticky program."""

    return PlaceholderOptimizer(
        "GP",
        "GP will later search richer expression trees and topologies beyond the current GP-lite branch.",
    )


def make_adam_placeholder() -> PlaceholderOptimizer:
    """Vrati placeholder pre buduci diferencovatelny optimizer."""

    return PlaceholderOptimizer(
        "ADAM",
        "ADAM will later tune differentiable continuous parameters once a suitable differentiable law family exists.",
    )
