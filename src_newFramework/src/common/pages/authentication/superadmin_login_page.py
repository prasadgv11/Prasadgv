from src.common.base.base_page import BasePage
from src.common.utilities.config_loader import ConfigManager
from src.banks.neoleap.locators.login_locators import NeoleapLoginLocators
# oab, wio, pinelabs have no SuperAdmin locator class defined

class SuperAdminLoginPage(BasePage):
    def __init__(self, page, module_name="Login"):
        super().__init__(page, module_name=module_name)
        self._dispatch = {
            "neoleap": (self._login_standard_mfa, NeoleapLoginLocators.SuperAdmin),
        }

    def navigate_to_portal(self) -> dict:
        creds = dict(ConfigManager.load_portal_config("superadmin"))
        self.navigate(creds["url"])
        return creds

    def login(self, bank: str) -> None:
        creds = self.navigate_to_portal()
        method, loc = self._dispatch[bank.lower()]
        method(creds, loc)

    def _login_standard(self, creds: dict, loc) -> None:
        self.click_by_locator(loc.login_button, "Login button")
        self.page.wait_for_load_state("domcontentloaded")
        self.fill_by_locator(loc.username_field, creds["username"], "Username")
        self.fill_by_locator(loc.password_field, creds["password"], "Password")
        self.click_by_locator(loc.submit_button, "Login button")

    def _login_standard_mfa(self, creds: dict, loc) -> None:
        self._login_standard(creds, loc)
        self.enter_authenticator(creds["totp_secret"], loc.otp_field)

    def assert_dashboard_visible(self, bank: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        self.assert_visible(self.locator(loc.dashboard_marker), f"{bank.capitalize()} SuperAdmin Dashboard")
