# utils/browserstack_helper.py
# Handles all BrowserStack connections and driver setup
# Creates Appium drivers connected to real cloud devices

import requests
from appium import webdriver
from utils.config_loader import config


class BrowserStackHelper:
    """
    Manages BrowserStack connections for DualGuard.
    Creates and returns Appium drivers for English and Arabic testing.
    """

    # BrowserStack Appium server URL
    BROWSERSTACK_URL = "https://hub-cloud.browserstack.com/wd/hub"

    def __init__(self):
        self.bs_config = config.get_browserstack_credentials()
        self.username = self.bs_config.get("username")
        self.access_key = self.bs_config.get("access_key")
        self.app_url = self.bs_config.get("app_url")

    # ──────────────────────────────────────────
    # Driver Creation
    # ──────────────────────────────────────────

    def create_driver(self, locale: str):
        """
        Creates and returns an Appium driver connected to BrowserStack.
        locale: 'english' or 'arabic'
        Returns: Appium WebDriver instance
        """
        device_config = config.get_device_config(locale)
        capabilities = self._build_capabilities(device_config, locale)
        driver = webdriver.Remote(
            command_executor=self.BROWSERSTACK_URL,
            desired_capabilities=capabilities
        )
        return driver

    def _build_capabilities(
        self, device_config: dict, locale: str
    ) -> dict:
        """
        Builds the capabilities dictionary for BrowserStack.
        These tell BrowserStack exactly which device and
        settings to use.
        """
        capabilities = {
            # App to test
            "app": self.app_url,

            # Device settings
            "deviceName": device_config.get("device"),
            "platformVersion": device_config.get("os_version"),
            "platformName": "Android",

            # Locale and language settings
            "language": device_config.get("language"),
            "locale": device_config.get("locale"),

            # BrowserStack credentials
            "browserstack.user": self.username,
            "browserstack.key": self.access_key,

            # BrowserStack session settings
            "project": "DualGuard",
            "build": f"DualGuard - {locale.capitalize()} Tests",
            "name": f"{locale.capitalize()} Test Session",

            # Additional settings
            "browserstack.appium_version": "2.0.0",
            "browserstack.networkLogs": True,
            "browserstack.deviceLogs": True,
            "browserstack.debug": True,
            "newCommandTimeout": 300,
            "autoGrantPermissions": True,
        }
        return capabilities

    # ──────────────────────────────────────────
    # App Upload
    # ──────────────────────────────────────────

    def upload_app(self, apk_path: str) -> str:
        """
        Uploads the APK to BrowserStack and returns the app URL.
        This URL is used in capabilities as the 'app' value.
        apk_path: local path to the APK file
        Returns: BrowserStack app URL (bs://xxxx)
        """
        print(f"Uploading app from: {apk_path}")
        with open(apk_path, "rb") as apk_file:
            response = requests.post(
                "https://api-cloud.browserstack.com/app-automate/upload",
                files={"file": apk_file},
                auth=(self.username, self.access_key)
            )
        if response.status_code == 200:
            app_url = response.json().get("app_url")
            print(f"App uploaded successfully: {app_url}")
            return app_url
        else:
            raise Exception(
                f"App upload failed: {response.status_code} "
                f"- {response.text}"
            )

    # ──────────────────────────────────────────
    # Session Management
    # ──────────────────────────────────────────

    def quit_driver(self, driver):
        """
        Safely closes the Appium driver session.
        Always call this after tests finish.
        """
        try:
            if driver:
                driver.quit()
                print("Driver session closed successfully.")
        except Exception as e:
            print(f"Warning: Error closing driver: {e}")

    def get_session_url(self, driver) -> str:
        """
        Returns the BrowserStack session URL.
        Use this to view the test video recording.
        """
        session_id = driver.session_id
        return (
            f"https://app-automate.browserstack.com/builds/"
            f"{session_id}"
        )