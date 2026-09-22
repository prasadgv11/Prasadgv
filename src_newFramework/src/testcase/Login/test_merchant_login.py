import pytest
from src.common.pages.authentication.merchant_login_page import MerchantLoginPage
from src.common.utilities.excel_utils import ExcelUtil
from src.common.utilities.config_manager import ConfigManager

BANK_NAME = ConfigManager.get("bank")


class MerchantLoginModule:
    def __init__(self, page):
        self.page = page

    def merchantportal(self) -> None:
        login_page = MerchantLoginPage(self.page)
        login_page.login(BANK_NAME)
        
