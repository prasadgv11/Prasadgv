import pytest
from src.common.pages.authentication.admin_login_page import AdminLoginPage
from src.common.pages.user_administration.user_role_page import UserRolePage
from src.common.utilities.excel_utils import ExcelUtil
from src.common.utilities.config_manager import ConfigManager

BANK_NAME = ConfigManager.get("bank")

_rows = ExcelUtil.get_sheet("UserAdministration", "UserRole")
_params = [pytest.param(data,id=f'{data["ScenarioID"]} - {data["TestcaseID"]} - {data["Description"]}') for data in _rows]

class TestUserRoleModule:
    @pytest.mark.wio
    @pytest.mark.neoleap
    @pytest.mark.sanity
    @pytest.mark.parametrize("data",_params)
    def test_user_role_add(self, page, data):
        """Verify the add functionality of User Role across banks"""
        # Step 1: Login via AdminLoginPage
        login_page = AdminLoginPage(page)
        login_page.login(BANK_NAME)
        login_page.assert_dashboard_visible(BANK_NAME)

        # Step 2: Navigate and perform User Role actions
        role_page = UserRolePage(page)
        role_page.navigate_to_user_role(BANK_NAME)
        role_page.add_role(BANK_NAME, data)
        role_page.assert_role_error_message(BANK_NAME, data["ExpectedMessage"])
