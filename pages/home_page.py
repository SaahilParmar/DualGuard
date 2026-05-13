# pages/home_page.py
# Represents the Wikipedia app home screen
# Inherits all common actions from BasePage

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

    # Search bar at the top of home screen
    SEARCH_BAR = (
        AppiumBy.ACCESSIBILITY_ID,
        "Search Wikipedia"
    )

    # Main feed container
    FEED_CONTAINER = (
        AppiumBy.ID,
        "org.wikipedia:id/fragment_feed_feed"
    )

    # Top read articles section
    TOP_READ_SECTION = (
        AppiumBy.ID,
        "org.wikipedia:id/view_list_card_header_title"
    )

    # Navigation menu button
    NAV_MORE_BUTTON = (
        AppiumBy.ID,
        "org.wikipedia:id/nav_more_container"
    )

    # Skip button on onboarding screen
    SKIP_BUTTON = (
        AppiumBy.ID,
        "org.wikipedia:id/fragment_onboarding_skip_button"
    )

    # Continue button on onboarding screen
    CONTINUE_BUTTON = (
        AppiumBy.ID,
        "org.wikipedia:id/fragment_onboarding_forward_button"
    )

    # ──────────────────────────────────────────
    # Actions
    # ──────────────────────────────────────────

    def skip_onboarding(self):
        """
        Skips the onboarding screen if it appears.
        Safe to call even if onboarding is not showing.
        """
        if self.is_element_visible(self.SKIP_BUTTON, timeout=5):
            self.tap(self.SKIP_BUTTON)

    def is_home_screen_loaded(self) -> bool:
        """
        Returns True if the home screen has fully loaded.
        Checks for the search bar which is always present.
        """
        return self.is_element_visible(self.SEARCH_BAR, timeout=15)

    def tap_search_bar(self):
        """Taps the search bar to open the search screen."""
        self.tap(self.SEARCH_BAR)

    def search_for(self, query: str):
        """
        Taps the search bar and types a search query.
        query: the text to search for
        """
        self.tap_search_bar()
        self.type_text(
            (AppiumBy.ID, "org.wikipedia:id/search_src_text"),
            query
        )

    def is_feed_visible(self) -> bool:
        """Returns True if the main article feed is visible."""
        return self.is_element_visible(self.FEED_CONTAINER)

    def scroll_feed(self):
        """Scrolls down through the article feed."""
        self.scroll_down()

    def take_home_screenshot(self, locale: str) -> str:
        """
        Takes a screenshot of the home screen.
        locale: 'english' or 'arabic'
        Returns the screenshot file path.
        """
        return self.take_screenshot("home_screen", locale)