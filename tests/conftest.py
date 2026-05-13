# tests/conftest.py
# Central test configuration for DualGuard
# Handles driver setup and teardown for all tests
# Every test automatically gets a driver through fixtures here

import pytest
import allure
from utils.browserstack_helper import BrowserStackHelper
from utils.locale_switcher import LocaleSwitcher
from visual_engine.screenshot_capture import ScreenshotCapture


# ──────────────────────────────────────────
# Session Scoped Fixtures
# (Created once for the entire test session)
# ──────────────────────────────────────────

@pytest.fixture(scope="session")
def bs_helper():
    """
    Creates a single BrowserStackHelper instance
    shared across all tests in the session.
    """
    return BrowserStackHelper()


# ──────────────────────────────────────────
# English Driver Fixture
# ──────────────────────────────────────────

@pytest.fixture(scope="function")
def english_driver(bs_helper):
    """
    Creates an English locale Appium driver.
    Automatically closes after each test function.
    """
    driver = None
    try:
        print("\nCreating English driver on BrowserStack...")
        driver = bs_helper.create_driver("english")
        print("English driver ready.")
        yield driver
    except Exception as e:
        pytest.fail(f"Failed to create English driver: {e}")
    finally:
        if driver:
            print("\nClosing English driver...")
            bs_helper.quit_driver(driver)


# ──────────────────────────────────────────
# Arabic Driver Fixture
# ──────────────────────────────────────────

@pytest.fixture(scope="function")
def arabic_driver(bs_helper):
    """
    Creates an Arabic locale Appium driver.
    Automatically closes after each test function.
    """
    driver = None
    try:
        print("\nCreating Arabic driver on BrowserStack...")
        driver = bs_helper.create_driver("arabic")
        print("Arabic driver ready.")
        yield driver
    except Exception as e:
        pytest.fail(f"Failed to create Arabic driver: {e}")
    finally:
        if driver:
            print("\nClosing Arabic driver...")
            bs_helper.quit_driver(driver)


# ──────────────────────────────────────────
# Locale Switcher Fixtures
# ──────────────────────────────────────────

@pytest.fixture(scope="function")
def english_locale_switcher(english_driver):
    """
    Creates a LocaleSwitcher for English tests.
    """
    return LocaleSwitcher(english_driver)


@pytest.fixture(scope="function")
def arabic_locale_switcher(arabic_driver):
    """
    Creates a LocaleSwitcher for Arabic tests.
    """
    return LocaleSwitcher(arabic_driver)


# ──────────────────────────────────────────
# Screenshot Fixtures
# ──────────────────────────────────────────

@pytest.fixture(scope="function")
def english_screenshot(english_driver):
    """
    Creates a ScreenshotCapture instance for English tests.
    """
    return ScreenshotCapture(english_driver)


@pytest.fixture(scope="function")
def arabic_screenshot(arabic_driver):
    """
    Creates a ScreenshotCapture instance for Arabic tests.
    """
    return ScreenshotCapture(arabic_driver)


# ──────────────────────────────────────────
# Combined Fixture
# (For visual regression tests that need both)
# ──────────────────────────────────────────

@pytest.fixture(scope="function")
def dual_drivers(bs_helper):
    """
    Creates both English and Arabic drivers together.
    Used specifically by visual regression tests.
    Ensures both drivers are cleanly closed after test.
    """
    en_driver = None
    ar_driver = None
    try:
        print("\nCreating dual drivers on BrowserStack...")
        en_driver = bs_helper.create_driver("english")
        ar_driver = bs_helper.create_driver("arabic")
        print("Both drivers ready.")
        yield {
            "english": en_driver,
            "arabic": ar_driver
        }
    except Exception as e:
        pytest.fail(f"Failed to create dual drivers: {e}")
    finally:
        print("\nClosing dual drivers...")
        if en_driver:
            bs_helper.quit_driver(en_driver)
        if ar_driver:
            bs_helper.quit_driver(ar_driver)


# ──────────────────────────────────────────
# Hooks
# (Run automatically at key points)
# ──────────────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Automatically takes a screenshot when any test fails.
    Attaches it to the Allure report for debugging.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Try to get driver from any available fixture
        driver = None
        for fixture_name in [
            "english_driver",
            "arabic_driver"
        ]:
            driver = item.funcargs.get(fixture_name)
            if driver:
                break

        if driver:
            try:
                screenshot = driver.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name="failure_screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
                print(f"\nFailure screenshot captured for: {item.name}")
            except Exception as e:
                print(f"Could not capture failure screenshot: {e}")