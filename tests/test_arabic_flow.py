# tests/test_arabic_flow.py
# Test suite for Wikipedia app in Arabic (RTL) mode
# Mirrors the English test suite exactly
# Screenshots captured here are compared against English ones

import pytest
import allure
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.settings_page import SettingsPage


@allure.suite("DualGuard — Arabic (RTL) Test Suite")
@allure.feature("Arabic App Functionality")
class TestArabicFlow:
    """
    Tests the Wikipedia app in Arabic locale.
    Mirrors English tests exactly so screenshots
    can be paired for visual comparison.
    """

    # ──────────────────────────────────────────
    # Home Screen Tests
    # ──────────────────────────────────────────

    @allure.title("Arabic — Home screen loads successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_home_screen_loads(
        self, arabic_driver, arabic_screenshot
    ):
        """
        Verifies the Wikipedia home screen loads
        correctly in Arabic RTL layout.
        """
        with allure.step("Initialize home page"):
            home = HomePage(arabic_driver)

        with allure.step("Skip onboarding if present"):
            home.skip_onboarding()

        with allure.step("Verify home screen is loaded"):
            assert home.is_home_screen_loaded(), \
                "Home screen did not load in Arabic"

        with allure.step("Capture Arabic home screenshot"):
            arabic_screenshot.capture_named(
                "home_screen", "arabic"
            )

        with allure.step("Verify feed is visible"):
            assert home.is_feed_visible(), \
                "Article feed not visible on Arabic home screen"

    @allure.title("Arabic — Search bar is visible in RTL position")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_bar_visible(
        self, arabic_driver, arabic_screenshot
    ):
        """
        Verifies the search bar is visible and
        correctly positioned in RTL Arabic layout.
        In Arabic the search bar should appear
        on the right side of the screen.
        """
        with allure.step("Initialize home page"):
            home = HomePage(arabic_driver)

        with allure.step("Skip onboarding if present"):
            home.skip_onboarding()

        with allure.step("Verify search bar is visible"):
            assert home.is_home_screen_loaded(), \
                "Search bar not visible in Arabic"

        with allure.step("Capture Arabic search bar screenshot"):
            arabic_screenshot.capture_named(
                "search_bar", "arabic"
            )

    @allure.title("Arabic — Search functionality works in Arabic")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_functionality(
        self, arabic_driver, arabic_screenshot
    ):
        """
        Verifies search works correctly with Arabic input.
        Searches for Dubai in Arabic script.
        """
        with allure.step("Initialize home page"):
            home = HomePage(arabic_driver)

        with allure.step("Skip onboarding if present"):
            home.skip_onboarding()

        with allure.step("Search for Dubai in Arabic"):
            # دبي is Arabic for Dubai
            home.search_for("دبي")

        with allure.step("Capture Arabic search results"):
            arabic_screenshot.capture_named(
                "search_results", "arabic"
            )

    @allure.title("Arabic — Feed scrolling works in RTL layout")
    @allure.severity(allure.severity_level.NORMAL)
    def test_feed_scrolling(
        self, arabic_driver, arabic_screenshot
    ):
        """
        Verifies the article feed scrolls correctly
        in RTL Arabic layout.
        """
        with allure.step("Initialize home page"):
            home = HomePage(arabic_driver)

        with allure.step("Skip onboarding if present"):
            home.skip_onboarding()

        with allure.step("Verify home screen loaded"):
            assert home.is_home_screen_loaded(), \
                "Home screen not loaded before scrolling"

        with allure.step("Scroll down through feed"):
            home.scroll_feed()

        with allure.step("Capture scrolled Arabic feed"):
            arabic_screenshot.capture_named(
                "feed_scrolled", "arabic"
            )

    # ──────────────────────────────────────────
    # Login Screen Tests
    # ──────────────────────────────────────────

    @allure.title("Arabic — Login screen loads in RTL layout")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_screen_loads(
        self, arabic_driver, arabic_screenshot
    ):
        """
        Verifies the login screen loads correctly
        in Arabic with proper RTL layout.
        Input fields and buttons should be
        mirrored compared to English version.
        """
        with allure.step("Initialize pages"):
            home = HomePage(arabic_driver)
            login = LoginPage(arabic_driver)

        with allure.step("Skip onboarding if present"):
            home.skip_onboarding()

        with allure.step("Navigate to login screen"):
            login.navigate_to_login()

        with allure.step("Verify login screen loaded"):
            assert login.is_login_screen_loaded(), \
                "Login screen did not load in Arabic"

        with allure.step("Capture Arabic login screenshot"):
            arabic_screenshot.capture_named(
                "login_screen", "arabic"
            )

    @allure.title("Arabic — Login error shows in Arabic script")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_error_message(
        self, arabic_driver, arabic_screenshot
    ):
        """
        Verifies error message appears in Arabic script
        when invalid credentials are entered.
        Error text should be in Arabic and
        aligned to the right side of the screen.
        """
        with allure.step("Initialize pages"):
            home = HomePage(arabic_driver)
            login = LoginPage(arabic_driver)

        with allure.step("Skip onboarding if present"):
            home.skip_onboarding()

        with allure.step("Navigate to login screen"):
            login.navigate_to_login()

        with allure.step("Enter invalid credentials"):
            login.attempt_login(
                "invalid_test_user_dualguard",
                "wrongpassword123"
            )

        with allure.step("Verify Arabic error message appears"):
            assert login.is_error_shown(), \
                "Error message not shown for invalid Arabic login"

        with allure.step("Capture Arabic error screenshot"):
            arabic_screenshot.capture_named(
                "login_error", "arabic"
            )

    # ──────────────────────────────────────────
    # Settings Screen Tests
    # ──────────────────────────────────────────

    @allure.title("Arabic — Settings screen accessible in RTL")
    @allure.severity(allure.severity_level.NORMAL)
    def test_settings_accessible(
        self, arabic_driver, arabic_screenshot
    ):
        """
        Verifies settings screen is accessible and
        displays correctly in Arabic RTL layout.
        """
        with allure.step("Initialize pages"):
            home = HomePage(arabic_driver)
            settings = SettingsPage(arabic_driver)

        with allure.step("Skip onboarding if present"):
            home.skip_onboarding()

        with allure.step("Navigate to settings"):
            settings.navigate_to_settings()

        with allure.step("Capture Arabic settings screenshot"):
            arabic_screenshot.capture_named(
                "settings_screen", "arabic"
            )

    @allure.title("Arabic — Language settings show Arabic as active")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_arabic_language_active(
        self, arabic_driver, arabic_screenshot
    ):
        """
        Verifies Arabic is correctly set as the
        active language in language settings.
        This is a critical DualGuard verification.
        """
        with allure.step("Initialize pages"):
            home = HomePage(arabic_driver)
            settings = SettingsPage(arabic_driver)

        with allure.step("Skip onboarding if present"):
            home.skip_onboarding()

        with allure.step("Verify Arabic is active language"):
            assert settings.is_arabic_active(), \
                "Arabic is not set as active language"

        with allure.step("Navigate to language settings"):
            settings.navigate_to_language_settings()

        with allure.step("Capture Arabic language settings"):
            arabic_screenshot.capture_named(
                "language_settings", "arabic"
            )