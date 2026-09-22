import pytest
from src.common.pages.authentication.bank_login_page import BankLoginPage
from src.common.pages.currency.currency_page import CurrencyPage
from src.common.utilities.excel_utils import ExcelUtil
from src.common.utilities.config_manager import ConfigManager

BANK_NAME = ConfigManager.get("bank")

# Helper to get test data for each action
_add_rows = ExcelUtil.get_sheet("Currency", "Add")
_view_rows = ExcelUtil.get_sheet("Currency", "View")
_edit_rows = ExcelUtil.get_sheet("Currency", "Edit")
_changestatus_rows = ExcelUtil.get_sheet("Currency", "ChangeStatus")

@pytest.mark.sanity
@pytest.mark.regression
class TestCurrencyModule:
    def test_currency_add(self, page, data):
        """Verify the add functionality of Currency"""
        login_page = BankLoginPage(page)
        login_page.login(BANK_NAME)
        login_page.assert_dashboard_visible(BANK_NAME)

        currency_page = CurrencyPage(page)
        currency_page.navigate_to_currency(BANK_NAME)
        currency_page.click_add_button(BANK_NAME)
        currency_page.assert_add_currency_page_loaded(BANK_NAME)
        currency_page.fill_currency_form(BANK_NAME, data)
        currency_page.click_save_button(BANK_NAME)
        currency_page.assert_currency_message(BANK_NAME, data["ExpectedMessage"])
        # If the expected message indicates success, verify the new row appears in the list
        if data["ExpectedMessage"] == "Currency added successfully":
            currency_page.assert_currency_exists_in_list(BANK_NAME, data["Currency Code"])

    def test_currency_view(self, page, data):
        """Verify the view functionality of Currency"""
        login_page = BankLoginPage(page)
        login_page.login(BANK_NAME)
        login_page.assert_dashboard_visible(BANK_NAME)

        currency_page = CurrencyPage(page)
        currency_page.navigate_to_currency(BANK_NAME)
        # Assuming we search/view by Currency Code from data
        currency_code = data.get("Currency Code")
        currency_page.click_view_button(BANK_NAME, currency_code)
        currency_page.assert_view_currency_details(BANK_NAME, data)
        currency_page.click_back_button(BANK_NAME)
        # Verify we are back on the list page (optional, can add assertion for list page element)

    def test_currency_edit(self, page, data):
        """Verify the edit functionality of Currency"""
        login_page = BankLoginPage(page)
        login_page.login(BANK_NAME)
        login_page.assert_dashboard_visible(BANK_NAME)

        currency_page = CurrencyPage(page)
        currency_page.navigate_to_currency(BANK_NAME)
        currency_code = data.get("Currency Code")
        currency_page.click_edit_button(BANK_NAME, currency_code)
        # For edit, we typically don't change Currency Code (read-only), so fill other fields
        # Remove Currency Code from data if present to avoid trying to fill read-only field
        edit_data = {k: v for k, v in data.items() if k != "Currency Code"}
        currency_page.fill_currency_form(BANK_NAME, edit_data)
        currency_page.click_save_button(BANK_NAME)
        currency_page.assert_currency_message(BANK_NAME, data["ExpectedMessage"])
        # If the expected message indicates success, verify the updated value in the list by viewing the record
        if data["ExpectedMessage"] == "Currency updated successfully":
            # Prepare the data for view: include the currency code (unchanged) and the updated fields
            view_data = {
                "Currency Code": currency_code,
                "Currency Description": edit_data.get("Currency Description", ""),
                "Minor Digits": edit_data.get("Minor Digits", ""),
                "Currency Symbol": edit_data.get("Currency Symbol", ""),
            }
            currency_page.click_view_button(BANK_NAME, currency_code)
            currency_page.assert_view_currency_details(BANK_NAME, view_data)
            currency_page.click_back_button(BANK_NAME)

    def test_currency_changestatus(self, page, data):
        """Verify the change status functionality of Currency"""
        login_page = BankLoginPage(page)
        login_page.login(BANK_NAME)
        login_page.assert_dashboard_visible(BANK_NAME)

        currency_page = CurrencyPage(page)
        currency_page.navigate_to_currency(BANK_NAME)
        currency_code = data.get("Currency Code")
        currency_page.click_checkbox(BANK_NAME, currency_code)
        currency_page.click_change_status_button(BANK_NAME)
        # Handle confirmation if needed
        currency_page.confirm_change_status(BANK_NAME)
        currency_page.assert_currency_message(BANK_NAME, data["ExpectedMessage"])
