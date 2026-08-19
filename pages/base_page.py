"""Base Page Object: reusable, low-level browser interactions shared by all pages.

Every concrete page object (LoginPage, InventoryPage, CartPage, ...) inherits
from BasePage so that common actions like clicking, typing and waiting are
implemented once and reused everywhere. All waits rely on Playwright's
built-in auto-waiting instead of explicit sleeps.
"""
from __future__ import annotations

from pathlib import Path

from playwright.sync_api import Page

from utils.config import config


class BasePage:
    """Common functionality wrapped around a Playwright `Page` instance."""

    def __init__(self, page: Page):
        self.page = page
        self.base_url = config.BASE_URL
        self.timeout = config.TIMEOUT

    def navigate(self, path: str = "") -> None:
        """Navigate to `base_url + path`."""
        url = f"{self.base_url}{path}"
        self.page.goto(url, timeout=config.NAVIGATION_TIMEOUT)

    def click_element(self, selector: str) -> None:
        """Wait for an element to be actionable, then click it."""
        locator = self.page.locator(selector)
        locator.wait_for(state="visible", timeout=self.timeout)
        locator.click()

    def fill_text(self, selector: str, text: str) -> None:
        """Clear and type text into an input, waiting for it to be visible first."""
        locator = self.page.locator(selector)
        locator.wait_for(state="visible", timeout=self.timeout)
        locator.fill(text)

    def get_text(self, selector: str) -> str:
        """Return the trimmed inner text of the first matching element."""
        locator = self.page.locator(selector)
        locator.wait_for(state="visible", timeout=self.timeout)
        return locator.inner_text().strip()

    def is_visible(self, selector: str, timeout: int | None = None) -> bool:
        """Return True if the element becomes visible within `timeout`, else False."""
        try:
            self.page.locator(selector).wait_for(
                state="visible", timeout=timeout or self.timeout
            )
            return True
        except Exception:
            return False

    def wait_for_element(self, selector: str, state: str = "visible") -> None:
        """Wait for an element to reach the given state (visible/hidden/attached/detached)."""
        self.page.locator(selector).wait_for(state=state, timeout=self.timeout)

    def take_screenshot(self, name: str) -> str:
        """Capture a full-page screenshot into the configured screenshots directory."""
        Path(config.SCREENSHOT_DIR).mkdir(parents=True, exist_ok=True)
        file_path = f"{config.SCREENSHOT_DIR}/{name}.png"
        self.page.screenshot(path=file_path, full_page=True)
        return file_path

    @property
    def url(self) -> str:
        """Current page URL."""
        return self.page.url

    @property
    def title(self) -> str:
        """Current page title."""
        return self.page.title()
