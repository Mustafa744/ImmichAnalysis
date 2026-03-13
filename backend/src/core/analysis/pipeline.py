import cv2
import numpy as np
import traceback
from typing import Protocol, Dict, Any, List
import vibrant
from PIL import Image
from vibrant.image import VibrantImage


class AnalysisStep(Protocol):
    def analyze(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Analyze an RGB image array and return a dictionary of feature/metric results.
        :param image: A NumPy array of shape (H, W, 3) representing an RGB image.
        """
        pass


class HistogramAnalysis:
    """Calculates 32-bin density histograms for R, G, B channels."""

    def __init__(self, bins: int = 32):
        self.bins = bins

    def analyze(self, image: np.ndarray) -> Dict[str, Any]:
        # Vectorized histogram via OpenCV for speed
        img_u8 = np.clip(image, 0, 255).astype(np.uint8)

        r_hist = cv2.calcHist([img_u8], [0], None, [self.bins], [0, 256]).flatten()
        g_hist = cv2.calcHist([img_u8], [1], None, [self.bins], [0, 256]).flatten()
        b_hist = cv2.calcHist([img_u8], [2], None, [self.bins], [0, 256]).flatten()

        n_pixels = float(image.shape[0] * image.shape[1])
        bin_width = 256.0 / self.bins

        return {
            "r_hist": (r_hist / (n_pixels * bin_width)).tolist(),
            "g_hist": (g_hist / (n_pixels * bin_width)).tolist(),
            "b_hist": (b_hist / (n_pixels * bin_width)).tolist(),
        }


class MetricsAnalysis:
    """Calculates generic image quality metrics (brightness, colorfulness, warmth, sky_score)."""

    def analyze(self, image: np.ndarray) -> Dict[str, Any]:
        pixels = image.reshape(-1, 3).astype(np.float32)

        channel_means = pixels.mean(axis=0)  # [R, G, B]
        brightness = float(pixels.mean())
        colorfulness = float(pixels.std())

        # Handle grayscale images (1 channel) vs RGB (3 channels)
        if len(channel_means) >= 3:
            warmth = float(channel_means[0] - channel_means[2])  # R - B
        else:
            warmth = 0.0

        # Sky score logic: difference between B and R in top third of image
        h = image.shape[0]
        top_third = image[: max(1, h // 3), :, :].astype(np.float32)

        if top_third.shape[2] >= 3:
            sky_score = float(top_third[:, :, 2].mean() - top_third[:, :, 0].mean())
        else:
            sky_score = 0.0

        return {
            "brightness": round(brightness, 2),
            "colorfulness": round(colorfulness, 2),
            "warmth": round(warmth, 2),
            "sky_score": round(sky_score, 2),
        }


class SafeVibrantImage(VibrantImage):
    """
    A persistent subclass override to fix a critical bug in `vibrant-python`.
    The original library indiscriminately strips all `0` bytes from the palette,
    corrupting the RGB stride and causing IndexError for certain images or pure black pixels.
    """

    def quantize(self):
        self.image = self.image.quantize(colors=self.props.color_count)
        swatches = []
        # getpalette() returns a flat list [R, G, B, R, G, B, ...]
        raw = self.image.getpalette()
        # getcolors() returns a list of tuples: (count, index)
        pops = self.image.getcolors() or []
        for count, idx in pops:
            if idx * 3 + 2 < len(raw):
                swatches.append(
                    vibrant.models.Swatch(
                        rgb=[
                            raw[idx * 3],
                            raw[idx * 3 + 1],
                            raw[idx * 3 + 2],
                        ],
                        population=count,
                    )
                )
        return swatches


class ColorPaletteAnalysis:
    """Extracts a vibrant color palette using python-vibrant."""

    def __init__(self, color_count: int = 32, quality: int = 5):
        self.color_count = color_count
        self.quality = quality

    def _rgb_to_hex(self, rgb: tuple[int, int, int]) -> str:
        return f"#{int(rgb[0]):02X}{int(rgb[1]):02X}{int(rgb[2]):02X}"

    def analyze(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Extracts a color palette from an RGB image array.

        Args:
            image (np.ndarray): An image array in RGB channel order.
                                Do not pass BGR images directly.

        Returns:
            Dict containing 'color_palette' and 'dominant_colors'.
        """
        # Create a PIL Image directly from the RGB numpy array
        # This bypasses any costly JPEG encoding step.

        try:
            pil_img = Image.fromarray(image)
            v_img = SafeVibrantImage(pil_img)

            v = vibrant.Vibrant(self.color_count, self.quality)
            palette = v.get_palette(v_img)

            swatches = {
                "vibrant": palette.vibrant,
                "light_vibrant": palette.light_vibrant,
                "dark_vibrant": palette.dark_vibrant,
                "muted": palette.muted,
                "light_muted": palette.light_muted,
                "dark_muted": palette.dark_muted,
            }

            extracted_colors = {}
            for name, swatch in swatches.items():
                if swatch:
                    r, g, b = swatch.rgb
                    extracted_colors[name] = self._rgb_to_hex((r, g, b))

            return {
                "color_palette": extracted_colors,
            }
        except Exception as e:
            # Fallback for vibrant-python indexing errors on edge-case images
            print(f"Skipping palette extraction due to internal vibrant error: {e}")
            import traceback

            traceback.print_exc()
            return {
                "color_palette": {},
            }

class BatchAnalyzer:
    """Orchestrates image analysis through a series of registered steps."""

    def __init__(self, steps: List[AnalysisStep]):
        self.steps = steps

    def analyze_single(
        self, image: np.ndarray, thumb_size: tuple[int, int] = (100, 100)
    ) -> Dict[str, Any]:
        """
        Runs the full analysis pipeline on a single image.
        WARNING: The input `image` MUST be in standard RGB channel order.
                 If you read via cv2.imread(), you must convert via cv2.COLOR_BGR2RGB first.
        """
        if image is None or image.size == 0:
            return {}

        # Resize to standard thumbnail size for processing speed
        small = cv2.resize(image, thumb_size, interpolation=cv2.INTER_AREA)

        result = {}
        for step in self.steps:
            try:
                result.update(step.analyze(small))
            except Exception:
                print(f"Error in analysis step {step.__class__.__name__}:")
                traceback.print_exc()
        return result
