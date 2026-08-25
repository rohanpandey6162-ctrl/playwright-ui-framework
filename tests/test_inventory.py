"""Inventory/product listing tests: sorting and adding items to the cart."""
import pytest

from pages.inventory_page import InventoryPage


@pytest.mark.smoke
def test_inventory_loads_six_products(logged_in_page):
    """The inventory page should display all six SauceDemo demo products."""
    inventory_page = InventoryPage(logged_in_page)

    assert inventory_page.is_loaded()
    assert len(inventory_page.get_product_names()) == 6


@pytest.mark.regression
def test_sort_products_price_low_to_high(logged_in_page):
    """Sorting by 'Price (low to high)' should order products ascending by price."""
    inventory_page = InventoryPage(logged_in_page)
    inventory_page.sort_by("lohi")

    prices = inventory_page.get_product_prices()
    assert prices == sorted(prices)


@pytest.mark.regression
def test_sort_products_name_z_to_a(logged_in_page):
    """Sorting by 'Name (Z to A)' should order product names in reverse alphabetical order."""
    inventory_page = InventoryPage(logged_in_page)
    inventory_page.sort_by("za")

    names = inventory_page.get_product_names()
    assert names == sorted(names, reverse=True)


@pytest.mark.regression
def test_sort_products_price_high_to_low(logged_in_page):
    """Sorting by 'Price (high to low)' should order products descending by price."""
    inventory_page = InventoryPage(logged_in_page)
    inventory_page.sort_by("hilo")

    prices = inventory_page.get_product_prices()
    assert prices == sorted(prices, reverse=True)


@pytest.mark.smoke
@pytest.mark.cart
def test_add_single_product_updates_cart_badge(logged_in_page):
    """Adding a product to the cart should update the cart badge count to 1."""
    inventory_page = InventoryPage(logged_in_page)
    inventory_page.add_product_to_cart_by_name("Sauce Labs Backpack")

    assert inventory_page.get_cart_count() == 1


@pytest.mark.regression
@pytest.mark.cart
def test_add_multiple_products_updates_cart_badge(logged_in_page):
    """Adding multiple products should accumulate the cart badge count correctly."""
    inventory_page = InventoryPage(logged_in_page)
    inventory_page.add_product_to_cart_by_name("Sauce Labs Backpack")
    inventory_page.add_product_to_cart_by_name("Sauce Labs Bike Light")

    assert inventory_page.get_cart_count() == 2


@pytest.mark.regression
@pytest.mark.cart
def test_remove_product_from_inventory_page(logged_in_page):
    """Removing a product from the inventory page should decrement the cart badge."""
    inventory_page = InventoryPage(logged_in_page)
    inventory_page.add_product_to_cart_by_name("Sauce Labs Backpack")
    assert inventory_page.get_cart_count() == 1

    inventory_page.remove_product_from_cart_by_name("Sauce Labs Backpack")
    assert inventory_page.get_cart_count() == 0
