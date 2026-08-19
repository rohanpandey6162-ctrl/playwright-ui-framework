"""Page Object for the SauceDemo cart and checkout flow."""
from playwright.sync_api import Page

from pages.base_page import BasePage


class CartPage(BasePage):
    """Locators and actions for the cart page (/cart.html) and checkout flow."""

    # Cart page
    CART_ITEM = ".cart_item"
    CART_ITEM_NAME = ".inventory_item_name"
    REMOVE_BUTTON = "button[data-test^='remove']"
    CHECKOUT_BUTTON = "#checkout"
    CONTINUE_SHOPPING_BUTTON = "#continue-shopping"

    # Checkout step one
    FIRST_NAME_INPUT = "#first-name"
    LAST_NAME_INPUT = "#last-name"
    POSTAL_CODE_INPUT = "#postal-code"
    CONTINUE_BUTTON = "#continue"
    CHECKOUT_ERROR = "[data-test='error']"

    # Checkout step two (overview)
    FINISH_BUTTON = "#finish"
    TOTAL_LABEL = ".summary_total_label"

    # Checkout complete
    COMPLETE_HEADER = ".complete-header"
    BACK_HOME_BUTTON = "#back-to-products"

    def __init__(self, page: Page):
        super().__init__(page)

    def load(self) -> "CartPage":
        """Navigate directly to the cart page."""
        self.navigate("/cart.html")
        return self

    def get_cart_item_names(self) -> list[str]:
        """Return the names of all products currently in the cart."""
        return self.page.locator(self.CART_ITEM_NAME).all_inner_texts()

    def get_cart_item_count(self) -> int:
        """Return the number of line items currently in the cart."""
        return self.page.locator(self.CART_ITEM).count()

    def remove_product_by_name(self, product_name: str) -> None:
        """Remove a specific product from the cart, identified by name."""
        item = self.page.locator(self.CART_ITEM).filter(has_text=product_name)
        item.locator(self.REMOVE_BUTTON).click()

    def proceed_to_checkout(self) -> None:
        """Click the checkout button to start the checkout flow."""
        self.click_element(self.CHECKOUT_BUTTON)

    def continue_shopping(self) -> None:
        """Navigate back to the inventory page from the cart."""
        self.click_element(self.CONTINUE_SHOPPING_BUTTON)

    def fill_checkout_information(
        self, first_name: str, last_name: str, postal_code: str
    ) -> None:
        """Fill out step one of checkout (customer information) and continue."""
        self.fill_text(self.FIRST_NAME_INPUT, first_name)
        self.fill_text(self.LAST_NAME_INPUT, last_name)
        self.fill_text(self.POSTAL_CODE_INPUT, postal_code)
        self.click_element(self.CONTINUE_BUTTON)

    def get_checkout_error(self) -> str:
        """Return the validation error text shown on checkout step one."""
        return self.get_text(self.CHECKOUT_ERROR)

    def get_total_label_text(self) -> str:
        """Return the total price label text from the checkout overview step."""
        return self.get_text(self.TOTAL_LABEL)

    def finish_checkout(self) -> None:
        """Click 'Finish' on the checkout overview step to complete the order."""
        self.click_element(self.FINISH_BUTTON)

    def get_complete_header(self) -> str:
        """Return the confirmation header text shown after a completed order."""
        return self.get_text(self.COMPLETE_HEADER)
