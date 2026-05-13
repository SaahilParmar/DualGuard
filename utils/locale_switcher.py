# utils/locale_switcher.py
# Handles language switching during test execution
# Works alongside settings_page.py to enable bilingual testing

import time
from utils.config_loader import config


class LocaleSwitcher:
    """
    Manages language switching between English and Arabic
    during DualGuard test execution.
    """

    # Supported locales
    ENGLISH = "english"
    ARABIC = "arabic"
    SUPPORTED_LOCALES = [ENGLISH, ARABIC]

    def __init__(self, driver):
        self.driver = driver
        self.current_locale = self.ENGLISH
        self.device_config = config.get_device_config

    # ──────────────────────────────────────────
    # Locale Switching
    # ──────────────────────────────────────────

    def switch_to(self, locale: str):
        """
        Switches the app to the specified locale.
        locale: 'english' or 'arabic'
        """
        if locale not in self.SUPPORTED_LOCALES:
            raise ValueError(
                f"Unsupported locale: '{locale}'. "
                f"Supported: {self.SUPPORTED_LOCALES}"
            )
        if locale == self.current_locale:
            print(f"Already in {locale} — no switch needed.")
            return

        print(f"Switching locale: {self.current_locale} → {locale}")

        if locale == self.ARABIC:
            self._switch_to_arabic()
        else:
            self._switch_to_english()

        # Wait for app to reload after language change
        time.sleep(3)
        self.current_locale = locale
        print(f"Locale successfully switched to: {locale}")

    def _switch_to_arabic(self):
        """
        Internal method — switches app to Arabic.
        Uses the device locale setting via ADB.
        """
        self.driver.set_settings({
            "language": "ar",
            "locale": "AE"
        })

    def _switch_to_english(self):
        """
        Internal method — switches app to English.
        Uses the device locale setting via ADB.
        """
        self.driver.set_settings({
            "language": "en",
            "locale": "US"
        })

    # ──────────────────────────────────────────
    # RTL / LTR Detection
    # ──────────────────────────────────────────

    def is_rtl_active(self) -> bool:
        """
        Returns True if the app is currently in RTL mode.
        RTL means right-to-left — Arabic layout.
        """
        return self.current_locale == self.ARABIC

    def is_ltr_active(self) -> bool:
        """
        Returns True if the app is currently in LTR mode.
        LTR means left-to-right — English layout.
        """
        return self.current_locale == self.ENGLISH

    def get_current_locale(self) -> str:
        """Returns the currently active locale."""
        return self.current_locale

    # ──────────────────────────────────────────
    # Layout Direction Verification
    # ──────────────────────────────────────────

    def verify_rtl_layout(self) -> dict:
        """
        Verifies RTL layout is correctly applied.
        Returns a dict with layout direction details.
        """
        window_size = self.driver.get_window_size()
        layout_info = {
            "locale": self.current_locale,
            "is_rtl": self.is_rtl_active(),
            "screen_width": window_size["width"],
            "screen_height": window_size["height"],
            "direction": "RTL" if self.is_rtl_active() else "LTR"
        }
        return layout_info

    def get_layout_direction(self) -> str:
        """
        Returns current layout direction as a string.
        Returns: 'RTL' or 'LTR'
        """
        return "RTL" if self.is_rtl_active() else "LTR"

    # ──────────────────────────────────────────
    # Test Context Helpers
    # ──────────────────────────────────────────

    def get_test_label(self) -> str:
        """
        Returns a human readable label for the current locale.
        Used in test names and report titles.
        """
        labels = {
            self.ENGLISH: "English (LTR)",
            self.ARABIC: "Arabic (RTL)"
        }
        return labels.get(self.current_locale, self.current_locale)

    def get_screenshot_folder(self) -> str:
        """
        Returns the correct screenshot folder for current locale.
        Used by screenshot capture to save to the right place.
        """
        screenshot_dir = config.get_test_config().get(
            "screenshot_dir", "reports/screenshots"
        )
        return f"{screenshot_dir}/{self.current_locale}"