# pages/home_page.py
# Represents the Wikipedia app home screen
# Updated to handle Wikipedia 25th birthday promotional popup

from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class HomePage(BasePage):
    """
    Page object for Wikipedia home screen.
    Contains all interactions specific to the home page.
    """

    # ──────────────────────────────────────────
    # Element Locators
    # ──────────────────────────────────────────

    # Search bar - multiple fallback locators
    SEARCH_BAR = (
        AppiumBy.ID,
        "org.wikipedia:id/search_container"
    )

    SEARCH_BAR_ALT = (
        AppiumBy.XPATH,
        "//android.widget.TextView[contains(@text, 'Search')]"
    )

    # Main feed container
    FEED_CONTAINER = (
        AppiumBy.ID,
        "org.wikipedia:id/feed_view"
    )

    FEED_CONTAINER_ALT = (
        AppiumBy.XPATH,
        "//androidx.recyclerview.widget.RecyclerView"
    )

    # Skip button on onboarding screen
    SKIP_BUTTON = (
        AppiumBy.ID,
        "org.wikipedia:id/fragment_onboarding_skip_button"
    )

    # Continue button on onboarding
    CONTINUE_BUTTON = (
        AppiumBy.ID,
        "org.wikipedia:id/fragment_onboarding_forward_button"
    )

    # Accept button for privacy/terms
    ACCEPT_BUTTON = (
        AppiumBy.XPATH,
        "//android.widget.Button[contains(@text, 'Accept')]"
    )

    # Got it button
    GOT_IT_BUTTON = (
        AppiumBy.XPATH,
        "//android.widget.Button[contains(@text, 'Got it')]"
    )

    # Wikipedia 25th birthday popup close button
    BIRTHDAY_CLOSE_1 = (
        AppiumBy.XPATH,
        "//android.widget.ImageButton[@content-desc='Close']"
    )

    BIRTHDAY_CLOSE_2 = (
        AppiumBy.XPATH,
        "//android.widget.ImageButton[@content-desc='close']"
    )

    BIRTHDAY_CLOSE_3 = (
        AppiumBy.XPATH,
        "//*[@content-desc='Close']"
    )

    BIRTHDAY_CLOSE_4 = (
        AppiumBy.XPATH,
        "//*[@content-desc='close']"
    )

    BIRTHDAY_CLOSE_5 = (
        AppiumBy.XPATH,
        "//android.widget.ImageButton[1]"
    )

    # ──────────────────────────────────────────
    # Actions
    # ──────────────────────────────────────────

    def skip_onboarding(self):
        """
        Handles all onboarding, permission, and promotional
        screens including the Wikipedia 25th birthday popup.
        Tries multiple approaches to get past all dialogs.
        """
        import time

        # Wait for app to fully launch
        time.sleep(5)

        # Handle Wikipedia 25th birthday challenge popup
        # Try all known close button locators
        birthday_locators = [
            self.BIRTHDAY_CLOSE_1,
            self.BIRTHDAY_CLOSE_2,
            self.BIRTHDAY_CLOSE_3,
            self.BIRTHDAY_CLOSE_4,
            self.BIRTHDAY_CLOSE_5,
        ]

        for locator in birthday_locators:
            if self.is_element_visible(locator, timeout=3):
                self.tap(locator)
                print("Dismissed birthday challenge popup")
                time.sleep(2)
                break

        # If popup still showing tap X by screen coordinates
        # X button is in top right corner of popup
        if not self.is_element_visible(self.SEARCH_BAR, timeout=5):
            try:
                size = self.driver.get_window_size()
                x = int(size["width"] * 0.92)
                y = int(size["height"] * 0.08)
                self.driver.tap([(x, y)])
                print("Tapped close by coordinates")
                time.sleep(2)
            except Exception:
                pass

        # Try skip button for standard onboarding
        if self.is_element_visible(self.SKIP_BUTTON, timeout=5):
            self.tap(self.SKIP_BUTTON)
            time.sleep(2)

        # Try accept button
        if self.is_element_visible(self.ACCEPT_BUTTON, timeout=5):
            self.tap(self.ACCEPT_BUTTON)
            time.sleep(2)

        # Try got it button
        if self.is_element_visible(self.GOT_IT_BUTTON, timeout=5):
            self.tap(self.GOT_IT_BUTTON)
            time.sleep(2)

        # Try continue button multiple times for multi-step onboarding
        for _ in range(3):
            if self.is_element_visible(
                self.CONTINUE_BUTTON, timeout=3
            ):
                self.tap(self.CONTINUE_BUTTON)
                time.sleep(2)

    def is_home_screen_loaded(self) -> bool:
        """
        Returns True if the home screen has loaded.
        Tries multiple locators as fallbacks.
        """
        if self.is_element_visible(self.SEARCH_BAR, timeout=15):
            return True
        if self.is_element_visible(self.SEARCH_BAR_ALT, timeout=10):
            return True
        if self.is_element_visible(self.FEED_CONTAINER, timeout=10):
            return True
        if self.is_element_visible(
            self.FEED_CONTAINER_ALT, timeout=10
        ):
            return True
        return False

    def tap_search_bar(self):
        """Taps the search bar to open search screen."""
        if self.is_element_visible(self.SEARCH_BAR, timeout=10):
            self.tap(self.SEARCH_BAR)
        else:
            self.tap(self.SEARCH_BAR_ALT)

    def search_for(self, query: str):
        """
        Taps search bar and types a search query.
        """
        self.tap_search_bar()
        import time
        time.sleep(2)
        search_input = (
            AppiumBy.ID,
            "org.wikipedia:id/search_src_text"
        )
        search_input_alt = (
            AppiumBy.XPATH,
            "//android.widget.EditText"
        )
        if self.is_element_visible(search_input, timeout=10):
            self.type_text(search_input, query)
        else:
            self.type_text(search_input_alt, query)

    def is_feed_visible(self) -> bool:
        """Returns True if the main article feed is visible."""
        if self.is_element_visible(self.FEED_CONTAINER, timeout=10):
            return True
        return self.is_element_visible(
            self.FEED_CONTAINER_ALT, timeout=10
        )

    def scroll_feed(self):
        """Scrolls down through the article feed."""
        self.scroll_down()

    def take_home_screenshot(self, locale: str) -> str:
        """Takes a screenshot of the home screen."""
        return self.take_screenshot("home_screen", locale)