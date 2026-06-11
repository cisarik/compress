"""Jednoduchy Tkinter cockpit pre male vyskumne simulacie."""

from __future__ import annotations

from dataclasses import dataclass

from .image_datasets import GrayImage, get_image_dataset_names, make_image_dataset
from .optimizers.registry import get_optimizer_names
from .simulation import format_simulation_report, run_image_simulation


def tkinter_available() -> bool:
    """Vrati pravdu iba ak je Tkinter importovatelny."""

    try:
        import tkinter  # noqa: F401
    except ModuleNotFoundError:
        return False
    return True


def parse_optional_int(text: str) -> int | None:
    """Prevedie prazdny string na None a inak vrati int."""

    stripped = text.strip()
    if not stripped:
        return None
    return int(stripped)


def parse_positive_int(text: str) -> int:
    """Vrati kladne cele cislo alebo vyhodi chybu."""

    value = int(text.strip())
    if value <= 0:
        raise ValueError("value must be positive")
    return value


def ensure_tkinter():
    """Importuje Tkinter az pri manualnom spusteni GUI."""

    try:
        import tkinter as tk
        from tkinter import messagebox, ttk
    except ModuleNotFoundError as exc:
        raise RuntimeError("Tkinter is unavailable; install the system package 'tk'.") from exc
    return tk, ttk, messagebox


@dataclass
class _GuiState:
    """Pomocny kontajner pre parsed vstupy z formulára."""

    optimizer_name: str
    dataset_name: str
    image_width: int
    image_height: int
    seed: int
    population_size: int
    generations: int
    max_index: int | None
    strict_lower: bool


class ResearchCockpit:
    """Jednoduche synchronne GUI pre prve porovnania optimizerov."""

    def __init__(self) -> None:
        tk, ttk, messagebox = ensure_tkinter()
        self._tk = tk
        self._ttk = ttk
        self._messagebox = messagebox
        self.root = tk.Tk()
        self.root.title("PrimeSymbolicMDL Research Cockpit")

        self.optimizer_var = tk.StringVar(value=get_optimizer_names()[0])
        self.dataset_var = tk.StringVar(value=get_image_dataset_names()[0])
        self.width_var = tk.StringVar(value="32")
        self.height_var = tk.StringVar(value="32")
        self.seed_var = tk.StringVar(value="1234")
        self.population_var = tk.StringVar(value="24")
        self.generations_var = tk.StringVar(value="12")
        self.max_index_var = tk.StringVar(value="31")
        self.strict_lower_var = tk.BooleanVar(value=False)

        self.canvas = tk.Canvas(self.root, width=128, height=128, bg="white", highlightthickness=1)
        self.output = tk.Text(self.root, width=72, height=18, wrap="word")
        self._build_layout()
        self._refresh_preview()

    def run(self) -> None:
        """Spusti Tkinter event loop."""

        self.root.mainloop()

    def _build_layout(self) -> None:
        """Postavi jednoduchy formular, canvas a textovy vystup."""

        frame = self._ttk.Frame(self.root, padding=12)
        frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        controls = [
            ("Optimizer", self._ttk.Combobox(frame, textvariable=self.optimizer_var, values=get_optimizer_names(), state="readonly")),
            ("Dataset", self._ttk.Combobox(frame, textvariable=self.dataset_var, values=get_image_dataset_names(), state="readonly")),
            ("Width", self._ttk.Entry(frame, textvariable=self.width_var)),
            ("Height", self._ttk.Entry(frame, textvariable=self.height_var)),
            ("Seed", self._ttk.Entry(frame, textvariable=self.seed_var)),
            ("Population", self._ttk.Entry(frame, textvariable=self.population_var)),
            ("Generations", self._ttk.Entry(frame, textvariable=self.generations_var)),
            ("Max index", self._ttk.Entry(frame, textvariable=self.max_index_var)),
        ]

        for row, (label, widget) in enumerate(controls):
            self._ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w", padx=(0, 8), pady=4)
            widget.grid(row=row, column=1, sticky="ew", pady=4)

        frame.columnconfigure(1, weight=1)

        strict_box = self._ttk.Checkbutton(frame, text="Strict lower anchor", variable=self.strict_lower_var)
        strict_box.grid(row=len(controls), column=0, columnspan=2, sticky="w", pady=(8, 8))

        button_row = len(controls) + 1
        self._ttk.Button(frame, text="Run simulation", command=self._run_simulation).grid(row=button_row, column=0, sticky="w", pady=(0, 8))
        self._ttk.Button(frame, text="Refresh preview", command=self._refresh_preview).grid(row=button_row, column=1, sticky="e", pady=(0, 8))

        self.canvas.grid(row=0, column=2, rowspan=button_row + 1, padx=(16, 0), sticky="n")
        self.output.grid(row=button_row + 1, column=0, columnspan=3, sticky="nsew", pady=(8, 0))
        frame.rowconfigure(button_row + 1, weight=1)

    def _parse_state(self) -> _GuiState:
        """Nacita a validuje hodnoty z formulára."""

        return _GuiState(
            optimizer_name=self.optimizer_var.get(),
            dataset_name=self.dataset_var.get(),
            image_width=parse_positive_int(self.width_var.get()),
            image_height=parse_positive_int(self.height_var.get()),
            seed=int(self.seed_var.get().strip()),
            population_size=parse_positive_int(self.population_var.get()),
            generations=parse_positive_int(self.generations_var.get()),
            max_index=parse_optional_int(self.max_index_var.get()),
            strict_lower=bool(self.strict_lower_var.get()),
        )

    def _run_simulation(self) -> None:
        """Spusti vybranu simulaciu a vypise textovy report."""

        try:
            state = self._parse_state()
            result = run_image_simulation(
                state.optimizer_name,
                dataset_name=state.dataset_name,
                image_width=state.image_width,
                image_height=state.image_height,
                seed=state.seed,
                population_size=state.population_size,
                generations=state.generations,
                max_index=state.max_index,
                strict_lower=state.strict_lower,
            )
            self._refresh_preview()
        except Exception as exc:
            self._messagebox.showerror("Simulation error", str(exc))
            return

        self.output.delete("1.0", self._tk.END)
        self.output.insert(self._tk.END, format_simulation_report(result))

    def _refresh_preview(self) -> None:
        """Prekresli maly grayscale preview aktualneho datasetu."""

        try:
            width = parse_positive_int(self.width_var.get())
            height = parse_positive_int(self.height_var.get())
            seed = int(self.seed_var.get().strip())
        except Exception:
            return

        image = make_image_dataset(self.dataset_var.get(), width, height, seed)
        self._draw_image(image)

    def _draw_image(self, image: GrayImage) -> None:
        """Nakresli grayscale obrazok ako siet malych stvorcov."""

        scale = max(1, min(8, 160 // max(image.width, image.height)))
        canvas_width = image.width * scale
        canvas_height = image.height * scale
        self.canvas.config(width=canvas_width, height=canvas_height)
        self.canvas.delete("all")

        for y in range(image.height):
            for x in range(image.width):
                pixel = image.pixels[(y * image.width) + x]
                color = f"#{pixel:02x}{pixel:02x}{pixel:02x}"
                self.canvas.create_rectangle(
                    x * scale,
                    y * scale,
                    (x + 1) * scale,
                    (y + 1) * scale,
                    outline=color,
                    fill=color,
                )


def main() -> None:
    """Spusti GUI alebo zlyha s jasnou hlaskou pri chybajucom Tk."""

    try:
        ResearchCockpit().run()
    except RuntimeError as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
