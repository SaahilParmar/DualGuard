# pages/settings_page.py
# Represents the Wikipedia app settings screen
# Most importantly handles language switching between English and Arabic

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

    # More menu button in bottom navigation
    MORE_MENU = (
        AppiumBy.ID,
        "org.wikipedia:id/nav_more_container"
    )

    # Settings option in more menu
    SETTINGS_OPTION = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='Settings']"
    )

    # Language settings option
    LANGUAGE_OPTION = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='Wikipedia languages']"
    )

    # Add language button
    ADD_LANGUAGE_BUTTON = (
        AppiumBy.ID,
        "org.wikipedia:id/wiki_language_title"
    )

    # Arabic language option in language list
    ARABIC_LANGUAGE = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='العربية']"
    )

    # English language option in language list
    ENGLISH_LANGUAGE = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='English']"
    )

    # App language setting
    APP_LANGUAGE_OPTION = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='App language']"
    )

    # System default language option
    SYSTEM_DEFAULT = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='System default']"
    )

    # ──────────────────────────────────────────
    # Navigation Actions
    # ──────────────────────────────────────────

    def navigate_to_settings(self):
        """
        Navigates from home screen to settings.
        Taps More menu then Settings option.
        """
        self.tap(self.MORE_MENU)
        self.tap(self.SETTINGS_OPTION)

    def navigate_to_language_settings(self):
        """Navigates to the language settings screen."""
        self.navigate_to_settings()
        self.tap(self.LANGUAGE_OPTION)

    # ──────────────────────────────────────────
    # Language Switching Actions
    # ──────────────────────────────────────────

    def switch_to_arabic(self):
        """
        Switches the app language to Arabic.
        Navigates to language settings and selects Arabic.
        """
        self.navigate_to_language_settings()
        if self.is_element_visible(self.APP_LANGUAGE_OPTION, timeout=5):
            self.tap(self.APP_LANGUAGE_OPTION)
        if self.is_element_visible(self.ARABIC_LANGUAGE, timeout=5):
            self.tap(self.ARABIC_LANGUAGE)
        else:
            self._add_arabic_language()

    def switch_to_english(self):
        """
        Switches the app language back to English.
        Navigates to language settings and selects English.
        """
        self.navigate_to_language_settings()
        if self.is_element_visible(self.APP_LANGUAGE_OPTION, timeout=5):
            self.tap(self.APP_LANGUAGE_OPTION)
        self.tap(self.ENGLISH_LANGUAGE)

    def _add_arabic_language(self):
        """
        Private method — adds Arabic if not already in language list.
        Called automatically by switch_to_arabic if needed.
        """
        if self.is_element_visible(self.ADD_LANGUAGE_BUTTON, timeout=5):
            self.tap(self.ADD_LANGUAGE_BUTTON)
            self.scroll_down()
            self.tap(self.ARABIC_LANGUAGE)

    # ──────────────────────────────────────────
    # Verification Actions
    # ──────────────────────────────────────────

    def is_arabic_active(self) -> bool:
        """
        Returns True if Arabic is currently the active language.
        Checks for Arabic text in the UI.
        """
        arabic_indicator = (
            AppiumBy.XPATH,
            "//android.widget.TextView[contains(@text, 'ويكيبيديا')]"
        )
        return self.is_element_visible(arabic_indicator, timeout=5)

    def is_english_active(self) -> bool:
        """
        Returns True if English is currently the active language.
        Checks for English text in the UI.
        """
        english_indicator = (
            AppiumBy.XPATH,
            "//android.widget.TextView[contains(@text, 'Wikipedia')]"
        )
        return self.is_element_visible(english_indicator, timeout=5)

    def take_settings_screenshot(self, locale: str) -> str:
        """
        Takes a screenshot of the settings screen.
        locale: 'english' or 'arabic'
        Returns the screenshot file path.
        """
        return self.take_screenshot("settings_screen", locale)