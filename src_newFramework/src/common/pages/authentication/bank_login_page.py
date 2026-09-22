from src.common.base.base_page import BasePage
from src.common.utilities.config_loader import ConfigManager
from src.banks.neoleap.locators.login_locators import NeoleapLoginLocators
from src.banks.alrajhi.locators.login_locators import AlrajhiLoginLocators
from src.banks.wio.locators.login_locators import WioLoginLocators
from src.banks.pinelabs.locators.login_locators import PinelabsLoginLocators
from src.banks.ecentric.locators.login_locators import EcentricLoginLocators
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

class BankLoginPage(BasePage):
    def __init__(self, page, module_name="Login"):
        super().__init__(page, module_name=module_name)
        self._dispatch = {
            "neoleap": (self._login_with_institution_mfa, NeoleapLoginLocators.Bank),
            "alrajhi": (self._login_with_institution_mfa, AlrajhiLoginLocators.Bank),
            "wio": (self._login_standard, WioLoginLocators.Bank),
            "pinelabs": (self._login_standard, PinelabsLoginLocators.Bank),
            "ecentric": (self._login_with_captcha, EcentricLoginLocators.Bank),
            
        }

    def navigate_to_portal(self) -> dict:
        creds = dict(ConfigManager.load_portal_config("bank"))
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

    def _login_with_institution(self, creds: dict, loc) -> None:
        self.fill_by_locator(loc.institution_field, creds["institution_id"], "Institution ID")
        self.fill_by_locator(loc.username_field, creds["username"], "User ID")
        self.fill_by_locator(loc.password_field, creds["password"], "Password")
        self.click_by_locator(loc.submit_button, "Submit button")
        

    def _login_with_institution_mfa(self, creds: dict, loc) -> None:
        self.click_by_locator(loc.login_button, "Login button")
        self._login_with_institution(creds, loc)
        self.enter_authenticator(creds["totp_secret"], loc.otp_field)
        self.click_by_locator(loc.verify_button, "Verify button")

    def assert_dashboard_visible(self, bank: str) -> None:
        _, loc = self._dispatch[bank.lower()]
        self.assert_visible(self.locator(loc.dashboard_marker), f"{bank.capitalize()} Bank Dashboard")
        
    def _login_with_captcha(self, creds: dict, loc) -> None:
        max_attempts = 5
        for attempt in range(max_attempts):
            self.page.wait_for_load_state("domcontentloaded")
            self.fill_by_locator(loc.username_field, creds["username"], "username")
            self.fill_by_locator(loc.password_field, creds["password"], "password")
 
        # Read captcha text directly from DOM spans (no OCR needed)
            captcha_spans = self.page.locator(loc.captcha_image)
            captcha_text = "".join(
                captcha_spans.nth(i).inner_text().strip()
                for i in range(captcha_spans.count())
            )
            self.fill_by_locator(loc.captcha_field, captcha_text, "Captcha text")
 
            self.click_by_locator(loc.login_button, "Login button")
 
            captcha_error = self.page.locator(loc.captcha_error)
            try:
                captcha_error.wait_for(state="visible", timeout=5000)
                if attempt == max_attempts - 1:
                    raise RuntimeError("Login failed after maximum captcha retry attempts.")
                self.click_by_locator(loc.captcha_refresh, "Captcha Refresh")
                self.page.wait_for_timeout(1000)
                continue
            except PlaywrightTimeoutError:
                return
    
        self.assert_visible(self.locator(loc.login_msg), "Ecentric Bank page")

        