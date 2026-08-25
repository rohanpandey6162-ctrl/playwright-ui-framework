"""Page Object for the site-wide footer component (present on authenticated app pages)."""
from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class FooterComponent(BasePage):
    """Locators and actions for the footer's social media links.

    Unlike LoginPage/InventoryPage/CartPage, the footer isn't a distinct
    URL of its own — it's a shared component rendered on every
    authenticated app page, so it has no load() method.
    """

    TWITTER_LINK = "[data-test='social-twitter']"
    FACEBOOK_LINK = "[data-test='social-facebook']"
    LINKEDIN_LINK = "[data-test='social-linkedin']"

    def __init__(self, page: Page):
        super().__init__(page)

    def get_twitter_href(self) -> str | None:
        """Return the href of the footer's Twitter/X link."""
        return self.page.locator(self.TWITTER_LINK).get_attribute("href")

    def get_facebook_href(self) -> str | None:
        """Return the href of the footer's Facebook link."""
        return self.page.locator(self.FACEBOOK_LINK).get_attribute("href")

    def get_linkedin_href(self) -> str | None:
        """Return the href of the footer's LinkedIn link."""
        return self.page.locator(self.LINKEDIN_LINK).get_attribute("href")
