from src.common.base.base_page import BasePage
from src.banks.neoleap.locators.user_role_locators import UserRoleLocators as NeoleapUserRoleLocators
from src.banks.oab.locators.user_role_locators import UserRoleLocators as OabUserRoleLocators
from src.banks.alrajhi.locators.user_role_locators import UserRoleLocators as AlrajhiUserRoleLocators
from src.banks.wio.locators.user_role_locators import UserRoleLocators as WioUserRoleLocators
from src.banks.pinelabs.locators.user_role_locators import UserRoleLocators as PinelabsUserRoleLocators
from src.banks.ecentric.locators.user_role_locators import UserRoleLocators as EcentricUserRoleLocators

class UserRolePage(BasePage):
    def __init__(self, page, module_name="UserRole"):
        super().__init__(page, module_name=module_name)
        self._dispatch = {
            "neoleap": (self._add_role_neoleap, self._assert_neoleap, NeoleapUserRoleLocators),
            "oab": (self._add_role_oab, self._assert_oab, OabUserRoleLocators),
            "alrajhi": (self._add_role_alrajhi, self._assert_alrajhi, AlrajhiUserRoleLocators),
            "wio": (self._add_role_wio, self._assert_wio, WioUserRoleLocators),
            "pinelabs": (self._add_role_pinelabs, self._assert_pinelabs, PinelabsUserRoleLocators),
            "ecentric": (self._add_role_ecentric, self._assert_ecentric, EcentricUserRoleLocators),
        }

    def navigate_to_user_role(self, bank: str) -> None:
        _, _, loc = self._dispatch[bank.lower()]
        self.click_by_locator(loc.menu_myaccount, f"{bank} My Account menu")
        self.click_by_locator(loc.menu_userrole, f"{bank} User Role menu")

    def add_role(self, bank: str, data: dict) -> None:
        add_method, _, loc = self._dispatch[bank.lower()]
        add_method(data, loc)

    def assert_role_error_message(self, bank: str, expected_message: str) -> None:
        _, assert_method, loc = self._dispatch[bank.lower()]
        assert_method(expected_message, loc)

    # --- Bank‑specific role creation handlers ---
    def _add_role_neoleap(self, data: dict, loc) -> None:
        self.fill_by_locator(loc.role_name, data["RoleName"], "Role Name")
        self.fill_by_locator(loc.role_desc, data["RoleDesc"], "Role Description")
        self.fill_by_locator(loc.permission1, data["Permission1"], "Permission 1")
        self.fill_by_locator(loc.permission2, data["Permission2"], "Permission 2")
        self.click_by_locator(loc.save_button, "Save Role")

    def _add_role_oab(self, data: dict, loc) -> None:
        self.fill_by_locator(loc.role_code, data["RoleCode"], "Role Code")
        self.fill_by_locator(loc.role_name, data["RoleName"], "Role Name")
        self.fill_by_locator(loc.role_desc, data["RoleDesc"], "Role Description")
        self.fill_by_locator(loc.extra_field, data["ExtraField"], "Extra Field")
        self.click_by_locator(loc.save_button, "Save Role")

    def _add_role_alrajhi(self, data: dict, loc) -> None:
        self.fill_by_locator(loc.role_name, data["RoleName"], "Role Name")
        self.fill_by_locator(loc.role_desc, data["RoleDesc"], "Role Description")
        self.fill_by_locator(loc.permission_level, data["PermissionLevel"], "Permission Level")
        self.click_by_locator(loc.save_button, "Save Role")

    def _add_role_wio(self, data: dict, loc) -> None:
        self.fill_by_locator(loc.role_name, data["RoleName"], "Role Name")
        self.fill_by_locator(loc.role_desc, data["RoleDesc"], "Role Description")
        self.fill_by_locator(loc.department, data["Department"], "Department")
        self.click_by_locator(loc.save_button, "Save Role")

    def _add_role_pinelabs(self, data: dict, loc) -> None:
        self.fill_by_locator(loc.role_name, data["RoleName"], "Role Name")
        self.fill_by_locator(loc.role_desc, data["RoleDesc"], "Role Description")
        self.fill_by_locator(loc.permission_group, data["PermissionGroup"], "Permission Group")
        self.click_by_locator(loc.save_button, "Save Role")

    def _add_role_ecentric(self, data: dict, loc) -> None:
        self.fill_by_locator(loc.role_name, data["RoleName"], "Role Name")
        self.fill_by_locator(loc.role_desc, data["RoleDesc"], "Role Description")
        self.fill_by_locator(loc.risk_level, data["RiskLevel"], "Risk Level")
        self.click_by_locator(loc.save_button, "Save Role")

    # --- Bank‑specific assertions ---
    def _assert_neoleap(self, expected_message: str, loc) -> None:
        self.assert_text(self.locator(loc.error_message), expected_message, "Neoleap Role error")

    def _assert_oab(self, expected_message: str, loc) -> None:
        self.assert_text(self.locator(loc.error_message), expected_message, "OAB Role error")

    def _assert_alrajhi(self, expected_message: str, loc) -> None:
        self.assert_text(self.locator(loc.error_message), expected_message, "Alrajhi Role error")

    def _assert_wio(self, expected_message: str, loc) -> None:
        self.assert_text(self.locator(loc.error_message), expected_message, "Wio Role error")

    def _assert_pinelabs(self, expected_message: str, loc) -> None:
        self.assert_text(self.locator(loc.error_message), expected_message, "Pinelabs Role error")

    def _assert_ecentric(self, expected_message: str, loc) -> None:
        self.assert_text(self.locator(loc.error_message), expected_message, "Ecentric Role error")
