from src.common.base.base_page import BasePage
from src.banks.wio.locators.currecncy_locators import CurrecncyLocators as WioCurrecncyLocators

class CurrecncyPage(BasePage):
    def __init__(self, page, module_name="Currecncy"):
        super().__init__(page, module_name=module_name)
        self._dispatch = {
            "wio": (self._add_standard, WioCurrecncyLocators),
        }

    def navigate_to_currecncy(self, bank: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        self.hover_by_getbytext(loc.configuration_menu, "Configuration menu")
        self.click_by_locator(loc.currency_submenu, "Currency submenu")

    def click_add_button(self, bank: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        self.click_by_locator(loc.add_button, "Add button")

    def fill_currecncy_form(self, bank: str, data: dict) -> None:
        method, loc = self._dispatch[bank.lower()]
        method(loc, data)

    def _add_standard(self, loc, data: dict) -> None:
        self.fill_by_locator(loc.currency_code_input, data["Currency Code"], "Currency Code")
        self.fill_by_locator(loc.currency_description_input, data["Currency Description"], "Currency Description")
        self.fill_by_locator(loc.minor_digits_input, data["Minor Digits"], "Minor Digits")
        self.fill_by_locator(loc.currency_symbol_input, data["Currency Symbol"], "Currency Symbol")

    def click_save_button(self, bank: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        self.click_by_locator(loc.save_button, "Save button")

    def click_cancel_button(self, bank: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        self.click_by_locator(loc.cancel_button, "Cancel button")

    def assert_currecncy_message(self, bank: str, expected_message: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        self.assert_text(self.locator(loc.message_container), expected_message, "Response Message")

    def assert_currency_row_present(self, bank: str, currency_code: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        row_locator = loc.currency_row_template.format(currency_code=currency_code)
        self.assert_visible(self.locator(row_locator), f"Currency row with code {currency_code} is visible")

    def assert_currency_row_not_present(self, bank: str, currency_code: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        row_locator = loc.currency_row_template.format(currency_code=currency_code)
        self.assert_not_visible(self.locator(row_locator), f"Currency row with code {currency_code} is not visible")

    # View action methods
    def click_view_button_on_row(self, bank: str, currency_code: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        row_locator = loc.currency_row_template.format(currency_code=currency_code)
        view_button_locator = f"{row_locator}{loc.view_button_in_row}"
        self.click_by_locator(self.locator(view_button_locator), f"View button for currency {currency_code}")

    def assert_view_page_values_match_list(self, bank: str, currency_code: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        # Get values from the list row
        row_locator = loc.currency_row_template.format(currency_code=currency_code)
        # We assume the columns are in order: Select, Currency Code, Currency Description, Minor Digits, Currency Symbol, Status
        # Adjust indices if needed
        currency_desc_from_list = self.get_cell_value(self.locator(f"{row_locator}/td[2]"), 0, 1, "Currency Description from list")
        minor_digits_from_list = self.get_cell_value(self.locator(f"{row_locator}/td[2]"), 0, 2, "Minor Digits from list")
        currency_symbol_from_list = self.get_cell_value(self.locator(f"{row_locator}/td[2]"), 0, 3, "Currency Symbol from list")
        status_from_list = self.get_cell_value(self.locator(f"{row_locator}/td[2]"), 0, 4, "Status from list")
        
        # Get values from the view page
        currency_code_on_view = self.get_text(self.locator(loc.view_currency_code_display), "Currency Code on view page")
        currency_desc_on_view = self.get_text(self.locator(loc.view_currency_description_display), "Currency Description on view page")
        minor_digits_on_view = self.get_text(self.locator(loc.view_minor_digits_display), "Minor Digits on view page")
        currency_symbol_on_view = self.get_text(self.locator(loc.view_currency_symbol_display), "Currency Symbol on view page")
        status_on_view = self.get_text(self.locator(loc.view_status_display), "Status on view page")
        
        # Assert they match (note: currency code should match the one we used to find the row)
        self.assert_text(self.locator(loc.view_currency_code_display), currency_code, "Currency Code on view page")
        self.assert_text(self.locator(loc.view_currency_description_display), currency_desc_from_list, "Currency Description on view page")
        self.assert_text(self.locator(loc.view_minor_digits_display), minor_digits_from_list, "Minor Digits on view page")
        self.assert_text(self.locator(loc.view_currency_symbol_display), currency_symbol_from_list, "Currency Symbol on view page")
        self.assert_text(self.locator(loc.view_status_display), status_from_list, "Status on view page")

    def click_back_button(self, bank: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        self.click_by_locator(loc.view_back_button, "Back button on view page")

    def assert_currency_list_page_visible(self, bank: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        self.assert_visible(self.locator(loc.currency_list_page_indicator), "Currency list page")

    # Edit action methods
    def click_edit_button_on_row(self, bank: str, currency_code: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        row_locator = loc.currency_row_template.format(currency_code=currency_code)
        edit_button_locator = f"{row_locator}{loc.edit_button_in_row}"
        self.click_by_locator(self.locator(edit_button_locator), f"Edit button for currency {currency_code}")

    def fill_edit_currecncy_form(self, bank: str, data: dict) -> None:
        method, loc = self._dispatch[bank.lower()]
        method(loc, data)

    def _edit_standard(self, loc, data: dict) -> None:
        # Currency Code is likely read-only, so we don't fill it
        self.fill_by_locator(loc.edit_currency_description_input, data["Currency Description"], "Currency Description")
        self.fill_by_locator(loc.edit_minor_digits_input, data["Minor Digits"], "Minor Digits")
        self.fill_by_locator(loc.edit_currency_symbol_input, data["Currency Symbol"], "Currency Symbol")

    def click_edit_save_button(self, bank: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        self.click_by_locator(loc.edit_save_button, "Edit Save button")

    def click_edit_cancel_button(self, bank: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        self.click_by_locator(loc.edit_cancel_button, "Edit Cancel button")

    # ChangeStatus action methods
    def select_currency_row_checkbox(self, bank: str, currency_code: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        row_locator = loc.currency_row_template.format(currency_code=currency_code)
        checkbox_locator = f"{row_locator}{loc.row_checkbox_template}"
        self.click_by_locator(self.locator(checkbox_locator), f"Checkbox for currency {currency_code}")

    def click_change_status_button(self, bank: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        self.click_by_locator(loc.change_status_button, "Change Status button")

    # Note: Assuming a confirmation dialog appears; we accept it by default
    # If the scenario requires handling a specific confirmation, we would add that here
