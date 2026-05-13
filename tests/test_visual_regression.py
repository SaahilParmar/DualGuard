# tests/test_visual_regression.py
# DualGuard's core visual regression test suite
# Compares English and Arabic screenshots using OpenCV
# Generates highlighted diff images for the HTML report

import pytest
import allure
from visual_engine.screenshot_capture import ScreenshotCapture
from visual_engine.image_comparator import ImageComparator
from visual_engine.diff_highlighter import DiffHighlighter


@allure.suite("DualGuard — Visual Regression Suite")
@allure.feature("Arabic vs English Visual Comparison")
class TestVisualRegression:
    """
    Compares English and Arabic screenshots
    to detect visual regressions and layout issues.
    Runs after both English and Arabic test suites
    have captured their screenshots.
    """

    # ──────────────────────────────────────────
    # Home Screen Visual Tests
    # ──────────────────────────────────────────

    @allure.title("Visual — Home screen RTL layout detected")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_home_screen_visual(self, dual_drivers):
        """
        Compares English and Arabic home screens.
        Verifies RTL layout is correctly applied
        in the Arabic version.
        """
        comparator = ImageComparator()
        highlighter = DiffHighlighter()
        capture = ScreenshotCapture(dual_drivers["english"])

        with allure.step("Verify screenshots exist"):
            assert capture.screenshot_exists(
                "home_screen", "english"
            ), "English home screenshot missing"
            assert capture.screenshot_exists(
                "home_screen", "arabic"
            ), "Arabic home screenshot missing"

        with allure.step("Run visual comparison"):
            result = comparator.compare(
                capture.get_screenshot_path(
                    "home_screen", "english"
                ),
                capture.get_screenshot_path(
                    "home_screen", "arabic"
                ),
                "home_screen"
            )

        with allure.step("Generate highlighted diff"):
            diff_path = highlighter.create_highlighted_diff(
                english_path=result["english_path"],
                arabic_path=result["arabic_path"],
                screen_name="home_screen",
                similarity_score=result["similarity_score"],
                status=result["status"]
            )
            allure.attach.file(
                diff_path,
                name="home_screen_diff",
                attachment_type=allure.attachment_type.PNG
            )

        with allure.step("Verify RTL layout detected"):
            assert result["is_rtl_detected"], \
                "RTL layout not detected on home screen"

        with allure.step("Verify similarity is in expected range"):
            assert result["similarity_score"] >= 40, \
                f"Home screen too dissimilar: " \
                f"{result['similarity_score']}%"

    # ──────────────────────────────────────────
    # Search Bar Visual Tests
    # ──────────────────────────────────────────

    @allure.title("Visual — Search bar position differs in RTL")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_bar_visual(self, dual_drivers):
        """
        Verifies search bar is repositioned correctly
        for Arabic RTL layout vs English LTR layout.
        """
        comparator = ImageComparator()
        highlighter = DiffHighlighter()
        capture = ScreenshotCapture(dual_drivers["english"])

        with allure.step("Verify screenshots exist"):
            assert capture.screenshot_exists(
                "search_bar", "english"
            ), "English search bar screenshot missing"
            assert capture.screenshot_exists(
                "search_bar", "arabic"
            ), "Arabic search bar screenshot missing"

        with allure.step("Run visual comparison"):
            result = comparator.compare(
                capture.get_screenshot_path(
                    "search_bar", "english"
                ),
                capture.get_screenshot_path(
                    "search_bar", "arabic"
                ),
                "search_bar"
            )

        with allure.step("Generate highlighted diff"):
            diff_path = highlighter.create_highlighted_diff(
                english_path=result["english_path"],
                arabic_path=result["arabic_path"],
                screen_name="search_bar",
                similarity_score=result["similarity_score"],
                status=result["status"]
            )
            allure.attach.file(
                diff_path,
                name="search_bar_diff",
                attachment_type=allure.attachment_type.PNG
            )

        with allure.step("Verify layout difference detected"):
            assert result["similarity_score"] < 90, \
                "Search bar layout looks identical " \
                "in English and Arabic — RTL may not be applied"

    # ──────────────────────────────────────────
    # Login Screen Visual Tests
    # ──────────────────────────────────────────

    @allure.title("Visual — Login screen RTL layout verified")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_screen_visual(self, dual_drivers):
        """
        Compares login screens between English and Arabic.
        Verifies form fields and buttons are
        correctly mirrored in RTL layout.
        """
        comparator = ImageComparator()
        highlighter = DiffHighlighter()
        capture = ScreenshotCapture(dual_drivers["english"])

        with allure.step("Verify screenshots exist"):
            assert capture.screenshot_exists(
                "login_screen", "english"
            ), "English login screenshot missing"
            assert capture.screenshot_exists(
                "login_screen", "arabic"
            ), "Arabic login screenshot missing"

        with allure.step("Run visual comparison"):
            result = comparator.compare(
                capture.get_screenshot_path(
                    "login_screen", "english"
                ),
                capture.get_screenshot_path(
                    "login_screen", "arabic"
                ),
                "login_screen"
            )

        with allure.step("Generate highlighted diff"):
            diff_path = highlighter.create_highlighted_diff(
                english_path=result["english_path"],
                arabic_path=result["arabic_path"],
                screen_name="login_screen",
                similarity_score=result["similarity_score"],
                status=result["status"]
            )
            allure.attach.file(
                diff_path,
                name="login_screen_diff",
                attachment_type=allure.attachment_type.PNG
            )

        with allure.step("Verify RTL layout on login screen"):
            assert result["is_rtl_detected"], \
                "RTL layout not detected on login screen"

    # ──────────────────────────────────────────
    # Settings Screen Visual Tests
    # ──────────────────────────────────────────

    @allure.title("Visual — Settings screen RTL layout verified")
    @allure.severity(allure.severity_level.NORMAL)
    def test_settings_screen_visual(self, dual_drivers):
        """
        Compares settings screens between English and Arabic.
        Verifies settings layout is correctly mirrored
        for RTL Arabic display.
        """
        comparator = ImageComparator()
        highlighter = DiffHighlighter()
        capture = ScreenshotCapture(dual_drivers["english"])

        with allure.step("Verify screenshots exist"):
            assert capture.screenshot_exists(
                "settings_screen", "english"
            ), "English settings screenshot missing"
            assert capture.screenshot_exists(
                "settings_screen", "arabic"
            ), "Arabic settings screenshot missing"

        with allure.step("Run visual comparison"):
            result = comparator.compare(
                capture.get_screenshot_path(
                    "settings_screen", "english"
                ),
                capture.get_screenshot_path(
                    "settings_screen", "arabic"
                ),
                "settings_screen"
            )

        with allure.step("Generate highlighted diff"):
            diff_path = highlighter.create_highlighted_diff(
                english_path=result["english_path"],
                arabic_path=result["arabic_path"],
                screen_name="settings_screen",
                similarity_score=result["similarity_score"],
                status=result["status"]
            )
            allure.attach.file(
                diff_path,
                name="settings_screen_diff",
                attachment_type=allure.attachment_type.PNG
            )

        with allure.step("Verify layout difference detected"):
            assert result["similarity_score"] >= 30, \
                f"Settings screen similarity too low: " \
                f"{result['similarity_score']}%"

    # ──────────────────────────────────────────
    # Full Suite Visual Summary Test
    # ──────────────────────────────────────────

    @allure.title("Visual — Full bilingual comparison summary")
    @allure.severity(allure.severity_level.NORMAL)
    def test_full_visual_summary(self, dual_drivers):
        """
        Runs visual comparison across all paired screenshots.
        Generates a complete summary of the bilingual
        visual regression results.
        """
        comparator = ImageComparator()
        highlighter = DiffHighlighter()
        capture = ScreenshotCapture(dual_drivers["english"])

        with allure.step("Get all paired screenshots"):
            pairs = capture.get_paired_screenshots()
            assert len(pairs) > 0, \
                "No paired screenshots found for comparison"

        with allure.step("Run comparison on all pairs"):
            results = comparator.compare_all(pairs)

        with allure.step("Generate all highlighted diffs"):
            highlighter.highlight_all(results)

        with allure.step("Generate summary"):
            summary = comparator.get_summary(results)
            allure.attach(
                str(summary),
                name="visual_comparison_summary",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Verify overall pass rate"):
            assert summary["pass_rate"] >= 60, \
                f"Overall visual pass rate too low: " \
                f"{summary['pass_rate']}%"

        with allure.step("Verify RTL detection rate"):
            assert summary["rtl_detected"] > 0, \
                "RTL layout not detected in any screen comparison"

        print(f"\nDualGuard Visual Summary:")
        print(f"Total Comparisons: {summary['total_comparisons']}")
        print(f"Passed: {summary['passed']}")
        print(f"Flagged: {summary['flagged']}")
        print(f"RTL Detected: {summary['rtl_detected']}")
        print(f"Pass Rate: {summary['pass_rate']}%")
        print(f"Overall: {summary['overall_status']}")