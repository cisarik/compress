"""Male generovane grayscale datasety bez externych kniznic."""

from __future__ import annotations

from dataclasses import dataclass
from random import Random


@dataclass(frozen=True)
class GrayImage:
    """Jednoducha grayscale reprezentacia obrazka."""

    name: str
    width: int
    height: int
    pixels: bytes


def make_gradient_image(width: int = 32, height: int = 32) -> GrayImage:
    """Vrati vodorovny gradient od ciernej po bielu."""

    pixels = bytes(
        _scale_255(x, max(1, width - 1))
        for _y in range(height)
        for x in range(width)
    )
    return _image("gradient", width, height, pixels)


def make_checker_image(width: int = 32, height: int = 32, block: int = 4) -> GrayImage:
    """Vrati sachovnicovy grayscale obrazok."""

    if block <= 0:
        raise ValueError("block must be positive")
    pixels = bytes(
        255 if ((x // block) + (y // block)) % 2 else 0
        for y in range(height)
        for x in range(width)
    )
    return _image("checker", width, height, pixels)


def make_diagonal_ramp_image(width: int = 32, height: int = 32) -> GrayImage:
    """Vrati diagonaly grayscale ramp."""

    scale = max(1, (width - 1) + (height - 1))
    pixels = bytes(
        _scale_255(x + y, scale)
        for y in range(height)
        for x in range(width)
    )
    return _image("diagonal_ramp", width, height, pixels)


def make_noise_image(width: int = 32, height: int = 32, seed: int = 1234) -> GrayImage:
    """Vrati deterministicky sumovy grayscale obrazok."""

    rng = Random(seed)
    pixels = bytes(rng.randrange(256) for _ in range(width * height))
    return _image("noise", width, height, pixels)


def get_image_dataset_names() -> list[str]:
    """Vrati stabilny zoznam mien obrazkovych datasetov."""

    return ["gradient", "checker", "diagonal_ramp", "noise"]


def make_image_dataset(name: str, width: int, height: int, seed: int = 1234) -> GrayImage:
    """Vytvori obrazok podla mena datasetu."""

    if name == "gradient":
        return make_gradient_image(width, height)
    if name == "checker":
        return make_checker_image(width, height)
    if name == "diagonal_ramp":
        return make_diagonal_ramp_image(width, height)
    if name == "noise":
        return make_noise_image(width, height, seed)
    raise ValueError(f"Unknown image dataset: {name}")


def _image(name: str, width: int, height: int, pixels: bytes) -> GrayImage:
    """Overi rozmery a vrati immutable objekt obrazka."""

    if width <= 0 or height <= 0:
        raise ValueError("width and height must be positive")
    if len(pixels) != width * height:
        raise ValueError("pixel count does not match image size")
    return GrayImage(name=name, width=width, height=height, pixels=pixels)


def _scale_255(value: int, max_value: int) -> int:
    """Preskaluje integer do rozsahu 0..255."""

    return (255 * value) // max_value
