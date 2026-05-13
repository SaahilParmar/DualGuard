# tests/test_english_flow.py
# Test suite for Wikipedia app in English (LTR) mode
# These tests verify core functionality in English
# and capture screenshots for visual comparison

import pytest
import allure
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.settings_page import SettingsPage


@allure.suite("DualGuard — English (LTR) Test Suite")
@allure.feature("English App Functionality")
class TestEnglishFlow:
    """
    Tests the Wikipedia app in English locale.
    Captures screenshots at each step for
    visual comparison against Arabic version.
    """

    # ──────────────────────────────────────────
    # Home Screen Tests
    # ──────────────────────────────────────────

    @allure.title("English — Home screen loads successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_home_screen_loads(
        self, english_driver, english_screenshot
    ):
        """
        Verifies the Wikipedia home screen loads
        correctly in English.
        """
        with allure.step("Initialize home page"):
            home = HomePage(english_driver)

        with allure.step("Skip onboarding if present"):
            home.skip_onboarding()

        with allure.step("Verify home screen is loaded"):
            assert home.is_home_screen_loaded(), \
                "Home screen did not load in English"

        with allure.step("Capture English home screenshot"):
            english_screenshot.capture_named(
                "home_screen", "english"
            )

        with allure.step("Verify feed is visible"):
            assert home.is_feed_visible(), \
                "Article feed not visible on English home screen"

    @allure.title("English — Search bar is visible and tappable")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_bar_visible(
        self, english_driver, english_screenshot
    ):
        """
        Verifies the search bar is visible and
        positioned correctly in LTR layout.
        """
        with allure.step("Initialize home page"):
            home = HomePage(english_driver)

        with allure.step("Skip onboarding if present"):
            home.skip_onboarding()

        with allure.step("Verify search bar is visible"):
            assert home.is_home_screen_loaded(), \
                "Search bar not visible in English"

        with allure.step("Capture search bar screenshot"):
            english_screenshot.capture_named(
                "search_bar", "english"
            )

    @allure.title("English — Search functionality works")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_functionality(
        self, english_driver, english_screenshot
    ):
        """
        Verifies search works correctly in English.
        Searches for a well known term and verifies results.
        """
        with allure.step("Initialize home page"):
            home = HomePage(english_driver)

        with allure.step("Skip onboarding if present"):
            home.skip_onboarding()

        with allure.step("Search for Wikipedia"):
            home.search_for("Dubai")

        with allure.step("Capture search results screenshot"):
            english_screenshot.capture_named(
                "search_results", "english"
            )

    @allure.title("English — Feed scrolling works")
    @allure.severity(allure.severity_level.NORMAL)
    def test_feed_scrolling(
        self, english_driver, english_screenshot
    ):
        """
        Verifies the article feed scrolls correctly
        in LTR English layout.
        """
        with allure.step("Initialize home page"):
            home = HomePage(english_driver)

        with allure.step("Skip onboarding if present"):
            home.skip_onboarding()

        with allure.step("Verify home screen loaded"):
            assert home.is_home_screen_loaded(), \
                "Home screen not loaded before scrolling"

        with allure.step("Scroll down through feed"):
            home.scroll_feed()

        with allure.step("Capture scrolled feed screenshot"):
            english_screenshot.capture_named(
                "feed_scrolled", "english"
            )

    # ──────────────────────────────────────────
    # Login Screen Tests
    # ──────────────────────────────────────────

    @allure.title("English — Login screen loads correctly")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_screen_loads(
        self, english_driver, english_screenshot
    ):
        """
        Verifies the login screen loads correctly
        in English with proper LTR layout.
        """
        with allure.step("Initialize pages"):
            home = HomePage(english_driver)
            login = LoginPage(english_driver)

        with allure.step("Skip onboarding if present"):
            home.skip_onboarding()

        with allure.step("Navigate to login screen"):
            login.navigate_to_login()

        with allure.step("Verify login screen loaded"):
            assert login.is_login_screen_loaded(), \
                "Login screen did not load in English"

        with allure.step("Capture English login screenshot"):
            english_screenshot.capture_named(
                "login_screen", "english"
            )

    @allure.title("English — Login error shows for invalid credentials")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_error_message(
        self, english_driver, english_screenshot
    ):
        """
        Verifies error message appears correctly in English
        when invalid credentials are entered.
        """
        with allure.step("Initialize pages"):
            home = HomePage(english_driver)
            login = LoginPage(english_driver)

        with allure.step("Skip onboarding if present"):
            home.skip_onboarding()

        with allure.step("Navigate to login screen"):
            login.navigate_to_login()

        with allure.step("Enter invalid credentials"):
            login.attempt_login(
                "invalid_test_user_dualguard",
                "wrongpassword123"
            )

        with allure.step("Verify error message appears"):
            assert login.is_error_shown(), \
                "Error message not shown for invalid English login"

        with allure.step("Capture error screenshot"):
            english_screenshot.capture_named(
                "login_error", "english"
            )

    # ──────────────────────────────────────────
    # Settings Screen Tests
    # ──────────────────────────────────────────

    @allure.title("English — Settings screen accessible")
    @allure.severity(allure.severity_level.NORMAL)
    def test_settings_accessible(
        self, english_driver, english_screenshot
    ):
        """
        Verifies settings screen is accessible
        and displays correctly in English.
        """
        with allure.step("Initialize pages"):
            home = HomePage(english_driver)
            settings = SettingsPage(english_driver)

        with allure.step("Skip onboarding if present"):
            home.skip_onboarding()

        with allure.step("Navigate to settings"):
            settings.navigate_to_settings()

        with allure.step("Capture settings screenshot"):
            english_screenshot.capture_named(
                "settings_screen", "english"
            )

    @allure.title("English — Language settings accessible")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_language_settings_accessible(
        self, english_driver, english_screenshot
    ):
        """
        Verifies language settings are accessible.
        Critical for DualGuard bilingual testing.
        """
        with allure.step("Initialize pages"):
            home = HomePage(english_driver)
            settings = SettingsPage(english_driver)

        with allure.step("Skip onboarding if present"):
            home.skip_onboarding()

        with allure.step("Navigate to language settings"):
            settings.navigate_to_language_settings()

        with allure.step("Capture language settings screenshot"):
            english_screenshot.capture_named(
                "language_settings", "english"
            )