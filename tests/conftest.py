"""Shared pytest fixtures: browser lifecycle, page creation, failure screenshots,
and a pre-authenticated page fixture for tests that don't need to test login itself.
"""
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

from pages.login_page import LoginPage
from utils.config import config


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach the outcome of each test phase to the test item.

    This lets fixtures (see `page` below) know whether the test failed so
    they can decide whether to capture a screenshot during teardown.
    """
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(scope="session")
def playwright_instance():
    """Start the Playwright driver once per test session."""
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance):
    """Launch a single browser instance shared across the whole test session."""
    browser_type = getattr(playwright_instance, config.BROWSER)
    browser = browser_type.launch(headless=config.HEADLESS, slow_mo=config.SLOW_MO)
    yield browser
    browser.close()


@pytest.fixture
def context(browser):
    """Create a fresh, isolated browser context for each test."""
    context = browser.new_context(
        viewport={
            "width": config.VIEWPORT_WIDTH,
            "height": config.VIEWPORT_HEIGHT,
        }
    )
    context.set_default_timeout(config.TIMEOUT)
    yield context
    context.close()


@pytest.fixture
def page(context, request):
    """Provide a new page per test; capture a screenshot automatically on failure."""
    page = context.new_page()
    yield page

    failed = request.node.rep_call.failed if hasattr(request.node, "rep_call") else False
    if failed:
        Path(config.SCREENSHOT_DIR).mkdir(parents=True, exist_ok=True)
        safe_name = request.node.nodeid.replace("::", "_").replace("/", "_")
        screenshot_path = f"{config.SCREENSHOT_DIR}/{safe_name}.png"
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"\nScreenshot saved for failed test: {screenshot_path}")

    page.close()


@pytest.fixture
def logged_in_page(page):
    """Provide a page that is already authenticated as the standard user.

    Use this fixture in tests that exercise inventory/cart behavior and don't
    need to re-test the login flow itself.
    """
    login_page = LoginPage(page)
    login_page.load()
    login_page.login(config.STANDARD_USER, config.PASSWORD)
    page.wait_for_url("**/inventory.html")
    return page
