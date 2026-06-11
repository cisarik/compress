"""Jednoduchy Tkinter cockpit pre male vyskumne simulacie."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .image_datasets import GrayImage, get_image_dataset_names, make_gray_image, make_image_dataset
from .optimizers.image_gplite import available_image_gplite_primitive_sets
from .optimizers.registry import get_optimizer_names
from .simulation import format_simulation_report, run_gray_image_simulation


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
        from tkinter import filedialog, messagebox, ttk
    except ModuleNotFoundError as exc:
        raise RuntimeError("Tkinter is unavailable; install the system package 'tk'.") from exc
    return tk, ttk, messagebox, filedialog


@dataclass
class _CanvasPanel:
    """Spoji canvas s titulkom nad nim."""

    title_var: object
    canvas: object


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
    image_gplite_primitive_set: str
    max_index: int | None
    strict_lower: bool


class ResearchCockpit:
    """Jednoduche synchronne GUI pre prve porovnania optimizerov."""

    def __init__(self) -> None:
        tk, ttk, messagebox, filedialog = ensure_tkinter()
        self._tk = tk
        self._ttk = ttk
        self._messagebox = messagebox
        self._filedialog = filedialog
        self.root = tk.Tk()
        self.root.title("PrimeSymbolicMDL Research Cockpit")
        self.root.geometry("1480x980")

        optimizer_names = get_optimizer_names()
        dataset_names = get_image_dataset_names()
        self.optimizer_var = tk.StringVar(value=optimizer_names[0])
        self.dataset_var = tk.StringVar(value=dataset_names[0])
        self.preview_mode_var = tk.StringVar(value="Residuals")
        self.source_var = tk.StringVar(value="dataset")
        self.loaded_path_var = tk.StringVar(value="No file loaded")
        self.status_var = tk.StringVar(
            value="Choose a generated dataset or load a small PNG/GIF/PGM/PPM image."
        )
        self.width_var = tk.StringVar(value="32")
        self.height_var = tk.StringVar(value="32")
        self.seed_var = tk.StringVar(value="1234")
        self.population_var = tk.StringVar(value="24")
        self.generations_var = tk.StringVar(value="12")
        self.image_gplite_primitive_set_var = tk.StringVar(value="full")
        self.max_index_var = tk.StringVar(value="31")
        self.strict_lower_var = tk.BooleanVar(value=False)

        self.loaded_image: GrayImage | None = None
        self.active_image: GrayImage | None = None
        self._results_by_name: dict[str, dict] = {}

        self.original_panel: _CanvasPanel | None = None
        self.coded_panel: _CanvasPanel | None = None
        self.decoded_panel: _CanvasPanel | None = None
        self.history_canvas = None
        self.results_tree = None
        self.output = None

        self._build_layout()
        self._clear_results()
        self._refresh_preview(clear_results=False)

    def run(self) -> None:
        """Spusti Tkinter event loop."""

        self.root.mainloop()

    def _build_layout(self) -> None:
        """Postavi formular, preview panely, tabulku a report."""

        frame = self._ttk.Frame(self.root, padding=12)
        frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)

        controls = self._ttk.LabelFrame(frame, text="Input and search", padding=12)
        controls.grid(row=0, column=0, sticky="nsw", padx=(0, 12))
        controls.columnconfigure(1, weight=1)

        self._ttk.Label(controls, text="Source").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=4)
        source_row = self._ttk.Frame(controls)
        source_row.grid(row=0, column=1, sticky="ew", pady=4)
        self._ttk.Radiobutton(
            source_row,
            text="Generated",
            variable=self.source_var,
            value="dataset",
            command=self._refresh_preview,
        ).grid(row=0, column=0, sticky="w")
        self._ttk.Radiobutton(
            source_row,
            text="Loaded file",
            variable=self.source_var,
            value="file",
            command=self._refresh_preview,
        ).grid(row=0, column=1, sticky="w", padx=(8, 0))

        row_index = 1
        dataset_box = self._ttk.Combobox(controls, textvariable=self.dataset_var, values=get_image_dataset_names(), state="readonly")
        preview_box = self._ttk.Combobox(controls, textvariable=self.preview_mode_var, values=("Residuals", "Anchors"), state="readonly")
        primitive_box = self._ttk.Combobox(
            controls,
            textvariable=self.image_gplite_primitive_set_var,
            values=available_image_gplite_primitive_sets(),
            state="readonly",
        )
        controls_spec = [
            ("Optimizer", self._ttk.Combobox(controls, textvariable=self.optimizer_var, values=get_optimizer_names(), state="readonly")),
            ("Dataset", dataset_box),
            ("View", preview_box),
            ("Width", self._ttk.Entry(controls, textvariable=self.width_var)),
            ("Height", self._ttk.Entry(controls, textvariable=self.height_var)),
            ("Seed", self._ttk.Entry(controls, textvariable=self.seed_var)),
            ("Population", self._ttk.Entry(controls, textvariable=self.population_var)),
            ("Generations", self._ttk.Entry(controls, textvariable=self.generations_var)),
            ("Image-GP set", primitive_box),
            ("Max index", self._ttk.Entry(controls, textvariable=self.max_index_var)),
        ]

        for label, widget in controls_spec:
            self._ttk.Label(controls, text=label).grid(row=row_index, column=0, sticky="w", padx=(0, 8), pady=4)
            widget.grid(row=row_index, column=1, sticky="ew", pady=4)
            row_index += 1

        strict_box = self._ttk.Checkbutton(controls, text="Strict lower anchor", variable=self.strict_lower_var)
        strict_box.grid(row=row_index, column=0, columnspan=2, sticky="w", pady=(8, 4))
        row_index += 1

        file_row = self._ttk.Frame(controls)
        file_row.grid(row=row_index, column=0, columnspan=2, sticky="ew", pady=(8, 4))
        file_row.columnconfigure(1, weight=1)
        self._ttk.Button(file_row, text="Load image", command=self._load_image).grid(row=0, column=0, sticky="w")
        self._ttk.Label(file_row, textvariable=self.loaded_path_var, wraplength=260).grid(
            row=0,
            column=1,
            sticky="w",
            padx=(8, 0),
        )
        row_index += 1

        button_row = self._ttk.Frame(controls)
        button_row.grid(row=row_index, column=0, columnspan=2, sticky="ew", pady=(8, 4))
        button_row.columnconfigure(1, weight=1)
        self._ttk.Button(button_row, text="Run selected", command=self._run_selected_optimizer).grid(row=0, column=0, sticky="w")
        self._ttk.Button(button_row, text="Run all", command=self._run_all_optimizers).grid(row=0, column=1, sticky="w", padx=(8, 0))
        self._ttk.Button(button_row, text="Refresh input", command=self._refresh_preview).grid(row=0, column=2, sticky="e")
        row_index += 1

        self._ttk.Label(controls, textvariable=self.status_var, wraplength=320).grid(
            row=row_index,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(12, 0),
        )

        preview_frame = self._ttk.LabelFrame(frame, text="Image views", padding=12)
        preview_frame.grid(row=0, column=1, sticky="nsew")
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.columnconfigure(1, weight=1)
        preview_frame.columnconfigure(2, weight=1)
        preview_frame.rowconfigure(1, weight=1)

        self.original_panel = self._build_panel(preview_frame, 0, "Input image")
        self.coded_panel = self._build_panel(preview_frame, 1, "Residuals / anchors")
        self.decoded_panel = self._build_panel(preview_frame, 2, "Decoded image")

        history_title = self._ttk.Label(preview_frame, text="Search history (total_bits vs raw_bits)")
        history_title.grid(row=2, column=0, columnspan=3, sticky="w", pady=(12, 4))
        self.history_canvas = self._tk.Canvas(preview_frame, width=960, height=210, bg="white", highlightthickness=1)
        self.history_canvas.grid(row=3, column=0, columnspan=3, sticky="ew")

        lower_frame = self._ttk.Frame(frame)
        lower_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(12, 0))
        lower_frame.columnconfigure(0, weight=1)
        lower_frame.columnconfigure(1, weight=1)
        lower_frame.rowconfigure(0, weight=1)

        result_frame = self._ttk.LabelFrame(lower_frame, text="Optimizer comparison", padding=12)
        result_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)

        columns = ("optimizer", "status", "raw_bytes", "total_bytes", "saving_bytes", "ratio")
        self.results_tree = self._ttk.Treeview(result_frame, columns=columns, show="headings", height=8)
        headings = {
            "optimizer": "Optimizer",
            "status": "Status",
            "raw_bytes": "Raw B",
            "total_bytes": "Est B",
            "saving_bytes": "Saved B",
            "ratio": "Ratio",
        }
        widths = {
            "optimizer": 120,
            "status": 120,
            "raw_bytes": 80,
            "total_bytes": 80,
            "saving_bytes": 90,
            "ratio": 80,
        }
        for key in columns:
            self.results_tree.heading(key, text=headings[key])
            self.results_tree.column(key, width=widths[key], anchor="center", stretch=(key == "optimizer"))
        self.results_tree.grid(row=0, column=0, sticky="nsew")
        self.results_tree.bind("<<TreeviewSelect>>", self._on_result_selected)

        tree_scroll = self._ttk.Scrollbar(result_frame, orient="vertical", command=self.results_tree.yview)
        tree_scroll.grid(row=0, column=1, sticky="ns")
        self.results_tree.configure(yscrollcommand=tree_scroll.set)

        report_frame = self._ttk.LabelFrame(lower_frame, text="Detailed report", padding=12)
        report_frame.grid(row=0, column=1, sticky="nsew")
        report_frame.columnconfigure(0, weight=1)
        report_frame.rowconfigure(0, weight=1)
        self.output = self._tk.Text(report_frame, width=72, height=18, wrap="word")
        self.output.grid(row=0, column=0, sticky="nsew")

        text_scroll = self._ttk.Scrollbar(report_frame, orient="vertical", command=self.output.yview)
        text_scroll.grid(row=0, column=1, sticky="ns")
        self.output.configure(yscrollcommand=text_scroll.set)
        dataset_box.bind("<<ComboboxSelected>>", self._refresh_preview)
        preview_box.bind("<<ComboboxSelected>>", self._refresh_selected_view)

    def _build_panel(self, parent, column: int, title: str) -> _CanvasPanel:
        """Vytvori jeden obrazkovy panel s titulkom a canvasom."""

        title_var = self._tk.StringVar(value=title)
        self._ttk.Label(parent, textvariable=title_var).grid(row=0, column=column, sticky="w", pady=(0, 4))
        canvas = self._tk.Canvas(parent, width=280, height=280, bg="white", highlightthickness=1)
        canvas.grid(row=1, column=column, sticky="nsew", padx=(0 if column == 0 else 8, 0))
        return _CanvasPanel(title_var=title_var, canvas=canvas)

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
            image_gplite_primitive_set=self.image_gplite_primitive_set_var.get(),
            max_index=parse_optional_int(self.max_index_var.get()),
            strict_lower=bool(self.strict_lower_var.get()),
        )

    def _load_image(self) -> None:
        """Nacita lokalny obrazok podporeny Tk PhotoImage a prevedie ho na grayscale."""

        path = self._filedialog.askopenfilename(
            title="Load image",
            filetypes=[
                ("Tk image files", "*.png *.gif *.pgm *.ppm"),
                ("PNG", "*.png"),
                ("GIF", "*.gif"),
                ("PGM", "*.pgm"),
                ("PPM", "*.ppm"),
                ("All files", "*.*"),
            ],
        )
        if not path:
            return

        try:
            image = self._load_tk_image(path)
        except Exception as exc:
            self._messagebox.showerror("Image load error", str(exc))
            return

        self.loaded_image = image
        self.source_var.set("file")
        self.loaded_path_var.set(str(Path(path).name))
        self.width_var.set(str(image.width))
        self.height_var.set(str(image.height))
        self.status_var.set(
            f"Loaded {Path(path).name} as {image.width}x{image.height} grayscale. "
            "Large images may be slow in this research UI."
        )
        self._refresh_preview()

    def _load_tk_image(self, path: str) -> GrayImage:
        """Nacita obrazok cez Tk a vrati grayscale pixely bez externych kniznic."""

        photo = self._tk.PhotoImage(file=path)
        width = int(photo.width())
        height = int(photo.height())
        pixels = bytearray()
        for y in range(height):
            for x in range(width):
                pixels.append(self._pixel_to_gray(photo.get(x, y)))
        return make_gray_image(Path(path).name, width, height, bytes(pixels))

    def _pixel_to_gray(self, value) -> int:
        """Prevedie Tk pixel na 8-bit grayscale."""

        if isinstance(value, tuple):
            if len(value) >= 3:
                red, green, blue = (int(channel) for channel in value[:3])
                return (299 * red + 587 * green + 114 * blue) // 1000
            if len(value) == 1:
                return int(value[0])

        if isinstance(value, str):
            if value.startswith("#") and len(value) == 7:
                red = int(value[1:3], 16)
                green = int(value[3:5], 16)
                blue = int(value[5:7], 16)
                return (299 * red + 587 * green + 114 * blue) // 1000
            red16, green16, blue16 = self.root.winfo_rgb(value)
            red = red16 // 257
            green = green16 // 257
            blue = blue16 // 257
            return (299 * red + 587 * green + 114 * blue) // 1000

        raise ValueError(f"Unsupported pixel format from Tk image loader: {value!r}")

    def _run_selected_optimizer(self) -> None:
        """Spusti iba aktualne vybrany optimizer."""

        self._run_optimizers([self.optimizer_var.get()])

    def _run_all_optimizers(self) -> None:
        """Spusti vsetky registrovane optimizery nad tym istym vstupom."""

        self._run_optimizers(get_optimizer_names())

    def _run_optimizers(self, optimizer_names: list[str]) -> None:
        """Spusti sadu optimizerov a naplni tabulku vysledkov."""

        try:
            state = self._parse_state()
            image = self._resolve_image(state)
        except Exception as exc:
            self._messagebox.showerror("Simulation error", str(exc))
            return

        self.active_image = image
        self.status_var.set(f"Running {len(optimizer_names)} optimizer(s) on {image.name} ({image.width}x{image.height})...")
        self.root.update_idletasks()

        results = []
        for optimizer_name in optimizer_names:
            try:
                result = run_gray_image_simulation(
                    optimizer_name,
                    image,
                    seed=state.seed,
                    population_size=state.population_size,
                    generations=state.generations,
                    image_gplite_primitive_set=state.image_gplite_primitive_set,
                    max_index=state.max_index,
                    strict_lower=state.strict_lower,
                )
            except Exception as exc:
                result = self._error_result(optimizer_name, image, str(exc))
            results.append(result)

        self._store_results(results)
        best = min(results, key=lambda item: (item["total_bits"], item["optimizer_name"]))
        self._select_result(best["optimizer_name"])
        self.status_var.set(
            f"Finished {len(results)} optimizer(s). "
            f"Best total_bits={best['total_bits']} with {best['optimizer_name']}."
        )

    def _error_result(self, optimizer_name: str, image: GrayImage, message: str) -> dict:
        """Vrati stabilny error vysledok, aby GUI ostalo citatelne."""

        raw_bits = len(image.pixels) * 8
        raw_bytes = len(image.pixels)
        return {
            "optimizer_name": optimizer_name,
            "status": "error",
            "dataset_name": image.name,
            "image_width": image.width,
            "image_height": image.height,
            "raw_bits": raw_bits,
            "total_bits": raw_bits,
            "saving_bits": 0,
            "ratio_vs_raw": 1.0,
            "raw_bytes": raw_bytes,
            "total_bytes_estimate": raw_bytes,
            "saving_bytes_estimate": 0,
            "best_model": "error",
            "history": [],
            "details": {"message": message},
        }

    def _resolve_image(self, state: _GuiState) -> GrayImage:
        """Vrati aktivny vstupny obrazok podla zvoleneho zdroja."""

        if self.source_var.get() == "file":
            if self.loaded_image is None:
                raise ValueError("No file image is loaded.")
            return self.loaded_image
        return make_image_dataset(state.dataset_name, state.image_width, state.image_height, state.seed)

    def _refresh_preview(self, _event=None, clear_results: bool = True) -> None:
        """Prekresli vstupny obrazok a pripadne zneplatni stare vysledky."""

        try:
            state = self._parse_state()
            image = self._resolve_image(state)
        except Exception:
            return

        self.active_image = image
        if self.original_panel is not None:
            self.original_panel.title_var.set(f"Input image: {image.name} ({image.width}x{image.height})")
            self._draw_image(self.original_panel.canvas, image)
        if clear_results:
            self._clear_results()

    def _refresh_selected_view(self, _event=None) -> None:
        """Prekresli coded panel pre aktualne vybrany vysledok bez resetu."""

        if self.results_tree is None:
            return
        selection = self.results_tree.selection()
        if not selection:
            return
        optimizer_name = selection[0]
        result = self._results_by_name.get(optimizer_name)
        if result is not None:
            self._draw_result_images(result)

    def _store_results(self, results: list[dict]) -> None:
        """Nahradi tabulku vysledkov novym behom."""

        self._results_by_name = {result["optimizer_name"]: result for result in results}
        self._clear_tree()
        for result in results:
            self.results_tree.insert(
                "",
                "end",
                iid=result["optimizer_name"],
                values=(
                    result["optimizer_name"],
                    result["status"],
                    result["raw_bytes"],
                    result["total_bytes_estimate"],
                    result["saving_bytes_estimate"],
                    f"{result['ratio_vs_raw']:.3f}",
                ),
            )

    def _clear_results(self) -> None:
        """Vymaze stare vysledky a necha iba vstupny preview."""

        self._results_by_name = {}
        self._clear_tree()
        if self.output is not None:
            self.output.delete("1.0", self._tk.END)
        self._draw_history(None)
        if self.coded_panel is not None:
            self.coded_panel.title_var.set("Residuals / anchors")
            self._draw_placeholder(self.coded_panel.canvas, "Run an optimizer to inspect the coded view.")
        if self.decoded_panel is not None:
            self.decoded_panel.title_var.set("Decoded image")
            self._draw_placeholder(self.decoded_panel.canvas, "Run an optimizer to inspect exact reconstruction.")

    def _clear_tree(self) -> None:
        """Vymaze vsetky riadky v tabulke vysledkov."""

        if self.results_tree is None:
            return
        for item_id in self.results_tree.get_children():
            self.results_tree.delete(item_id)

    def _select_result(self, optimizer_name: str) -> None:
        """Programovo vyberie riadok a zobrazi detail vysledku."""

        if self.results_tree is None or optimizer_name not in self._results_by_name:
            return
        self.results_tree.selection_set(optimizer_name)
        self.results_tree.focus(optimizer_name)
        self._show_result(self._results_by_name[optimizer_name])

    def _on_result_selected(self, _event=None) -> None:
        """Zareaguje na manualny vyber riadku v tabulke."""

        if self.results_tree is None:
            return
        selection = self.results_tree.selection()
        if not selection:
            return
        optimizer_name = selection[0]
        result = self._results_by_name.get(optimizer_name)
        if result is not None:
            self._show_result(result)

    def _show_result(self, result: dict) -> None:
        """Zobrazi detail vybraneho optimizera."""

        if self.output is not None:
            self.output.delete("1.0", self._tk.END)
            self.output.insert(self._tk.END, format_simulation_report(result))
        self._draw_history(result)
        self._draw_result_images(result)

    def _draw_result_images(self, result: dict) -> None:
        """Prekresli coded a decoded pohlad pre vybrany vysledok."""

        preview = result.get("preview")
        if self.active_image is not None and self.original_panel is not None:
            self._draw_image(self.original_panel.canvas, self.active_image)

        if not isinstance(preview, dict):
            self._draw_fallback_result_images(result)
            return

        coded_key = "residual_image" if self.preview_mode_var.get() == "Residuals" else "anchor_image"
        coded_title = str(preview.get("residual_label", "Residuals"))
        if coded_key == "anchor_image":
            coded_title = str(preview.get("anchor_label", "Anchors"))

        coded_image = preview[coded_key]
        decoded_image = preview["decoded_image"]
        residual_codec = result.get("details", {}).get("residual_codec")

        if self.coded_panel is not None:
            codec_suffix = f" codec={residual_codec}" if residual_codec else ""
            self.coded_panel.title_var.set(
                f"{coded_title}{codec_suffix}: min_residual={preview['min_residual']} max_residual={preview['max_residual']} escapes={preview['escaped_count']}"
            )
            self._draw_image(self.coded_panel.canvas, coded_image)
        if self.decoded_panel is not None:
            self.decoded_panel.title_var.set(
                f"Decoded: exact_roundtrip={preview['roundtrip_ok']}"
            )
            self._draw_image(self.decoded_panel.canvas, decoded_image)

    def _draw_fallback_result_images(self, result: dict) -> None:
        """Zobrazi placeholder alebo raw fallback, ked preview nie je dostupny."""

        if self.active_image is None:
            return

        if self.coded_panel is not None:
            self.coded_panel.title_var.set("Coded view unavailable")
            self._draw_placeholder(
                self.coded_panel.canvas,
                "This optimizer does not expose a law-based coded image preview.",
            )

        if self.decoded_panel is None:
            return

        if result["best_model"] == "raw_fallback":
            self.decoded_panel.title_var.set("Decoded image: raw fallback")
            self._draw_image(self.decoded_panel.canvas, self.active_image)
            return

        self.decoded_panel.title_var.set("Decoded image unavailable")
        self._draw_placeholder(
            self.decoded_panel.canvas,
            "No exact decoded preview is available for this result.",
        )

    def _draw_history(self, result: dict | None) -> None:
        """Nakresli priebeh total_bits pre vybrany search."""

        if self.history_canvas is None:
            return

        canvas = self.history_canvas
        canvas.delete("all")
        width = int(canvas.cget("width"))
        height = int(canvas.cget("height"))

        left = 48
        right = width - 16
        top = 16
        bottom = height - 28
        canvas.create_rectangle(left, top, right, bottom, outline="#999999")

        if result is None:
            self._draw_placeholder(canvas, "Run an optimizer to see total_bits history.")
            return

        history = result.get("history", [])
        raw_bits = int(result["raw_bits"])
        canvas.create_line(left, top, right, top, fill="#ffffff")

        if not history:
            self._draw_placeholder(canvas, "No search history is available for this optimizer.")
            return

        totals = [int(item.get("total_bits", raw_bits)) for item in history]
        generations = [int(item.get("generation", index)) for index, item in enumerate(history)]
        max_bits = max(max(totals), raw_bits)
        min_bits = min(min(totals), raw_bits)
        span = max(1, max_bits - min_bits)

        def project_x(index: int) -> float:
            if len(generations) == 1:
                return (left + right) / 2
            return left + ((right - left) * index / (len(generations) - 1))

        def project_y(bits: int) -> float:
            return bottom - ((bits - min_bits) * (bottom - top) / span)

        raw_y = project_y(raw_bits)
        canvas.create_line(left, raw_y, right, raw_y, fill="#cc3333", dash=(4, 4), width=2)
        canvas.create_text(left, raw_y - 10, anchor="w", text=f"raw_bits={raw_bits}", fill="#aa2222")

        points = []
        for index, total_bits in enumerate(totals):
            points.extend((project_x(index), project_y(total_bits)))
        if len(points) >= 4:
            canvas.create_line(*points, fill="#1f5d9b", width=3, smooth=False)

        for index, total_bits in enumerate(totals):
            x_coord = project_x(index)
            y_coord = project_y(total_bits)
            canvas.create_oval(x_coord - 3, y_coord - 3, x_coord + 3, y_coord + 3, fill="#1f5d9b", outline="#1f5d9b")
            canvas.create_text(x_coord, bottom + 12, text=str(generations[index]), fill="#333333")

        canvas.create_text(left, top - 8, anchor="w", text=f"best total_bits={min(totals)}", fill="#333333")
        canvas.create_text(right, top - 8, anchor="e", text=result["optimizer_name"], fill="#333333")
        canvas.create_text(left, bottom + 12, anchor="w", text="generation", fill="#333333")

    def _draw_placeholder(self, canvas, text: str) -> None:
        """Vymaze canvas a zobrazi textovy placeholder."""

        canvas.delete("all")
        width = int(canvas.cget("width"))
        height = int(canvas.cget("height"))
        canvas.create_text(width // 2, height // 2, width=max(120, width - 24), text=text, fill="#666666")

    def _draw_image(self, canvas, image: GrayImage) -> None:
        """Nakresli grayscale obrazok ako siet malych stvorcov."""

        max_canvas = 280
        scale = max(1, min(8, max_canvas // max(image.width, image.height)))
        canvas_width = image.width * scale
        canvas_height = image.height * scale
        canvas.config(width=canvas_width, height=canvas_height)
        canvas.delete("all")

        for y in range(image.height):
            for x in range(image.width):
                pixel = image.pixels[(y * image.width) + x]
                color = f"#{pixel:02x}{pixel:02x}{pixel:02x}"
                canvas.create_rectangle(
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
