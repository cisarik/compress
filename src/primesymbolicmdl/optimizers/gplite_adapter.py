"""Adapter medzi povodnym GP-lite searchom a registry optimizerov."""

from __future__ import annotations

from .base import OptimizerRequest, OptimizerResult
from ..law_search import search_best_law_for_bytes


class GPLiteOptimizer:
    """Tenký adapter pre existujuci stromovy GP-lite search."""

    def name(self) -> str:
        """Vrati stabilny nazov optimizera."""

        return "GP-lite"

    def available(self) -> bool:
        """GP-lite je plne dostupny v tomto repozitari."""

        return True

    def run(self, request: OptimizerRequest) -> OptimizerResult:
        """Spusti povodny GP-lite search a normalizuje vysledok."""

        result = search_best_law_for_bytes(
            request.data,
            width_bits=request.width_bits,
            seed=request.seed,
            population_size=request.population_size,
            generations=request.generations,
            max_index=request.max_index,
            strict_lower=request.strict_lower,
        )
        details = dict(result)
        details.pop("best_law", None)
        return OptimizerResult(
            optimizer_name=self.name(),
            status="ok",
            best_model=result["best_law_string"],
            raw_bits=result["raw_bits"],
            total_bits=result["total_bits"],
            saving_bits=result["saving_bits"],
            ratio_vs_raw=result["ratio_vs_raw"],
            history=result["history"],
            details=details,
        )
