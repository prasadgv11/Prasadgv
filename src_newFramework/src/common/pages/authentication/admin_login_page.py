from src.common.base.base_page import BasePage
from src.common.utilities.config_loader import ConfigManager
from src.banks.neoleap.locators.login_locators import NeoleapLoginLocators
from src.banks.oab.locators.login_locators import OabLoginLocators
from src.banks.alrajhi.locators.login_locators import AlrajhiLoginLocators
from src.banks.wio.locators.login_locators import WioLoginLocators
from src.banks.pinelabs.locators.login_locators import PinelabsLoginLocators

class AdminLoginPage(BasePage):
    def __init__(self, page, module_name="Login"):
        super().__init__(page, module_name=module_name)
        self._dispatch = {
            "neoleap": (self._login_standard_mfa, NeoleapLoginLocators.Admin),
            "oab": (self._login_standard, OabLoginLocators.Admin),
            "alrajhi": (self._login_standard_mfa, AlrajhiLoginLocators.Admin),
            "wio": (self._login_standard, WioLoginLocators.Admin),
            "pinelabs": (self._login_standard, PinelabsLoginLocators.Admin),
        }

    def navigate_to_portal(self) -> dict:
        creds = dict(ConfigManager.load_portal_config("admin"))
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
        self.click_by_locator(loc.submit_button, "Submit button")
        
    def logout(self, bank_name: str) -> None:
        loc = self._get_locators(bank_name)

        self.click_by_locator(
        loc.logout_button,
        "Logout button"
    )

    print("Logout clicked")
    
    def _login_standard_mfa(self, creds: dict, loc) -> None:
        self._login_standard(creds, loc)
        self.enter_authenticator(creds["totp_secret"], loc.otp_field)
        self.click_by_locator(loc.verify_button, "Verify button")
    def assert_dashboard_visible(self, bank: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        self.assert_visible(self.locator(loc.dashboard_marker), f"{bank.capitalize()} Admin Dashboard")
