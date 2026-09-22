from src.common.base.base_page import BasePage
from src.banks.ecentric.locators.riskprofile_locators import RiskprofileLocators as EcentricRiskprofileLocators

class RiskprofilePage(BasePage):
    def __init__(self, page, module_name="Riskprofile"):
        super().__init__(page, module_name=module_name)
        self._dispatch = {
            "ecentric": (self._add_standard, EcentricRiskprofileLocators)
        }

    def navigate_to_riskprofile(self, bank: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        self.hover_by_getbytext(loc.menu_administration, "Administration menu")
        self.click_by_locator(loc.menu_risk_setup, "Risk setup sub-menu")
        self.click_by_locator(loc.menu_pg, "PG sub-menu")
        self.click_by_locator(loc.tab_risk_profile, "Risk profile tab")

    def click_add_button(self, bank: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        self.click_by_locator(loc.button_add, "Add button")

    def click_save_button(self, bank: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        self.click_by_locator(loc.button_save, "Save button")

    def click_search_button(self, bank: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        self.click_by_locator(loc.button_search, "Search button")

    def fill_riskprofile_form(self, bank: str, data: dict) -> None:
        method, loc = self._dispatch[bank.lower()]
        method(loc, data)

    def _add_standard(self, loc, data: dict) -> None:
        self.fill_by_locator(loc.input_risk_profile_name, data["Risk profile name"], "Risk profile name")
        self.select_by_locator(loc.dropdown_currency_code, data["Currency code"], "Currency code")
        self.check_by_locator(loc.radio_profile_international_transaction_no, "Profile international transaction No")
        self.check_by_locator(loc.toggle_terminal_domestic_daily, "Terminal Domestic Daily toggle")
        self.check_by_locator(loc.toggle_terminal_domestic_weekly, "Terminal Domestic Weekly toggle")
        self.check_by_locator(loc.toggle_terminal_domestic_monthly, "Terminal Domestic Monthly toggle")
        self.fill_by_locator(loc.input_terminal_domestic_daily_count, data["No of transactions Daily"], "No of transactions Daily")
        self.fill_by_locator(loc.input_terminal_domestic_weekly_count, data["No of transactions Weekly"], "No of transactions Weekly")
        self.fill_by_locator(loc.input_terminal_domestic_monthly_count, data["No of transactions Monthly"], "No of transactions Monthly")
        self.check_by_locator(loc.toggle_cumulative_transaction_amount_daily, "Cumulative transaction amount Daily toggle")
        self.check_by_locator(loc.toggle_cumulative_refund_amount_daily, "Cumulative refund amount Daily toggle")
        self.check_by_locator(loc.radio_terminal_actions_terminal_blocking, "Terminal Actions Terminal blocking")
        self.fill_by_locator(loc.input_transaction_amount_min, data["Minimum amount"], "Minimum amount")
        self.fill_by_locator(loc.input_transaction_amount_max, data["Maximum amount"], "Maximum amount")
        self.check_by_locator(loc.toggle_user_domestic_daily, "User Domestic Daily toggle")
        self.check_by_locator(loc.radio_user_actions_card_blocking, "User Actions Card blocking")
        self.check_by_locator(loc.toggle_ip_domestic_daily, "IP Domestic Daily toggle")
        self.check_by_locator(loc.radio_ip_actions_ip_blocking, "IP Actions IP blocking")

    def fill_search_form(self, bank: str, data: dict) -> None:
        _, loc = self._dispatch[bank.lower()]
        self.fill_by_locator(loc.input_search_risk_profile_name_currency, data["Search text input"], "Search text input")
        self.select_by_locator(loc.dropdown_search_mode, data["Mode"], "Mode")

    def assert_riskprofile_message(self, bank: str, expected_message: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        self.assert_text(self.locator(loc.message_success), expected_message, "Success message")

    def assert_search_result(self, bank: str, expected_message: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        if expected_message:
            safe_message = expected_message.replace("'", "''")
            row_locator = f"//tr[td[contains(normalize-space(text()),'{safe_message}')]]"
            self.assert_text(self.locator(row_locator), expected_message, "Risk profile row")
        else:
            self.assert_text(self.locator(loc.message_no_records), "No records found", "No records message")
