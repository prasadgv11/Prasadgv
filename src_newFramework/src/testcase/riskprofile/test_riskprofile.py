import pytest
from src.common.pages.authentication.bank_login_page import BankLoginPage
from src.common.pages.riskprofile.riskprofile_page import RiskprofilePage
from src.common.utilities.excel_utils import ExcelUtil
from src.common.utilities.config_manager import ConfigManager

BANK_NAME = ConfigManager.get("bank")

_rows_add = ExcelUtil.get_sheet("Riskprofile", "Add")
_rows_search = ExcelUtil.get_sheet("Riskprofile", "Search")

@pytest.mark.sanity
@pytest.mark.regression
@pytest.mark.ecentric
class TestRiskprofileModule:
    @pytest.mark.parametrize(
        "data",
        _rows_add,
        ids=[f'{data["ScenarioID"]} - {data["TestcaseID"]} - {data["Description"]}' for data in _rows_add]
    )
    def test_riskprofile_add(self, page, data):
        """Verify the add functionality of Risk profile"""
        login_page = BankLoginPage(page)
        login_page.login(BANK_NAME)
        login_page.assert_dashboard_visible(BANK_NAME)

        riskprofile_page = RiskprofilePage(page)
        riskprofile_page.navigate_to_riskprofile(BANK_NAME)
        riskprofile_page.click_add_button(BANK_NAME)
        riskprofile_page.fill_riskprofile_form(BANK_NAME, data)
        riskprofile_page.click_save_button(BANK_NAME)
        riskprofile_page.assert_riskprofile_message(BANK_NAME, data["ExpectedMessage"])

    @pytest.mark.parametrize(
        "data",
        _rows_search,
        ids=[f'{data["ScenarioID"]} - {data["TestcaseID"]} - {data["Description"]}' for data in _rows_search]
    )
    def test_riskprofile_search(self, page, data):
        """Verify the search functionality of Risk profile"""
        login_page = BankLoginPage(page)
        login_page.login(BANK_NAME)
        login_page.assert_dashboard_visible(BANK_NAME)

        riskprofile_page = RiskprofilePage(page)
        riskprofile_page.navigate_to_riskprofile(BANK_NAME)
        riskprofile_page.fill_search_form(BANK_NAME, data)
        riskprofile_page.click_search_button(BANK_NAME)
        riskprofile_page.assert_search_result(BANK_NAME, data["ExpectedMessage"])
