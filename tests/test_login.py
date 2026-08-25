"""Login tests for SauceDemo: valid login, invalid login, and locked-out user."""
import pytest

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.config import config


@pytest.mark.smoke
@pytest.mark.login
def test_valid_login_navigates_to_inventory(page):
    """A standard user with correct credentials should land on the inventory page."""
    login_page = LoginPage(page).load()
    login_page.login(config.STANDARD_USER, config.PASSWORD)

    inventory_page = InventoryPage(page)
    page.wait_for_url("**/inventory.html")

    assert inventory_page.is_loaded()
    assert "inventory.html" in inventory_page.url


@pytest.mark.regression
@pytest.mark.login
def test_invalid_password_shows_error(page):
    """Logging in with a wrong password should keep the user on the login page with an error."""
    login_page = LoginPage(page).load()
    login_page.login(config.STANDARD_USER, "wrong_password")

    assert login_page.is_error_displayed()
    assert "Username and password do not match" in login_page.get_error_message()
    assert login_page.is_login_button_visible()


@pytest.mark.regression
@pytest.mark.login
def test_empty_credentials_shows_error(page):
    """Submitting the login form with no username should show a required-field error."""
    login_page = LoginPage(page).load()
    login_page.login("", "")

    assert login_page.is_error_displayed()
    assert "Username is required" in login_page.get_error_message()


@pytest.mark.smoke
@pytest.mark.login
def test_locked_out_user_is_denied_access(page):
    """A locked-out user should be blocked from logging in with a clear error message."""
    login_page = LoginPage(page).load()
    login_page.login(config.LOCKED_OUT_USER, config.PASSWORD)

    assert login_page.is_error_displayed()
    assert "locked out" in login_page.get_error_message().lower()
    assert login_page.is_login_button_visible()


@pytest.mark.regression
@pytest.mark.login
def test_direct_inventory_access_without_login_shows_error(page):
    """Navigating straight to the inventory URL without logging in should be rejected."""
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    inventory_page.load()

    assert not inventory_page.is_loaded()
    assert login_page.is_error_displayed()
    assert "logged in" in login_page.get_error_message().lower()
