from src.common.base.base_page import BasePage
from src.common.utilities.config_loader import ConfigManager
from src.banks.neoleap.locators.login_locators import NeoleapLoginLocators
from src.banks.alrajhi.locators.login_locators import AlrajhiLoginLocators
from src.banks.wio.locators.login_locators import WioLoginLocators
from src.banks.pinelabs.locators.login_locators import PinelabsLoginLocators
from src.banks.ecentric.locators.login_locators import EcentricLoginLocators
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import Error as ActionFailedError


class MerchantLoginPage(BasePage):
    def __init__(self, page, module_name="Login"):
        super().__init__(page, module_name=module_name)
        self._dispatch = {
            "neoleap": (self._login_with_institution_mfa, NeoleapLoginLocators.Merchant),
            "alrajhi": (self._login_with_merchant_mfa, AlrajhiLoginLocators.Merchant),
            "pinelabs": (self._login_standard, PinelabsLoginLocators.Merchant),
            "ecentric": (self._login_with_captcha, EcentricLoginLocators.Merchant),
        }

    def navigate_to_portal(self) -> dict:
        creds = dict(ConfigManager.load_portal_config("merchant"))
        self.navigate(creds["url"])
        return creds

    def login(self, merchant: str) -> None:
        creds = self.navigate_to_portal()
        method, loc = self._dispatch[merchant.lower()]
        method(creds, loc)

    def _login_standard(self, creds: dict, loc) -> None:
        self.click_by_locator(loc.login_button, "Login button")
        self.page.wait_for_load_state("domcontentloaded")
        self.fill_by_locator(loc.username_field, creds["username"], "Username")
        self.fill_by_locator(loc.password_field, creds["password"], "Password")
        self.click_by_locator(loc.submit_button, "Login button")

    def _login_with_merchant(self, creds: dict, loc) -> None:
        self.fill_by_locator(loc.institution_name_field, creds["institution_name"], "Institution Name")
        self.fill_by_locator(loc.merchant_id_field, creds["merchant_id"], "Merchant ID")
        self.fill_by_locator(loc.username_field, creds["username"], "User ID")
        self.fill_by_locator(loc.password_field, creds["password"], "Password")
        self.click_by_locator(loc.login_button, "Login button")

    def _login_with_merchant_mfa(self, creds: dict, loc) -> None:
        self._login_with_merchant(creds, loc)
        self.enter_authenticator(creds["totp_secret"], loc.otp_field)
        self.click_by_locator(loc.verify_button, "Verify button")

    def _login_with_institution(self, creds: dict, loc) -> None:
        self.fill_by_locator(loc.institution_field, creds["institution_id"], "Institution ID")
        self.fill_by_locator(loc.username_field, creds["username"], "User ID")
        self.fill_by_locator(loc.password_field, creds["password"], "Password")
        self.click_by_locator(loc.login_button, "Login button")

    def _login_with_institution_mfa(self, creds: dict, loc) -> None:
        self._login_with_institution(creds, loc)
        self.enter_authenticator(creds["totp_secret"], loc.otp_field)

    def _login_with_captcha(self, creds: dict, loc) -> None:
        max_attempts = 5
        for attempt in range(max_attempts):
            self.page.wait_for_load_state("domcontentloaded")
            self.fill_by_locator(loc.username_field, creds["username"], "username")
            self.fill_by_locator(loc.password_field, creds["password"], "password")

            # Read captcha text directly from DOM spans (no OCR needed)
            captcha_spans = self.page.locator(loc.captcha_image)
            captcha_text = "".join(
                captcha_spans.nth(i).inner_text().strip() for i in range(captcha_spans.count())
            )
            self.fill_by_locator(loc.captcha_field, captcha_text, "Captcha text")

            self.click_by_locator(loc.login_button, "Login button")

            captcha_error = self.page.locator(loc.captcha_error)
            try:
                captcha_error.wait_for(state="visible", timeout=5000)
                if attempt == max_attempts - 1:
                    raise ActionFailedError("Login failed after maximum captcha retry attempts.")
                self.click_by_locator(loc.captcha_refresh, "Captcha Refresh")
                self.page.wait_for_timeout(1000)
                continue
            except PlaywrightTimeoutError:
                return

    def assert_dashboard_visible(self, merchant: str) -> None:
        _, loc = self._dispatch[merchant.lower()]
        self.assert_visible(self.locator(loc.dashboard_marker), f"{merchant.capitalize()} Merchant Dashboard")
