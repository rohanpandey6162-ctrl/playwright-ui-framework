"""Cart tests: adding/removing items and the full checkout flow."""
import pytest

from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


@pytest.mark.smoke
@pytest.mark.cart
def test_added_item_appears_in_cart(logged_in_page):
    """A product added from the inventory page should appear in the cart with the same name."""
    inventory_page = InventoryPage(logged_in_page)
    inventory_page.add_product_to_cart_by_name("Sauce Labs Backpack")
    inventory_page.go_to_cart()

    cart_page = CartPage(logged_in_page)
    assert cart_page.get_cart_item_count() == 1
    assert "Sauce Labs Backpack" in cart_page.get_cart_item_names()


@pytest.mark.regression
@pytest.mark.cart
def test_remove_item_from_cart_page(logged_in_page):
    """Removing an item on the cart page should leave the cart empty."""
    inventory_page = InventoryPage(logged_in_page)
    inventory_page.add_product_to_cart_by_name("Sauce Labs Bike Light")
    inventory_page.go_to_cart()

    cart_page = CartPage(logged_in_page)
    cart_page.remove_product_by_name("Sauce Labs Bike Light")

    assert cart_page.get_cart_item_count() == 0


@pytest.mark.regression
@pytest.mark.cart
def test_continue_shopping_returns_to_inventory(logged_in_page):
    """Clicking 'Continue Shopping' from the cart should navigate back to the inventory page."""
    inventory_page = InventoryPage(logged_in_page)
    inventory_page.go_to_cart()

    cart_page = CartPage(logged_in_page)
    cart_page.continue_shopping()

    assert "inventory.html" in inventory_page.url


@pytest.mark.smoke
@pytest.mark.cart
def test_full_checkout_flow_completes_order(logged_in_page):
    """A user should be able to add an item, check out, and see the order confirmation."""
    inventory_page = InventoryPage(logged_in_page)
    inventory_page.add_product_to_cart_by_name("Sauce Labs Backpack")
    inventory_page.go_to_cart()

    cart_page = CartPage(logged_in_page)
    cart_page.proceed_to_checkout()
    cart_page.fill_checkout_information("Jane", "Doe", "94107")

    assert "Total" in cart_page.get_total_label_text()

    cart_page.finish_checkout()

    assert cart_page.get_complete_header() == "Thank you for your order!"


@pytest.mark.regression
@pytest.mark.cart
def test_checkout_requires_first_name(logged_in_page):
    """Attempting checkout without a first name should show a validation error."""
    inventory_page = InventoryPage(logged_in_page)
    inventory_page.add_product_to_cart_by_name("Sauce Labs Backpack")
    inventory_page.go_to_cart()

    cart_page = CartPage(logged_in_page)
    cart_page.proceed_to_checkout()
    cart_page.fill_checkout_information("", "Doe", "94107")

    assert "First Name is required" in cart_page.get_checkout_error()
