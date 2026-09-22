from src.common.base.base_page import BasePage
from src.banks.wio.locators.currency_locators import WioCurrencyLocators as WioCurrencyLocators

class CurrencyPage(BasePage):
    def __init__(self, page, module_name="Currency"):
        super().__init__(page, module_name=module_name)
        self._dispatch = {
            "wio": (self._currency_standard, WioCurrencyLocators),
        }

    def navigate_to_currency(self, bank: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        self.hover_by_getbytext(loc.menu_configuration, "Configuration menu")
        self.click_by_locator(loc.menu_currency, "Currency submenu")

    def click_add_button(self, bank: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        self.click_by_locator(loc.add_button, "Add button")

    def fill_currency_form(self, bank: str, data: dict) -> None:
        method, loc = self._dispatch[bank.lower()]
        method(loc, data)

    def _currency_standard(self, loc, data: dict) -> None:
        # Fill Currency Code (if provided and not read-only)
        if "Currency Code" in data and data["Currency Code"]:
            self.fill_by_locator(loc.currency_code_input, data["Currency Code"], "Currency Code")
        # Fill Currency Description
        if "Currency Description" in data:
            self.fill_by_locator(loc.currency_description_input, data["Currency Description"], "Currency Description")
        # Fill Minor Digits
        if "Minor Digits" in data:
            self.fill_by_locator(loc.minor_digits_input, data["Minor Digits"], "Minor Digits")
        # Fill Currency Symbol
        if "Currency Symbol" in data:
            self.fill_by_locator(loc.currency_symbol_input, data["Currency Symbol"], "Currency Symbol")

    def click_save_button(self, bank: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        self.click_by_locator(loc.save_button, "Save button")

    def click_cancel_button(self, bank: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        self.click_by_locator(loc.cancel_button, "Cancel button")

    def assert_currency_message(self, bank: str, expected_message: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        self.assert_text(self.locator(loc.message_container), expected_message, "Response Message")

    def click_view_button(self, bank: str, currency_code: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        view_button_locator = loc.view_button.format(currency_code=currency_code)
        self.click_by_locator(view_button_locator, f"View button for currency {currency_code}")

    def assert_view_currency_details(self, bank: str, data: dict) -> None:
        _, loc = self._dispatch[bank.lower()]
        if "Currency Code" in data:
            self.assert_text(self.locator(loc.view_currency_code), data["Currency Code"], "Currency Code")
        if "Currency Description" in data:
            self.assert_text(self.locator(loc.view_currency_description), data["Currency Description"], "Currency Description")
        if "Minor Digits" in data:
            self.assert_text(self.locator(loc.view_minor_digits), data["Minor Digits"], "Minor Digits")
        if "Currency Symbol" in data:
            self.assert_text(self.locator(loc.view_currency_symbol), data["Currency Symbol"], "Currency Symbol")
        # Status might not be in data, but we can assert it's present if needed

    def click_back_button(self, bank: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        self.click_by_locator(loc.back_button, "Back button")

    def click_edit_button(self, bank: str, currency_code: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        edit_button_locator = loc.edit_button.format(currency_code=currency_code)
        self.click_by_locator(edit_button_locator, f"Edit button for currency {currency_code}")

    def click_checkbox(self, bank: str, currency_code: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        checkbox_locator = loc.checkbox.format(currency_code=currency_code)
        self.click_by_locator(checkbox_locator, f"Checkbox for currency {currency_code}")

    def click_change_status_button(self, bank: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        self.click_by_locator(loc.change_status_button, "Change Status button")

    # Method to handle confirmation dialog if any (not specified in scenario, but common)
    def confirm_change_status(self, bank: str) -> None:
        # Assuming a simple confirmation dialog with OK button
        # We'll use a generic locator for confirmation OK button as placeholder
        # In a real scenario, this would be replaced with actual locator
        pass  # Placeholder - to be implemented based on actual UI

    def assert_add_currency_page_loaded(self, bank: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        self.assert_visible(self.locator(loc.add_currency_page_title), "Add Currency page title")

    def assert_currency_exists_in_list(self, bank: str, currency_code: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        row_locator = loc.row_template.format(currency_code=currency_code)
        self.assert_visible(self.locator(row_locator), f"Currency row for {currency_code}")
