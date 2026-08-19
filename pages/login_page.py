"""Page Object for https://www.saucedemo.com login page."""
from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Locators and actions for the SauceDemo login page."""

    # Locators
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"
    ERROR_CLOSE_BUTTON = ".error-button"

    def __init__(self, page: Page):
        super().__init__(page)

    def load(self) -> "LoginPage":
        """Navigate to the login (home) page."""
        self.navigate("/")
        return self

    def login(self, username: str, password: str) -> None:
        """Fill credentials and submit the login form."""
        self.fill_text(self.USERNAME_INPUT, username)
        self.fill_text(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        """Return the text of the login error banner."""
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        """Return True if a login error banner is visible."""
        return self.is_visible(self.ERROR_MESSAGE, timeout=5_000)

    def is_login_button_visible(self) -> bool:
        """Return True if the login button is visible (i.e. still on the login page)."""
        return self.is_visible(self.LOGIN_BUTTON, timeout=5_000)
