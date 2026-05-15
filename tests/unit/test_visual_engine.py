# tests/unit/test_visual_engine.py
# Unit tests for the visual engine components
# These run without needing BrowserStack or a real device

import numpy as np
import cv2
import os
import pytest


class TestImageComparator:
    """Unit tests for ImageComparator."""

    def test_comparator_imports(self):
        """Verify ImageComparator imports correctly."""
        from visual_engine.image_comparator import ImageComparator
        comparator = ImageComparator()
        assert comparator is not None

    def test_compare_identical_images(self, tmp_path):
        """Two identical images should have high similarity."""
        from visual_engine.image_comparator import ImageComparator
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        img[:] = (255, 255, 255)
        path1 = str(tmp_path / "img1.png")
        path2 = str(tmp_path / "img2.png")
        cv2.imwrite(path1, img)
        cv2.imwrite(path2, img)
        comparator = ImageComparator()
        result = comparator.compare(path1, path2, "test")
        assert result["similarity_score"] > 90

    def test_compare_different_images(self, tmp_path):
        """Two different images should have lower similarity."""
        from visual_engine.image_comparator import ImageComparator
        img1 = np.zeros((100, 100, 3), dtype=np.uint8)
        img1[:] = (255, 255, 255)
        img2 = np.zeros((100, 100, 3), dtype=np.uint8)
        img2[:] = (0, 0, 0)
        path1 = str(tmp_path / "white.png")
        path2 = str(tmp_path / "black.png")
        cv2.imwrite(path1, img1)
        cv2.imwrite(path2, img2)
        comparator = ImageComparator()
        result = comparator.compare(path1, path2, "test")
        assert result["similarity_score"] < 90

    def test_result_has_required_keys(self, tmp_path):
        """Comparison result must contain all required keys."""
        from visual_engine.image_comparator import ImageComparator
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        path1 = str(tmp_path / "img1.png")
        path2 = str(tmp_path / "img2.png")
        cv2.imwrite(path1, img)
        cv2.imwrite(path2, img)
        comparator = ImageComparator()
        result = comparator.compare(path1, path2, "test")
        required_keys = [
            "screen_name",
            "similarity_score",
            "status",
            "is_rtl_detected",
            "dimensions_match",
            "diff_path"
        ]
        for key in required_keys:
            assert key in result, f"Missing key: {key}"


class TestDiffHighlighter:
    """Unit tests for DiffHighlighter."""

    def test_highlighter_imports(self):
        """Verify DiffHighlighter imports correctly."""
        from visual_engine.diff_highlighter import DiffHighlighter
        highlighter = DiffHighlighter()
        assert highlighter is not None

    def test_creates_diff_image(self, tmp_path):
        """Highlighter should create a diff image file."""
        from visual_engine.diff_highlighter import DiffHighlighter
        img1 = np.zeros((200, 100, 3), dtype=np.uint8)
        img1[:] = (255, 255, 255)
        img2 = np.zeros((200, 100, 3), dtype=np.uint8)
        img2[:] = (200, 180, 160)
        path1 = str(tmp_path / "english.png")
        path2 = str(tmp_path / "arabic.png")
        cv2.imwrite(path1, img1)
        cv2.imwrite(path2, img2)
        highlighter = DiffHighlighter()
        result_path = highlighter.create_highlighted_diff(
            path1, path2, "unit_test", 75.0,
            "PASS — Expected bilingual difference detected"
        )
        assert os.path.exists(result_path)


class TestScreenshotCapture:
    """Unit tests for ScreenshotCapture."""

    def test_screenshot_capture_imports(self):
        """Verify ScreenshotCapture imports correctly."""
        from visual_engine.screenshot_capture import ScreenshotCapture
        assert ScreenshotCapture is not None