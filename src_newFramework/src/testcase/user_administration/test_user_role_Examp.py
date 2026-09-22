import pytest
from src.common.pages.authentication.bank_login_page import BankLoginPage
from src.common.pages.user_administration.user_role_page import UserRolePage
from src.common.pages.authentication.merchant_login_page import MerchantLoginPage
from src.common.pages.authentication.admin_login_page import AdminLoginPage
from src.common.utilities.excel_utils import ExcelUtil


from src.common.utilities.config_manager import ConfigManager
from src.testcase.Login.test_bank_login import BankLoginModule

BANK_NAME = ConfigManager.get("bank")

_all_rows = ExcelUtil.get_sheet("UserAdministration", "UserRole")


# Load all rows from Merchant.xlsx / Configuration sheet
# Utility: filter rows by exact ScenarioID.
# If ExpectedMessage is blank, the row still runs so we can validate the flow
# without requiring a hardcoded success message.
def filter_rows(scenario_id: str):
    filtered = []
    for row in _all_rows:
        if row.get("ScenarioID") != scenario_id:
            continue
        filtered.append(
            pytest.param(row, id=f'{row["ScenarioID"]} - {row["TestcaseID"]} - {row["Description"]}')
        )
    return filtered


# Scenario-specific row sets
_params_add = filter_rows("TS_UserRole_001")
@pytest.mark.sanity
@pytest.mark.regression
class TestUserRoleModule:
    @pytest.mark.parametrize("data", _params_add)
    def test_user_role_add(self, page, data):
        """Verify the add functionality of User Role across banks"""
        # Step 1: Login via AdminLoginPage
        # Step 2: Navigate and perform User Role actions
        
        BankLoginModule(page).bankportal()
        role_page = UserRolePage(page)
        role_page.navigate_to_user_role(BANK_NAME)
        role_page.add_role(BANK_NAME, data)
        role_page.assert_role_error_message(BANK_NAME, data["ExpectedMessage"])
       

