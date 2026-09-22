import pytest
from src.common.pages.authentication.bank_login_page import BankLoginPage
from src.common.utilities.excel_utils import ExcelUtil
from src.common.utilities.config_manager import ConfigManager

BANK_NAME = ConfigManager.get("bank")


class BankLoginModule:
    def __init__(self, page):
        self.page = page

    def bankportal(self) -> None:
        login_page = BankLoginPage(self.page)
        login_page.login(BANK_NAME)


# @pytest.mark.sanity
# @pytest.mark.regression
# class TestLoginModule:
#     def test_login_bank(self, page):
#         BankLoginModule(page).bankportal()
        
