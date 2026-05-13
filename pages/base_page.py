# pages/base_page.py
# Foundation class for all page objects in DualGuard
# Every page inherits these common actions

import os
import allure
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException
)
from utils.config_loader import config


class BasePage:
    """
    Base class for all page objects.
    Provides common mobile interactions used across all pages.
    """

    def __init__(self, driver):
        self.driver = driver
        self.timeout = config.get_test_config().get("timeout", 30)
        self.screenshot_dir = config.get_test_config().get(
            "screenshot_dir", "reports/screenshots"
        )

    # ──────────────────────────────────────────
    # Core Wait & Find Actions
    # ──────────────────────────────────────────

    def wait_for_element(self, locator: tuple, timeout: int = None):
        """
        Waits for an element to be visible on screen.
        locator: tuple of (AppiumBy.xxx, 'value')
        """
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except TimeoutException:
            raise TimeoutException(
                f"Element not found after {wait_time}s: {locator}"
            )

    def find_element(self, locator: tuple):
        """Finds a single element on screen."""
        try:
            return self.driver.find_element(*locator)
        except NoSuchElementException:
            raise NoSuchElementException(
                f"Element not found: {locator}"
            )

    def find_elements(self, locator: tuple):
        """Finds multiple elements on screen."""
        return self.driver.find_elements(*locator)

    # ──────────────────────────────────────────
    # Core Interaction Actions
    # ──────────────────────────────────────────

    def tap(self, locator: tuple, timeout: int = None):
        """Waits for element then taps it."""
        element = self.wait_for_element(locator, timeout)
        element.click()

    def type_text(self, locator: tuple, text: str, timeout: int = None):
        """Waits for element then types text into it."""
        element = self.wait_for_element(locator, timeout)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple, timeout: int = None) -> str:
        """Returns the text content of an element."""
        element = self.wait_for_element(locator, timeout)
        return element.text

    def is_element_visible(self, locator: tuple, timeout: int = 5) -> bool:
        """
        Returns True if element is visible, False if not.
        Uses shorter timeout so tests don't wait too long.
        """
        try:
            self.wait_for_element(locator, timeout)
            return True
        except TimeoutException:
            return False

    # ──────────────────────────────────────────
    # Scroll Actions
    # ──────────────────────────────────────────

    def scroll_down(self):
        """Scrolls down on the screen."""
        size = self.driver.get_window_size()
        start_x = size["width"] // 2
        start_y = int(size["height"] * 0.8)
        end_y = int(size["height"] * 0.2)
        self.driver.swipe(start_x, start_y, start_x, end_y, 800)

    def scroll_up(self):
        """Scrolls up on the screen."""
        size = self.driver.get_window_size()
        start_x = size["width"] // 2
        start_y = int(size["height"] * 0.2)
        end_y = int(size["height"] * 0.8)
        self.driver.swipe(start_x, start_y, start_x, end_y, 800)

    # ──────────────────────────────────────────
    # Screenshot Actions
    # ──────────────────────────────────────────

    def take_screenshot(self, name: str, locale: str = "english") -> str:
        """
        Takes a screenshot and saves it to the correct locale folder.
        Returns the full path of the saved screenshot.
        locale: 'english' or 'arabic'
        """
        folder = os.path.join(self.screenshot_dir, locale)
        os.makedirs(folder, exist_ok=True)
        filepath = os.path.join(folder, f"{name}.png")
        self.driver.save_screenshot(filepath)
        allure.attach.file(
            filepath,
            name=f"{locale}_{name}",
            attachment_type=allure.attachment_type.PNG
        )
        return filepath

    # ──────────────────────────────────────────
    # App State Actions
    # ──────────────────────────────────────────

    def get_current_activity(self) -> str:
        """Returns the current Android activity name."""
        return self.driver.current_activity

    def get_current_package(self) -> str:
        """Returns the current app package name."""
        return self.driver.current_package

    def press_back(self):
        """Presses the Android back button."""
        self.driver.back()

    def hide_keyboard(self):
        """Hides the on-screen keyboard if visible."""
        try:
            self.driver.hide_keyboard()
        except Exception:
            pass