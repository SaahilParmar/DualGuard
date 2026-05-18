# pages/settings_page.py
# Updated locators for Wikipedia app version 50583

from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class SettingsPage(BasePage):
    """
    Page object for Wikipedia settings screen.
    Handles language switching between English and Arabic.
    """

    # ──────────────────────────────────────────
    # Element Locators
    # ──────────────────────────────────────────

    # Bottom navigation - More tab
    MORE_MENU = (
        AppiumBy.XPATH,
        "//android.widget.FrameLayout[@content-desc='More']"
    )

    MORE_MENU_ALT = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='More']"
    )

    # Settings option
    SETTINGS_OPTION = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='Settings']"
    )

    # Language settings
    LANGUAGE_OPTION = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='Wikipedia languages']"
    )

    LANGUAGE_OPTION_ALT = (
        AppiumBy.XPATH,
        "//android.widget.TextView[contains(@text, 'language')]"
    )

    # Arabic language option
    ARABIC_LANGUAGE = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='العربية']"
    )

    # English language option
    ENGLISH_LANGUAGE = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='English']"
    )

    # App language setting
    APP_LANGUAGE_OPTION = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='App language']"
    )

    # Arabic indicator on home screen
    ARABIC_INDICATOR = (
        AppiumBy.XPATH,
        "//android.widget.TextView[contains(@text, 'ويكيبيديا')]"
    )

    # ──────────────────────────────────────────
    # Navigation Actions
    # ──────────────────────────────────────────

    def navigate_to_settings(self):
        """Navigates to settings screen."""
        import time
        if self.is_element_visible(self.MORE_MENU, timeout=10):
            self.tap(self.MORE_MENU)
        elif self.is_element_visible(self.MORE_MENU_ALT, timeout=10):
            self.tap(self.MORE_MENU_ALT)
        time.sleep(2)
        if self.is_element_visible(self.SETTINGS_OPTION, timeout=10):
            self.tap(self.SETTINGS_OPTION)
        time.sleep(2)

    def navigate_to_language_settings(self):
        """Navigates to language settings."""
        self.navigate_to_settings()
        if self.is_element_visible(self.LANGUAGE_OPTION, timeout=10):
            self.tap(self.LANGUAGE_OPTION)
        elif self.is_element_visible(
            self.LANGUAGE_OPTION_ALT, timeout=10
        ):
            self.tap(self.LANGUAGE_OPTION_ALT)

    # ──────────────────────────────────────────
    # Language Switching
    # ──────────────────────────────────────────

    def switch_to_arabic(self):
        """Switches app language to Arabic."""
        self.navigate_to_language_settings()
        if self.is_element_visible(
            self.APP_LANGUAGE_OPTION, timeout=5
        ):
            self.tap(self.APP_LANGUAGE_OPTION)
        if self.is_element_visible(self.ARABIC_LANGUAGE, timeout=5):
            self.tap(self.ARABIC_LANGUAGE)

    def switch_to_english(self):
        """Switches app language to English."""
        self.navigate_to_language_settings()
        if self.is_element_visible(
            self.APP_LANGUAGE_OPTION, timeout=5
        ):
            self.tap(self.APP_LANGUAGE_OPTION)
        if self.is_element_visible(self.ENGLISH_LANGUAGE, timeout=5):
            self.tap(self.ENGLISH_LANGUAGE)

    # ──────────────────────────────────────────
    # Verification
    # ──────────────────────────────────────────

    def is_arabic_active(self) -> bool:
        """Returns True if Arabic is active language."""
        return self.is_element_visible(
            self.ARABIC_INDICATOR, timeout=5
        )

    def is_english_active(self) -> bool:
        """Returns True if English is active language."""
        english_indicator = (
            AppiumBy.XPATH,
            "//android.widget.TextView[contains(@text, 'Wikipedia')]"
        )
        return self.is_element_visible(english_indicator, timeout=5)

    def take_settings_screenshot(self, locale: str) -> str:
        """Takes a screenshot of settings screen."""
        return self.take_screenshot("settings_screen", locale)