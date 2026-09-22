import pytest
from src.common.pages.authentication.admin_login_page import AdminLoginPage
from src.common.utilities.excel_utils import ExcelUtil
from src.common.utilities.config_manager import ConfigManager

BANK_NAME = ConfigManager.get("bank")


class AdminLoginModule:
    def __init__(self, page):
        self.page = page

    def adminportal(self) -> None:
        login_page = AdminLoginPage(self.page)
        login_page.login(BANK_NAME)
        
