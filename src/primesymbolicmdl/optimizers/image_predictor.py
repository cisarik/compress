"""Adapter optimizera pre deterministicke 2D obrazkove prediktory."""

from __future__ import annotations

from .base import OptimizerRequest, OptimizerResult
from ..image_datasets import make_gray_image
from ..image_predictor_branch import encode_image_predictor_payload, estimate_image_predictor_cost
from ..image_predictors import default_image_predictor_models, render_image_predictor


class ImagePredictorOptimizer:
    """Registry adapter pre 2D grayscale predictor baseline."""

    def name(self) -> str:
        """Vrati stabilny nazov optimizera."""

        return "Image-predictor"

    def available(self) -> bool:
        """Tento baseline je plne implementovany v repozitari."""

        return True

    def run(self, request: OptimizerRequest) -> OptimizerResult:
        """Vyhodnoti malu sadu decoder-znamych 2D prediktorov."""

        width = request.metadata.get("image_width")
        height = request.metadata.get("image_height")
        dataset_name = request.metadata.get("dataset_name", "external")

        if not isinstance(width, int) or width <= 0:
            raise ValueError("Image-predictor requires positive metadata['image_width']")
        if not isinstance(height, int) or height <= 0:
            raise ValueError("Image-predictor requires positive metadata['image_height']")

        image_name = str(dataset_name) if isinstance(dataset_name, str) else "external"
        image = make_gray_image(image_name, width, height, bytes(request.data))

        history: list[dict] = []
        best_model = None
        best_cost = None

        for index, model in enumerate(default_image_predictor_models()):
            cost = estimate_image_predictor_cost(image, model)
            if best_cost is None or (cost["total_bits"], render_image_predictor(model)) < (
                best_cost["total_bits"],
                render_image_predictor(best_model),
            ):
                best_model = model
                best_cost = cost

            history.append(
                {
                    "generation": index,
                    "best_model": render_image_predictor(best_model),
                    "candidate_model": render_image_predictor(model),
                    "total_bits": best_cost["total_bits"],
                    "saving_bits": best_cost["saving_bits"],
                }
            )

        if best_model is None or best_cost is None:
            raise RuntimeError("Image-predictor did not evaluate any models")

        payload = encode_image_predictor_payload(image, best_model)
        return OptimizerResult(
            optimizer_name=self.name(),
            status="ok",
            best_model=render_image_predictor(best_model),
            raw_bits=best_cost["raw_bits"],
            total_bits=best_cost["total_bits"],
            saving_bits=best_cost["saving_bits"],
            ratio_vs_raw=best_cost["ratio_vs_raw"],
            history=history,
            details={
                "predictor_model": best_model,
                "payload": payload,
                "residual_width": best_cost["residual_width"],
                "residual_bits": best_cost["residual_bits"],
                "residual_codec": best_cost["residual_codec"],
                "residual_codec_details": best_cost["residual_codec_details"],
                "min_residual": best_cost["min_residual"],
                "max_residual": best_cost["max_residual"],
                "would_use_fallback": best_cost["total_bits"] >= best_cost["raw_bits"],
                "best_cost": best_cost,
            },
        )
