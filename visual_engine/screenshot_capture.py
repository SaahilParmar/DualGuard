# visual_engine/screenshot_capture.py
# Handles all screenshot capture and storage for DualGuard
# Screenshots are the input to the visual comparison engine

import os
import time
from utils.config_loader import config


class ScreenshotCapture:
    """
    Captures and organises screenshots for visual comparison.
    Saves English screenshots separately from Arabic screenshots
    so the comparator can pair them up correctly.
    """

    def __init__(self, driver):
        self.driver = driver
        test_config = config.get_test_config()
        self.screenshot_dir = test_config.get(
            "screenshot_dir", "reports/screenshots"
        )
        self._ensure_directories()

    # ──────────────────────────────────────────
    # Directory Setup
    # ──────────────────────────────────────────

    def _ensure_directories(self):
        """
        Creates screenshot directories if they don't exist.
        Creates both english/ and arabic/ subdirectories.
        """
        for locale in ["english", "arabic"]:
            folder = os.path.join(self.screenshot_dir, locale)
            os.makedirs(folder, exist_ok=True)

    # ──────────────────────────────────────────
    # Screenshot Capture
    # ──────────────────────────────────────────

    def capture(self, screen_name: str, locale: str) -> str:
        """
        Captures a screenshot and saves it to the correct folder.
        screen_name: descriptive name e.g. 'home_screen'
        locale: 'english' or 'arabic'
        Returns: full path of saved screenshot
        """
        # Add timestamp to avoid overwriting previous runs
        timestamp = int(time.time())
        filename = f"{screen_name}_{timestamp}.png"
        folder = os.path.join(self.screenshot_dir, locale)
        filepath = os.path.join(folder, filename)
        self.driver.save_screenshot(filepath)
        print(f"Screenshot saved: {filepath}")
        return filepath

    def capture_named(self, screen_name: str, locale: str) -> str:
        """
        Captures a screenshot with a fixed name — no timestamp.
        Used when we need to pair English and Arabic screenshots
        by the same name for comparison.
        screen_name: must match exactly between English and Arabic
        locale: 'english' or 'arabic'
        Returns: full path of saved screenshot
        """
        filename = f"{screen_name}.png"
        folder = os.path.join(self.screenshot_dir, locale)
        filepath = os.path.join(folder, filename)
        self.driver.save_screenshot(filepath)
        print(f"Named screenshot saved: {filepath}")
        return filepath

    def capture_sequence(
        self, screen_names: list, locale: str
    ) -> list:
        """
        Captures multiple screenshots in sequence.
        screen_names: list of screen names to capture
        locale: 'english' or 'arabic'
        Returns: list of saved file paths
        """
        paths = []
        for name in screen_names:
            path = self.capture_named(name, locale)
            paths.append(path)
            # Small pause between captures
            time.sleep(0.5)
        return paths

    # ──────────────────────────────────────────
    # Screenshot Retrieval
    # ──────────────────────────────────────────

    def get_screenshot_path(
        self, screen_name: str, locale: str
    ) -> str:
        """
        Returns the expected path for a named screenshot.
        Useful for checking if a screenshot exists before comparing.
        """
        filename = f"{screen_name}.png"
        return os.path.join(self.screenshot_dir, locale, filename)

    def screenshot_exists(
        self, screen_name: str, locale: str
    ) -> bool:
        """
        Returns True if a named screenshot exists on disk.
        Used by comparator to verify both sides exist
        before running comparison.
        """
        path = self.get_screenshot_path(screen_name, locale)
        return os.path.exists(path)

    def get_all_screenshots(self, locale: str) -> list:
        """
        Returns a list of all screenshot paths for a locale.
        locale: 'english' or 'arabic'
        """
        folder = os.path.join(self.screenshot_dir, locale)
        if not os.path.exists(folder):
            return []
        return [
            os.path.join(folder, f)
            for f in os.listdir(folder)
            if f.endswith(".png")
        ]

    def get_paired_screenshots(self) -> list:
        """
        Returns pairs of matching English and Arabic screenshots.
        Only returns pairs where both sides exist.
        Used by the comparator to know what to compare.
        Returns: list of dicts with 'name', 'english', 'arabic'
        """
        english_folder = os.path.join(
            self.screenshot_dir, "english"
        )
        pairs = []

        if not os.path.exists(english_folder):
            return pairs

        for filename in os.listdir(english_folder):
            if not filename.endswith(".png"):
                continue
            screen_name = filename.replace(".png", "")
            arabic_path = self.get_screenshot_path(
                screen_name, "arabic"
            )
            english_path = self.get_screenshot_path(
                screen_name, "english"
            )
            if os.path.exists(arabic_path):
                pairs.append({
                    "name": screen_name,
                    "english": english_path,
                    "arabic": arabic_path
                })

        print(f"Found {len(pairs)} paired screenshots for comparison")
        return pairs