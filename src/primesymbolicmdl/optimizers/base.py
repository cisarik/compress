"""Zakladne typy pre spustanie optimizerov."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class OptimizerRequest:
    """Vstupne nastavenia jedneho optimalizacneho behu."""

    data: bytes
    width_bits: int
    seed: int
    population_size: int
    generations: int
    max_index: int | None
    strict_lower: bool


@dataclass(frozen=True)
class OptimizerResult:
    """Stabilne zhrnutie vysledku optimizera."""

    optimizer_name: str
    status: str
    best_model: str
    raw_bits: int
    total_bits: int
    saving_bits: int
    ratio_vs_raw: float
    history: list[dict]
    details: dict


class Optimizer(Protocol):
    """Minimalne rozhranie pre optimizer v registry."""

    def name(self) -> str:
        """Vrati stabilny nazov optimizera."""

    def available(self) -> bool:
        """Vrati pravdu iba pre realne implementovany optimizer."""

    def run(self, request: OptimizerRequest) -> OptimizerResult:
        """Spusti optimizer nad zadanymi bytmi."""
