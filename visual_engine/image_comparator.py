# visual_engine/image_comparator.py
# The core visual AI engine of DualGuard
# Uses OpenCV to compare English and Arabic screenshots
# and detect visual regressions and layout issues

import os
import cv2
import numpy as np
from utils.config_loader import config


class ImageComparator:
    """
    Compares English and Arabic screenshots using OpenCV.
    Detects visual differences, layout breaks, and
    RTL/LTR rendering issues between the two versions.
    """

    def __init__(self):
        test_config = config.get_test_config()
        # Threshold below which we flag a visual issue
        # Default 40% — Arabic and English SHOULD look different
        # but not broken
        self.threshold = test_config.get("visual_threshold", 40)
        self.diff_dir = test_config.get(
            "diff_dir", "reports/diffs"
        )
        os.makedirs(self.diff_dir, exist_ok=True)

    # ──────────────────────────────────────────
    # Core Comparison
    # ──────────────────────────────────────────

    def compare(
        self, english_path: str, arabic_path: str, screen_name: str
    ) -> dict:
        """
        Compares two screenshots and returns a detailed result.
        english_path: path to English screenshot
        arabic_path: path to Arabic screenshot
        screen_name: name used for the diff image file
        Returns: dict with similarity score and diff image path
        """
        # Load both images
        english_img = self._load_image(english_path)
        arabic_img = self._load_image(arabic_path)

        # Resize Arabic to match English dimensions if different
        arabic_img = self._resize_to_match(arabic_img, english_img)

        # Calculate structural similarity
        similarity_score = self._calculate_similarity(
            english_img, arabic_img
        )

        # Generate diff image highlighting differences
        diff_path = self._generate_diff_image(
            english_img, arabic_img, screen_name
        )

        # Determine if this is a pass or potential issue
        status = self._evaluate_status(similarity_score)

        result = {
            "screen_name": screen_name,
            "english_path": english_path,
            "arabic_path": arabic_path,
            "diff_path": diff_path,
            "similarity_score": round(similarity_score, 2),
            "threshold": self.threshold,
            "status": status,
            "is_rtl_detected": self._detect_rtl_layout(
                english_img, arabic_img
            ),
            "dimensions_match": self._check_dimensions(
                english_img, arabic_img
            )
        }

        print(
            f"Comparison [{screen_name}]: "
            f"Similarity={similarity_score:.1f}% | "
            f"Status={status}"
        )
        return result

    def compare_all(self, pairs: list) -> list:
        """
        Compares all paired screenshots.
        pairs: list of dicts from ScreenshotCapture.get_paired_screenshots()
        Returns: list of comparison results
        """
        results = []
        for pair in pairs:
            result = self.compare(
                pair["english"],
                pair["arabic"],
                pair["name"]
            )
            results.append(result)
        return results

    # ──────────────────────────────────────────
    # Image Processing
    # ──────────────────────────────────────────

    def _load_image(self, path: str):
        """
        Loads an image from disk using OpenCV.
        Raises FileNotFoundError if image doesn't exist.
        """
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Screenshot not found: {path}"
            )
        img = cv2.imread(path)
        if img is None:
            raise ValueError(
                f"Could not read image: {path}"
            )
        return img

    def _resize_to_match(self, img, reference_img):
        """
        Resizes img to match reference_img dimensions.
        Needed when screenshots have slightly different sizes.
        """
        ref_height, ref_width = reference_img.shape[:2]
        img_height, img_width = img.shape[:2]

        if img_height != ref_height or img_width != ref_width:
            img = cv2.resize(
                img,
                (ref_width, ref_height),
                interpolation=cv2.INTER_AREA
            )
        return img

    def _calculate_similarity(
        self, img1, img2
    ) -> float:
        """
        Calculates visual similarity between two images.
        Uses histogram comparison for reliable results.
        Returns: similarity percentage (0-100)
        """
        # Convert to grayscale for comparison
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # Calculate histograms
        hist1 = cv2.calcHist(
            [gray1], [0], None, [256], [0, 256]
        )
        hist2 = cv2.calcHist(
            [gray2], [0], None, [256], [0, 256]
        )

        # Normalize histograms
        cv2.normalize(hist1, hist1, 0, 1, cv2.NORM_MINMAX)
        cv2.normalize(hist2, hist2, 0, 1, cv2.NORM_MINMAX)

        # Compare using correlation method
        # Returns value between -1 and 1, we convert to 0-100%
        correlation = cv2.compareHist(
            hist1, hist2, cv2.HISTCMP_CORREL
        )
        similarity = max(0, correlation) * 100
        return similarity

    def _generate_diff_image(
        self, img1, img2, screen_name: str
    ) -> str:
        """
        Creates a visual diff image highlighting differences.
        Different pixels are highlighted in red.
        Returns: path to the saved diff image
        """
        # Calculate absolute difference
        diff = cv2.absdiff(img1, img2)

        # Convert diff to grayscale
        diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        # Threshold to make differences more visible
        _, thresh = cv2.threshold(
            diff_gray, 30, 255, cv2.THRESH_BINARY
        )

        # Create red highlight overlay
        diff_colored = img1.copy()
        diff_colored[thresh == 255] = [0, 0, 255]

        # Create side by side comparison image
        side_by_side = np.hstack([img1, img2, diff_colored])

        # Save diff image
        diff_path = os.path.join(
            self.diff_dir, f"{screen_name}_diff.png"
        )
        cv2.imwrite(diff_path, side_by_side)
        print(f"Diff image saved: {diff_path}")
        return diff_path

    # ──────────────────────────────────────────
    # Analysis Methods
    # ──────────────────────────────────────────

    def _detect_rtl_layout(self, english_img, arabic_img) -> bool:
        """
        Attempts to detect if RTL layout is applied
        by comparing left/right pixel density differences.
        Returns True if RTL layout change is detected.
        """
        # Split images into left and right halves
        width = english_img.shape[1]
        mid = width // 2

        eng_left = english_img[:, :mid]
        eng_right = english_img[:, mid:]
        arab_left = arabic_img[:, :mid]
        arab_right = arabic_img[:, mid:]

        # Compare left half similarity and right half similarity
        left_diff = np.mean(
            cv2.absdiff(eng_left, arab_left)
        )
        right_diff = np.mean(
            cv2.absdiff(eng_right, arab_right)
        )

        # If right side differs more than left side,
        # it suggests layout mirroring (RTL)
        return right_diff > left_diff

    def _check_dimensions(self, img1, img2) -> bool:
        """
        Returns True if both images have the same dimensions.
        Dimension mismatch can indicate layout breaks.
        """
        return img1.shape == img2.shape

    def _evaluate_status(self, similarity_score: float) -> str:
        """
        Evaluates the comparison result status.
        Returns a human readable status string.
        """
        if similarity_score >= 70:
            return "SIMILAR — Possible missing RTL layout"
        elif similarity_score >= self.threshold:
            return "PASS — Expected bilingual difference detected"
        else:
            return "FLAG — Potential layout break detected"

    # ──────────────────────────────────────────
    # Summary
    # ──────────────────────────────────────────

    def get_summary(self, results: list) -> dict:
        """
        Generates a summary of all comparison results.
        results: list of comparison result dicts
        Returns: summary dict with counts and overall status
        """
        total = len(results)
        passed = sum(
            1 for r in results if "PASS" in r["status"]
        )
        flagged = sum(
            1 for r in results if "FLAG" in r["status"]
        )
        similar = sum(
            1 for r in results if "SIMILAR" in r["status"]
        )
        rtl_detected = sum(
            1 for r in results if r["is_rtl_detected"]
        )

        return {
            "total_comparisons": total,
            "passed": passed,
            "flagged": flagged,
            "similar": similar,
            "rtl_detected": rtl_detected,
            "overall_status": "PASS" if flagged == 0 else "ISSUES FOUND",
            "pass_rate": round(
                (passed / total * 100) if total > 0 else 0, 1
            )
        }