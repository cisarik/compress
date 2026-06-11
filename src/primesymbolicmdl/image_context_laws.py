"""Male expression-tree prediktory nad 2D grayscale kontextom."""

from __future__ import annotations

from dataclasses import dataclass

from .bitcost import bits_unsigned_range

_TERMINAL_KINDS = (
    "col",
    "row",
    "left",
    "up",
    "up_left",
    "x_ramp",
    "y_ramp",
    "diag_ramp",
)
_NODE_KINDS = _TERMINAL_KINDS + (
    "const",
    "add",
    "sub",
    "avg",
    "gradient",
    "mul_small",
    "floordiv_pow2",
    "mod_const",
    "floordiv_const",
    "eq_const",
    "parity_byte",
    "checker_parity",
    "clamp_byte",
)
_NODE_KIND_BITS = bits_unsigned_range(len(_NODE_KINDS) - 1)
_MOD_DIV_CONST_VALUES = (2, 4, 8, 16)
_EQ_CONST_VALUES = tuple(range(17))
_CHECKER_BLOCKS = (1, 2, 4, 8, 16)


@dataclass(frozen=True)
class ImageLawNode:
    """Nemenny uzol maleho obrazkoveho expression stromu."""

    kind: str
    value: int | None = None
    children: tuple["ImageLawNode", ...] = ()


def terminal_law(name: str) -> ImageLawNode:
    """Vytvori terminal reprezentujuci decoder-znamy kontext."""

    law = ImageLawNode(str(name))
    _validate_law(law)
    return law


def const_law(value: int) -> ImageLawNode:
    """Vytvori konstantny terminal."""

    law = ImageLawNode("const", int(value))
    _validate_law(law)
    return law


def add_law(left: ImageLawNode, right: ImageLawNode) -> ImageLawNode:
    """Vytvori binarny sucet."""

    law = ImageLawNode("add", None, (left, right))
    _validate_law(law)
    return law


def sub_law(left: ImageLawNode, right: ImageLawNode) -> ImageLawNode:
    """Vytvori binarny rozdiel."""

    law = ImageLawNode("sub", None, (left, right))
    _validate_law(law)
    return law


def avg_law(left: ImageLawNode, right: ImageLawNode) -> ImageLawNode:
    """Vytvori celociselny priemer dvoch podstromov."""

    law = ImageLawNode("avg", None, (left, right))
    _validate_law(law)
    return law


def gradient_law(a: ImageLawNode, b: ImageLawNode, c: ImageLawNode) -> ImageLawNode:
    """Vytvori trojargumentovy gradient zakon a + b - c."""

    law = ImageLawNode("gradient", None, (a, b, c))
    _validate_law(law)
    return law


def mul_small_law(child: ImageLawNode, factor: int) -> ImageLawNode:
    """Vytvori male celociselne nasobenie."""

    law = ImageLawNode("mul_small", int(factor), (child,))
    _validate_law(law)
    return law


def floordiv_pow2_law(child: ImageLawNode, shift: int) -> ImageLawNode:
    """Vytvori floor delenie mocninou dvojky."""

    law = ImageLawNode("floordiv_pow2", int(shift), (child,))
    _validate_law(law)
    return law


def clamp_byte_law(child: ImageLawNode) -> ImageLawNode:
    """Vytvori explicitne byte clampnutie podstromu."""

    law = ImageLawNode("clamp_byte", None, (child,))
    _validate_law(law)
    return law


def mod_const_law(child: ImageLawNode, modulus: int) -> ImageLawNode:
    """Vytvori modulo uzol s malym pevnym delitelom."""

    law = ImageLawNode("mod_const", int(modulus), (child,))
    _validate_law(law)
    return law


def floordiv_const_law(child: ImageLawNode, divisor: int) -> ImageLawNode:
    """Vytvori floor delenie malou pevnou konstantou."""

    law = ImageLawNode("floordiv_const", int(divisor), (child,))
    _validate_law(law)
    return law


def eq_const_law(child: ImageLawNode, constant: int) -> ImageLawNode:
    """Vytvori porovnanie s malou konstantou vracajuce 0 alebo 255."""

    law = ImageLawNode("eq_const", int(constant), (child,))
    _validate_law(law)
    return law


def parity_byte_law(child: ImageLawNode) -> ImageLawNode:
    """Vytvori parity primitive vracajucu 0 alebo 255."""

    law = ImageLawNode("parity_byte", None, (child,))
    _validate_law(law)
    return law


def checker_parity_law(block: int) -> ImageLawNode:
    """Vytvori explicitnu checker primitive nad col a row kontextom."""

    law = ImageLawNode("checker_parity", int(block))
    _validate_law(law)
    return law


def evaluate_image_law(law: ImageLawNode, context: dict[str, int]) -> int:
    """Vyhodnoti zakon nad decoder-znamym kontextom a vrati byte predikciu."""

    _validate_law(law)
    raw_value = _evaluate_raw(law, context)
    return _clamp_byte(raw_value)


def render_image_law(law: ImageLawNode) -> str:
    """Vrati stabilnu citatelnu textualnu podobu zakona."""

    _validate_law(law)

    if law.kind in _TERMINAL_KINDS:
        return law.kind
    if law.kind == "const":
        return f"const({int(law.value or 0)})"
    if law.kind in {"add", "sub", "avg"}:
        left, right = law.children
        return f"{law.kind}({render_image_law(left)}, {render_image_law(right)})"
    if law.kind == "gradient":
        first, second, third = law.children
        return (
            "gradient("
            f"{render_image_law(first)}, "
            f"{render_image_law(second)}, "
            f"{render_image_law(third)})"
        )
    if law.kind == "mul_small":
        return f"mul_small({render_image_law(law.children[0])}, {int(law.value or 0)})"
    if law.kind == "floordiv_pow2":
        return f"floordiv_pow2({render_image_law(law.children[0])}, {int(law.value or 0)})"
    if law.kind == "mod_const":
        return f"mod_const({render_image_law(law.children[0])}, {int(law.value or 0)})"
    if law.kind == "floordiv_const":
        return f"floordiv_const({render_image_law(law.children[0])}, {int(law.value or 0)})"
    if law.kind == "eq_const":
        return f"eq_const({render_image_law(law.children[0])}, {int(law.value or 0)})"
    if law.kind == "parity_byte":
        return f"parity_byte({render_image_law(law.children[0])})"
    if law.kind == "checker_parity":
        return f"checker_parity(block={int(law.value or 0)})"
    if law.kind == "clamp_byte":
        return f"clamp_byte({render_image_law(law.children[0])})"
    raise ValueError(f"Unsupported image law kind: {law.kind}")


def image_law_model_bits(law: ImageLawNode) -> int:
    """Vrati konzervativnu modelovu cenu stromu bez jeho parametrov."""

    _validate_law(law)
    return sum(_NODE_KIND_BITS for _ in _iter_nodes(law))


def image_law_parameter_bits(law: ImageLawNode) -> int:
    """Vrati konzervativnu cenu vsetkych ciselnych parametrov stromu."""

    _validate_law(law)
    total = 0
    for node in _iter_nodes(law):
        if node.kind == "const":
            total += _signed_parameter_bits(int(node.value or 0))
        elif node.kind == "mul_small":
            total += _signed_parameter_bits(int(node.value or 0))
        elif node.kind == "floordiv_pow2":
            total += 1 if int(node.value or 0) == 0 else bits_unsigned_range(int(node.value or 0))
        elif node.kind in {"mod_const", "floordiv_const", "checker_parity"}:
            total += bits_unsigned_range(int(node.value or 0))
        elif node.kind == "eq_const":
            total += bits_unsigned_range(int(node.value or 0))
    return total


def serialize_image_law(law: ImageLawNode) -> dict:
    """Serializuje zakon do research dict payloadu."""

    _validate_law(law)
    return {
        "kind": law.kind,
        "value": law.value,
        "children": [serialize_image_law(child) for child in law.children],
    }


def deserialize_image_law(payload: dict) -> ImageLawNode:
    """Obnovi zakon zo serializovaneho dict payloadu."""

    if not isinstance(payload, dict):
        raise ValueError("image law payload must be a dict")
    kind = payload.get("kind")
    value = payload.get("value")
    children_payload = payload.get("children", [])
    if not isinstance(kind, str):
        raise ValueError("image law kind must be a string")
    if not isinstance(children_payload, list):
        raise ValueError("image law children must be a list")
    children = tuple(deserialize_image_law(child) for child in children_payload)
    law = ImageLawNode(kind, None if value is None else int(value), children)
    _validate_law(law)
    return law


def _evaluate_raw(law: ImageLawNode, context: dict[str, int]) -> int:
    """Vrati neorezanu hodnotu podstromu pred finalnym byte clampom."""

    if law.kind in _TERMINAL_KINDS:
        return _context_value(context, law.kind)
    if law.kind == "const":
        return int(law.value or 0)
    if law.kind == "add":
        return _evaluate_raw(law.children[0], context) + _evaluate_raw(law.children[1], context)
    if law.kind == "sub":
        return _evaluate_raw(law.children[0], context) - _evaluate_raw(law.children[1], context)
    if law.kind == "avg":
        return (_evaluate_raw(law.children[0], context) + _evaluate_raw(law.children[1], context)) // 2
    if law.kind == "gradient":
        return (
            _evaluate_raw(law.children[0], context)
            + _evaluate_raw(law.children[1], context)
            - _evaluate_raw(law.children[2], context)
        )
    if law.kind == "mul_small":
        return _evaluate_raw(law.children[0], context) * int(law.value or 0)
    if law.kind == "floordiv_pow2":
        return _evaluate_raw(law.children[0], context) // (1 << int(law.value or 0))
    if law.kind == "mod_const":
        return _evaluate_raw(law.children[0], context) % int(law.value or 0)
    if law.kind == "floordiv_const":
        return _evaluate_raw(law.children[0], context) // int(law.value or 0)
    if law.kind == "eq_const":
        return 255 if _evaluate_raw(law.children[0], context) == int(law.value or 0) else 0
    if law.kind == "parity_byte":
        return 255 if (_evaluate_raw(law.children[0], context) % 2) == 1 else 0
    if law.kind == "checker_parity":
        block = int(law.value or 0)
        col = _context_value(context, "col")
        row = _context_value(context, "row")
        return 255 if (((col // block) + (row // block)) % 2) else 0
    if law.kind == "clamp_byte":
        return _clamp_byte(_evaluate_raw(law.children[0], context))
    raise ValueError(f"Unsupported image law kind: {law.kind}")


def _context_value(context: dict[str, int], key: str) -> int:
    """Bezpecne vyberie integer zo vstupneho kontextu."""

    if key not in context:
        raise ValueError(f"Missing image context key: {key}")
    value = context[key]
    if not isinstance(value, int):
        raise ValueError(f"Image context value must be an integer: {key}")
    return int(value)


def _validate_law(law: ImageLawNode) -> None:
    """Overi aritu, kind aj parametre uzla."""

    if law.kind not in _NODE_KINDS:
        raise ValueError(f"Unsupported image law kind: {law.kind}")

    arity = len(law.children)
    if law.kind in _TERMINAL_KINDS:
        if law.value is not None or arity != 0:
            raise ValueError(f"Terminal {law.kind} must not have parameters or children")
        return
    if law.kind == "const":
        if not isinstance(law.value, int) or arity != 0:
            raise ValueError("const law requires an integer value and no children")
        return
    if law.kind in {"add", "sub", "avg"}:
        if law.value is not None or arity != 2:
            raise ValueError(f"{law.kind} requires exactly two children")
        return
    if law.kind == "gradient":
        if law.value is not None or arity != 3:
            raise ValueError("gradient requires exactly three children")
        return
    if law.kind == "mul_small":
        if not isinstance(law.value, int) or arity != 1:
            raise ValueError("mul_small requires one child and an integer factor")
        if int(law.value) < -4 or int(law.value) > 4:
            raise ValueError("mul_small factor must be in range -4..4")
        return
    if law.kind == "floordiv_pow2":
        if not isinstance(law.value, int) or arity != 1:
            raise ValueError("floordiv_pow2 requires one child and an integer shift")
        if int(law.value) < 0 or int(law.value) > 8:
            raise ValueError("floordiv_pow2 shift must be in range 0..8")
        return
    if law.kind == "mod_const":
        if not isinstance(law.value, int) or arity != 1:
            raise ValueError("mod_const requires one child and an integer modulus")
        if int(law.value) not in _MOD_DIV_CONST_VALUES:
            raise ValueError(f"mod_const modulus must be one of {_MOD_DIV_CONST_VALUES}")
        return
    if law.kind == "floordiv_const":
        if not isinstance(law.value, int) or arity != 1:
            raise ValueError("floordiv_const requires one child and an integer divisor")
        if int(law.value) not in _MOD_DIV_CONST_VALUES:
            raise ValueError(f"floordiv_const divisor must be one of {_MOD_DIV_CONST_VALUES}")
        return
    if law.kind == "eq_const":
        if not isinstance(law.value, int) or arity != 1:
            raise ValueError("eq_const requires one child and an integer constant")
        if int(law.value) not in _EQ_CONST_VALUES:
            raise ValueError(f"eq_const constant must be in range {_EQ_CONST_VALUES[0]}..{_EQ_CONST_VALUES[-1]}")
        return
    if law.kind == "parity_byte":
        if law.value is not None or arity != 1:
            raise ValueError("parity_byte requires exactly one child")
        return
    if law.kind == "checker_parity":
        if not isinstance(law.value, int) or arity != 0:
            raise ValueError("checker_parity requires a block parameter and no children")
        if int(law.value) not in _CHECKER_BLOCKS:
            raise ValueError(f"checker_parity block must be one of {_CHECKER_BLOCKS}")
        return
    if law.kind == "clamp_byte":
        if law.value is not None or arity != 1:
            raise ValueError("clamp_byte requires exactly one child")
        return


def _iter_nodes(law: ImageLawNode):
    """Prejde cely strom v preorder poradi."""

    yield law
    for child in law.children:
        yield from _iter_nodes(child)


def _signed_parameter_bits(value: int) -> int:
    """Vrati konzervativny pocet bitov pre jedno podpisane cele cislo."""

    if value == 0:
        return 1
    return 1 + bits_unsigned_range(abs(int(value)))


def _clamp_byte(value: int) -> int:
    """Oreze lubovolne cele cislo na grayscale rozsah 0..255."""

    return max(0, min(255, int(value)))
