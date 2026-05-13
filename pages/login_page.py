# pages/login_page.py
# Represents the Wikipedia app login screen
# Demonstrates bilingual form input testing

from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Page object for Wikipedia login screen.
    Tests form interactions in both English and Arabic.
    """

    # ──────────────────────────────────────────
    # Element Locators
    # ──────────────────────────────────────────

    # Login button on home screen
    LOGIN_BUTTON = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='Log in']"
    )

    # Username input field
    USERNAME_FIELD = (
        AppiumBy.ID,
        "org.wikipedia:id/login_username_text"
    )

    # Password input field
    PASSWORD_FIELD = (
        AppiumBy.ID,
        "org.wikipedia:id/login_password_text"
    )

    # Submit login button
    SUBMIT_BUTTON = (
        AppiumBy.ID,
        "org.wikipedia:id/login_button"
    )

    # Error message container
    ERROR_MESSAGE = (
        AppiumBy.ID,
        "org.wikipedia:id/textinput_error"
    )

    # Login screen title
    LOGIN_TITLE = (
        AppiumBy.ID,
        "org.wikipedia:id/login_title"
    )

    # Create account link
    CREATE_ACCOUNT_LINK = (
        AppiumBy.ID,
        "org.wikipedia:id/login_create_account_button"
    )

    # Forgot password link
    FORGOT_PASSWORD_LINK = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='Forgot password?']"
    )

    # ──────────────────────────────────────────
    # Navigation Actions
    # ──────────────────────────────────────────

    def navigate_to_login(self):
        """
        Navigates to the login screen from the more menu.
        """
        more_menu = (
            AppiumBy.ID,
            "org.wikipedia:id/nav_more_container"
        )
        self.tap(more_menu)
        self.tap(self.LOGIN_BUTTON)

    def is_login_screen_loaded(self) -> bool:
        """Returns True if login screen has fully loaded."""
        return self.is_element_visible(self.LOGIN_TITLE, timeout=15)

    # ──────────────────────────────────────────
    # Form Interaction Actions
    # ──────────────────────────────────────────

    def enter_username(self, username: str):
        """Types username into the username field."""
        self.type_text(self.USERNAME_FIELD, username)
        self.hide_keyboard()

    def enter_password(self, password: str):
        """Types password into the password field."""
        self.type_text(self.PASSWORD_FIELD, password)
        self.hide_keyboard()

    def tap_login_button(self):
        """Taps the login submit button."""
        self.tap(self.SUBMIT_BUTTON)

    def attempt_login(self, username: str, password: str):
        """
        Complete login flow — enters credentials and submits.
        username: account username
        password: account password
        """
        self.enter_username(username)
        self.enter_password(password)
        self.tap_login_button()

    # ──────────────────────────────────────────
    # Validation Actions
    # ──────────────────────────────────────────

    def is_error_shown(self) -> bool:
        """Returns True if an error message is visible."""
        return self.is_element_visible(self.ERROR_MESSAGE, timeout=5)

    def get_error_message(self) -> str:
        """Returns the text of the error message if shown."""
        if self.is_error_shown():
            return self.get_text(self.ERROR_MESSAGE)
        return ""

    def is_create_account_visible(self) -> bool:
        """Returns True if the create account link is visible."""
        return self.is_element_visible(self.CREATE_ACCOUNT_LINK)

    def is_forgot_password_visible(self) -> bool:
        """Returns True if the forgot password link is visible."""
        return self.is_element_visible(self.FORGOT_PASSWORD_LINK)

    # ──────────────────────────────────────────
    # Screenshot Actions
    # ──────────────────────────────────────────

    def take_login_screenshot(self, locale: str) -> str:
        """
        Takes a screenshot of the login screen.
        locale: 'english' or 'arabic'
        Returns the screenshot file path.
        """
        return self.take_screenshot("login_screen", locale)

    def take_error_screenshot(self, locale: str) -> str:
        """
        Takes a screenshot when an error is displayed.
        locale: 'english' or 'arabic'
        Returns the screenshot file path.
        """
        return self.take_screenshot("login_error", locale)