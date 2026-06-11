"""Male deterministicke stromove anchor zakony pre indexovu vetvu."""

from __future__ import annotations

from dataclasses import dataclass

from .bitcost import bits_unsigned_range

_TERMINAL_MODEL_BITS = 3
_OPERATOR_MODEL_BITS = 5


@dataclass(frozen=True)
class LawNode:
    """Nemenny uzol maleho vyrazoveho stromu."""

    kind: str
    value: int | None = None
    left: "LawNode | None" = None
    right: "LawNode | None" = None


def idx_law() -> LawNode:
    """Vrati terminal reprezentujuci index i."""

    return LawNode("idx")


def const_law(value: int) -> LawNode:
    """Vrati konstantny terminal."""

    return LawNode("const", value=int(value))


def add_law(left: LawNode, right: LawNode) -> LawNode:
    """Vrati uzol scitania."""

    return LawNode("add", left=left, right=right)


def sub_law(left: LawNode, right: LawNode) -> LawNode:
    """Vrati uzol odcitania."""

    return LawNode("sub", left=left, right=right)


def mul_small_law(child: LawNode, factor: int) -> LawNode:
    """Vrati uzol nasobenia malou kladnou konstantou."""

    if factor <= 0:
        raise ValueError("factor must be positive")
    return LawNode("mul_small", value=int(factor), left=child)


def floordiv_pow2_law(child: LawNode, shift: int) -> LawNode:
    """Vrati uzol podlahoveho delenia mocninou dvojky."""

    if shift < 0 or shift > 8:
        raise ValueError("shift must be in range 0..8")
    return LawNode("floordiv_pow2", value=int(shift), left=child)


def square_law(child: LawNode) -> LawNode:
    """Vrati uzol druhej mocniny."""

    return LawNode("square", left=child)


def clamp_nonnegative_law(child: LawNode) -> LawNode:
    """Vrati uzol useknutia na nezaporny rozsah."""

    return LawNode("clamp_nonnegative", left=child)


def anchor_value(law: LawNode, index: int) -> int:
    """Vyhodnoti anchor zakon A(i) pre zadany index."""

    if index < 0:
        raise ValueError("index must be non-negative")

    if law.kind == "idx":
        return index
    if law.kind == "const":
        if law.value is None:
            raise ValueError("const node requires a value")
        return int(law.value)
    if law.kind == "add":
        return anchor_value(_require_child(law.left), index) + anchor_value(_require_child(law.right), index)
    if law.kind == "sub":
        return anchor_value(_require_child(law.left), index) - anchor_value(_require_child(law.right), index)
    if law.kind == "mul_small":
        if law.value is None:
            raise ValueError("mul_small node requires a factor")
        return anchor_value(_require_child(law.left), index) * int(law.value)
    if law.kind == "floordiv_pow2":
        if law.value is None:
            raise ValueError("floordiv_pow2 node requires a shift")
        return anchor_value(_require_child(law.left), index) // (1 << int(law.value))
    if law.kind == "square":
        value = anchor_value(_require_child(law.left), index)
        return value * value
    if law.kind == "clamp_nonnegative":
        return max(0, anchor_value(_require_child(law.left), index))
    raise ValueError(f"Unsupported law node kind: {law.kind}")


def law_model_bits(law: LawNode) -> int:
    """Vrati konzervativny odhad modelovej ceny stromu bez parametrov."""

    if law.kind in {"idx", "const"}:
        return _TERMINAL_MODEL_BITS
    if law.kind in {"add", "sub"}:
        return _OPERATOR_MODEL_BITS + law_model_bits(_require_child(law.left)) + law_model_bits(_require_child(law.right))
    if law.kind in {"mul_small", "floordiv_pow2", "square", "clamp_nonnegative"}:
        return _OPERATOR_MODEL_BITS + law_model_bits(_require_child(law.left))
    raise ValueError(f"Unsupported law node kind: {law.kind}")


def law_parameter_bits(law: LawNode) -> int:
    """Vrati konzervativny odhad ceny ciselnych parametrov stromu."""

    if law.kind == "idx":
        return 0
    if law.kind == "const":
        return _signed_int_bits(_require_value(law.value))
    if law.kind in {"add", "sub"}:
        return law_parameter_bits(_require_child(law.left)) + law_parameter_bits(_require_child(law.right))
    if law.kind == "mul_small":
        return bits_unsigned_range(_require_value(law.value)) + law_parameter_bits(_require_child(law.left))
    if law.kind == "floordiv_pow2":
        return bits_unsigned_range(_require_value(law.value)) + law_parameter_bits(_require_child(law.left))
    if law.kind in {"square", "clamp_nonnegative"}:
        return law_parameter_bits(_require_child(law.left))
    raise ValueError(f"Unsupported law node kind: {law.kind}")


def render_law(law: LawNode) -> str:
    """Vrati stabilnu citatelnu reprezentaciu anchor zakona."""

    if law.kind == "idx":
        return "idx"
    if law.kind == "const":
        return str(_require_value(law.value))
    if law.kind == "add":
        return f"add({render_law(_require_child(law.left))}, {render_law(_require_child(law.right))})"
    if law.kind == "sub":
        return f"sub({render_law(_require_child(law.left))}, {render_law(_require_child(law.right))})"
    if law.kind == "mul_small":
        return f"mul_small({render_law(_require_child(law.left))}, {_require_value(law.value)})"
    if law.kind == "floordiv_pow2":
        return f"floordiv_pow2({render_law(_require_child(law.left))}, {_require_value(law.value)})"
    if law.kind == "square":
        return f"square({render_law(_require_child(law.left))})"
    if law.kind == "clamp_nonnegative":
        return f"clamp_nonnegative({render_law(_require_child(law.left))})"
    raise ValueError(f"Unsupported law node kind: {law.kind}")


def _signed_int_bits(value: int) -> int:
    """Vrati konzervativny pocet bitov pre male cele cislo so znamienkom."""

    if value == 0:
        return 1
    return 1 + bits_unsigned_range(abs(value))


def _require_child(child: LawNode | None) -> LawNode:
    """Overi pritomnost potomka pre unary alebo binary uzol."""

    if child is None:
        raise ValueError("law node is missing a child")
    return child


def _require_value(value: int | None) -> int:
    """Overi pritomnost parametra v uzle."""

    if value is None:
        raise ValueError("law node is missing a value")
    return int(value)
