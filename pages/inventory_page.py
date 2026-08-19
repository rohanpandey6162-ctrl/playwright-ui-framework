"""Page Object for the SauceDemo products/inventory page."""
from playwright.sync_api import Page

from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Locators and actions for the products listing page (/inventory.html)."""

    # Locators
    PAGE_TITLE = ".title"
    INVENTORY_ITEM = ".inventory_item"
    INVENTORY_ITEM_NAME = ".inventory_item_name"
    INVENTORY_ITEM_PRICE = ".inventory_item_price"
    ADD_TO_CART_BUTTON = "button[data-test^='add-to-cart']"
    REMOVE_BUTTON = "button[data-test^='remove']"
    CART_BADGE = ".shopping_cart_badge"
    CART_LINK = ".shopping_cart_link"
    SORT_DROPDOWN = "[data-test='product-sort-container']"

    def __init__(self, page: Page):
        super().__init__(page)

    def load(self) -> "InventoryPage":
        """Navigate directly to the inventory page."""
        self.navigate("/inventory.html")
        return self

    def is_loaded(self) -> bool:
        """Return True if the inventory page title is visible."""
        return self.is_visible(self.PAGE_TITLE)

    def get_product_names(self) -> list[str]:
        """Return the list of product names in current display order."""
        return self.page.locator(self.INVENTORY_ITEM_NAME).all_inner_texts()

    def get_product_prices(self) -> list[float]:
        """Return the list of product prices (as floats) in current display order."""
        raw_prices = self.page.locator(self.INVENTORY_ITEM_PRICE).all_inner_texts()
        return [float(price.replace("$", "")) for price in raw_prices]

    def sort_by(self, option_value: str) -> None:
        """Select a sorting option from the dropdown.

        Valid option_value choices on SauceDemo: 'az', 'za', 'lohi', 'hilo'.
        """
        self.page.locator(self.SORT_DROPDOWN).select_option(option_value)

    def add_product_to_cart_by_name(self, product_name: str) -> None:
        """Click the 'Add to cart' button for a specific product, identified by name."""
        item = self.page.locator(self.INVENTORY_ITEM).filter(has_text=product_name)
        item.locator(self.ADD_TO_CART_BUTTON).click()

    def remove_product_from_cart_by_name(self, product_name: str) -> None:
        """Click the 'Remove' button for a specific product, identified by name."""
        item = self.page.locator(self.INVENTORY_ITEM).filter(has_text=product_name)
        item.locator(self.REMOVE_BUTTON).click()

    def get_cart_count(self) -> int:
        """Return the number shown on the cart badge, or 0 if the badge is absent."""
        if self.is_visible(self.CART_BADGE, timeout=2_000):
            return int(self.get_text(self.CART_BADGE))
        return 0

    def go_to_cart(self) -> None:
        """Navigate to the shopping cart page."""
        self.click_element(self.CART_LINK)
