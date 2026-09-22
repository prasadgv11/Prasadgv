import os
import json
import re
import allure

from venv import logger
from typing import Union
from openai import timeout
from core.logger import get_logger
from typing import Literal
from core.llm_auto_heal import LocatorAutoHeal
from playwright.sync_api import Locator, TimeoutError as PlaywrightTimeoutError, expect

class BasePage:
    def __init__(self, page, module_name="General"):
        self.page = page
        self.logger = logger or self._default_logger()
        self.logger = get_logger(self.__class__.__name__)
        self.auto_healer = LocatorAutoHeal(page)
        self.module_name = module_name
        self.screenshot_dir = os.path.join("screenshots", module_name)
        os.makedirs(self.screenshot_dir, exist_ok=True)
        self.screenshot_count = 1


    def attach_screenshot(self, step_name):
        """Save screenshot in module folder and attach to Allure.
        A timeout or other error should not crash the test; log and continue.
        """
        file_name = f"{self.screenshot_count:03d}_{step_name}.png"
        path = os.path.join(self.screenshot_dir, file_name)
        try:
            self.page.screenshot(path=path, full_page=True, timeout=60000)
        except Exception as e:  # PlaywrightTimeoutError or others
            # don't re-raise, just log
            self.logger.warning(f"Screenshot failed for {step_name}: {e}")
        try:
            allure.attach.file(path, name=step_name, attachment_type=allure.attachment_type.PNG)
        except Exception:
            pass
        self.screenshot_count += 1

    @allure.step("Navigate to URL: {url}")
    def navigate(self, url: str, timeout: int = 30000) -> bool:
        """Navigate to a given URL"""
        try:
            self.page.goto(url, timeout=timeout)
            self.logger.info(f"Navigated to URL: {url}")
            self.attach_screenshot("After navigation")
            return True
        except TimeoutError:
            self.logger.error(f"Failed to navigate to URL: {url}")
            return False
        
    @allure.step("Click element")
    def click_by_locator(self, locator, description="Click action", timeout: int = 30000) -> bool:
        """Click with auto-heal fallback"""
        try:
             # If locator is a string, convert to Playwright locator
            if isinstance(locator, str):
                locator = self.page.locator(locator)
                
            locator.wait_for(state="visible", timeout=timeout)
            locator.click()
            self.logger.info(f"Clicked element: {description}")
            self.attach_screenshot(f"After {description}")
            return True
        except TimeoutError:
            self.logger.error(f"Click failed for: {description}")
            # 🔧 Auto-heal attempt
            healed_locator = self.auto_healer.locator(str(locator))
            if healed_locator:
                self.logger.info(f"Auto-heal applied for: {description}")
                healed_locator.click()
                self.attach_screenshot(f"After auto-heal {description}")
                return True
            raise AssertionError(f"{description} Failed")
        
    @allure.step("Fill input field")
    def fill_by_locator(self, locator, text: str, description="Fill action", timeout: int = 30000) -> bool:
        """Fill with auto-heal fallback"""
        try:
            if isinstance(locator, str): 
                locator = self.page.locator(locator)
            
            locator.wait_for(state="visible", timeout=timeout)
            locator.fill(text)
            self.logger.info(f"Filled element ({description}) with text: {text}")
            self.attach_screenshot(f"After {description}")
            return True
        except TimeoutError:
            self.logger.error(f"Fill failed for: {description}")
            healed_locator = self.auto_healer.locator(str(locator))
            if healed_locator:
                self.logger.info(f"Auto-heal applied for: {description}")
                healed_locator.fill(text)
                self.attach_screenshot(f"After auto-heal {description}")
                return True
            return False
        
    # @allure.step("Click element by XPath: {xpath}")
    # def click_by_xpath(self, xpath: str, description: str = "Click by XPath", timeout: int = 30000) -> bool:
    #     """Wait until element located by XPath is visible, then click"""
    #     try:
    #         locator = self.page.locator(f"xpath={xpath}")
    #         locator.wait_for(state="visible", timeout=timeout)
    #         locator.click()
    #         self.logger.info(f"Clicked element by XPath: {xpath}")
    #         self.attach_screenshot(f"After {description}")
    #         return True
    #     except TimeoutError:
    #         self.logger.error(f"Element not visible for XPath click: {xpath}")
    #         return False


    @allure.step("Click element by XPath: {xpath}")
    def click_by_xpath(
            self,
            xpath: str,
            description: str = "Click by XPath",
            timeout: int = 10000
    ) -> bool:

        try:

            self.check_application_errors()

            locator = self.page.locator(f"xpath={xpath}")

            locator.wait_for(
                state="visible",
                timeout=timeout
            )

            locator.click()

            self.logger.info(
                f"Clicked element by XPath: {xpath}"
            )

            self.attach_screenshot(
                f"After {description}"
            )

            return True

        except Exception as e:

            self.attach_screenshot(
                f"FAILED_{description}"
            )

            raise AssertionError(
                f"{description} Failed : {e}"
            )
   
        
    @allure.step("Fill input field by XPath: {xpath}")
    def fill_by_xpath(self, xpath: str, text: str, description: str = "Fill by XPath", timeout: int = 30000) -> bool:
            """Wait until element located by XPath is visible, then fill"""
            try:
                locator = self.page.locator(f"xpath={xpath}")
                locator.wait_for(state="visible", timeout=timeout)
                locator.fill(text)
                self.logger.info(f"Filled element by XPath: {xpath} with text: {text}")
                self.attach_screenshot(f"After {description}")
                return True
            except Exception as e:
                self.attach_screenshot(f"FAILED_{description}")
            raise AssertionError(f"{description} Failed : {e}")
        

    @allure.step("Get text content")
    def get_text(self, locator, description: str = "Get text", timeout: int = 30000) -> str:
        try:
            locator.wait_for(state="visible", timeout=timeout)
            text = locator.text_content()
            self.logger.info(f"Got text from {description}: {text}")
            allure.attach(text, name=f"Text content - {description}", attachment_type=allure.attachment_type.TEXT)
            return text
        except TimeoutError:
            self.logger.error(f"Get text failed for: {description}")
            return ""
        
  

    @allure.step("Click element")
    def click_by_getbyrole(
        self,
        get_by_role,                     # can be tuple OR string (role)
        description: str = "Click action",
        timeout: int = 30_000,
        **kwargs                         # optional: name="...", exact=True
    ) -> bool:
        """
        Supports:
        A) ("role", "link", {"name": "Purchase", "exact": True})
        B) ("link", {"name": "Purchase", "exact": True})
        C) "link", name="Purchase", exact=True
        """
        # ---- Resolve BEFORE try (prevents UnboundLocalError) ----
        if isinstance(get_by_role, tuple):
            if len(get_by_role) == 3 and str(get_by_role[0]).lower() == "role":
                _, role, extra = get_by_role
                extra = dict(extra or {})
            elif len(get_by_role) == 2:
                role, extra = get_by_role
                extra = dict(extra or {})
            else:
                raise ValueError(f"Unsupported role tuple format: {get_by_role}")

            # kwargs (like name/exact) override tuple extras when provided
            if "name" in kwargs:  extra["name"]  = kwargs["name"]
            if "exact" in kwargs: extra["exact"] = kwargs["exact"]

            locator = self.page.get_by_role(role, **extra)
            for_log = f'get_by_role("{role}", {extra})'
            heal_name  = extra.get("name")
            heal_exact = extra.get("exact", False)
        else:
            # role string + kwargs
            role = str(get_by_role)
            locator = self.page.get_by_role(role, **kwargs)
            for_log = f'get_by_role("{role}", {kwargs})'
            heal_name  = kwargs.get("name")
            heal_exact = kwargs.get("exact", False)

        try:
            locator.wait_for(state="visible", timeout=timeout)
            locator.click()
            self.logger.info(f"Clicked element: {description} using {for_log}")
            self.attach_screenshot(f"After {description}")
            return True

        except PlaywrightTimeoutError as e:
            self.logger.error(f"[Timeout] {description} | {for_log} | {e}")
            # Optional: Auto‑heal fallback (defensive if healer disabled)
            try:
                healed = self.auto_healer.get_by_role(role, name=heal_name, exact=bool(heal_exact))
            except Exception:
                healed = None
            if healed:
                healed.click()
                self.attach_screenshot(f"After AutoHeal {description}")
                return True
            return False

        except Exception as e:
            self.logger.error(f"[Click failed] {description} | {for_log} | {e}")
            raise AssertionError(f"{description} Failed")
        
    @allure.step("Fill input field")
    def fill_by_getbyrole(
        self,
        get_by_role,  # can be tuple OR string (role)
        text: str,
        description="Fill action",
        timeout: int = 30000,
        **kwargs  # optional: name="...", exact=True
    ) -> bool:
        """Fill with auto-heal fallback (handles same patterns as click_by_getbyrole)"""
        # resolve locator before try so we can reference it in except blocks
        if isinstance(get_by_role, tuple):
            if len(get_by_role) == 3 and str(get_by_role[0]).lower() == "role":
                _, role, extra = get_by_role
                extra = dict(extra or {})
            elif len(get_by_role) == 2:
                role, extra = get_by_role
                extra = dict(extra or {})
            else:
                raise ValueError(f"Unsupported role tuple format: {get_by_role}")

            # kwargs override tuple extras when provided
            if "name" in kwargs:
                extra["name"] = kwargs["name"]
            if "exact" in kwargs:
                extra["exact"] = kwargs["exact"]

            locator = self.page.get_by_role(role, **extra)
            heal_name = extra.get("name")
            heal_exact = extra.get("exact", False)
        else:
            # string role + kwargs
            role = str(get_by_role)
            locator = self.page.get_by_role(role, **kwargs)
            heal_name = kwargs.get("name")
            heal_exact = kwargs.get("exact", False)

        try:
            locator.wait_for(state="visible", timeout=timeout)
            locator.fill(text)
            self.logger.info(f"Filled element ({description}) with text: {text}")
            self.attach_screenshot(f"After {description}")
            return True
        except TimeoutError:
            self.logger.error(f"Fill failed for: {description}")
            # auto-heal attempt
            try:
                healed_locator = self.auto_healer.get_by_role(role, name=heal_name, exact=bool(heal_exact))
            except Exception:
                healed_locator = None
            if healed_locator:
                self.logger.info(f"Auto-heal applied for: {description}")
                healed_locator.fill(text)
                self.attach_screenshot(f"After auto-heal {description}")
                return True
            raise AssertionError(f"{description} Failed")
        
    @allure.step("Hover element by role")
    def hover_by_getbyrole(self, get_by_role, description="Hover action", timeout: int = 30000) -> bool:
        """Hover with auto-heal fallback"""
        try:
            if isinstance(get_by_role, str):
                locator = self.page.get_by_role(get_by_role)
            else:
                locator = get_by_role

            locator.wait_for(state="visible", timeout=timeout)
            locator.hover()
            self.logger.info(f"Hovered element ({description}) successfully")
            self.attach_screenshot(f"After {description}")
            return True
        except TimeoutError:
            self.logger.error(f"Hover failed for: {description}")
            healed_locator = self.auto_healer.get_by_role(str(locator))
            if healed_locator:
                self.logger.info(f"Auto-heal applied for: {description}")
                healed_locator.hover()
                self.attach_screenshot(f"After auto-heal {description}")
                return True
            return False
        
    @allure.step("Click element by text")
    def click_by_getbytext(self, text: str, description="Click action", exact: bool = False, timeout: int = 30000) -> bool:
        """Click with auto-heal fallback"""
        try:
            locator = self.page.get_by_text(text, exact=exact)
            locator.wait_for(state="visible", timeout=timeout)
            locator.click()
            self.logger.info(f"Clicked element ({description}) successfully")
            self.attach_screenshot(f"After {description}")
            return True
        except TimeoutError:
            self.logger.error(f"Click failed for: {description}")
            healed_locator = self.auto_healer.get_by_text(text, exact=exact)
            if healed_locator:
                self.logger.info(f"Auto-heal applied for: {description}")
                healed_locator.click()
                self.attach_screenshot(f"After auto-heal {description}")
                return True
            return False
        
    @allure.step("Hover element by text")
    def hover_by_getbytext(self, text: str, description="Hover action", exact: bool = False, timeout: int = 30000) -> bool:
        """Hover with auto-heal fallback"""
        try:
            locator = self.page.get_by_text(text, exact=exact)
            locator.wait_for(state="visible", timeout=timeout)
            locator.hover()
            self.logger.info(f"Hovered element ({description}) successfully")
            self.attach_screenshot(f"After {description}")
            return True
        except TimeoutError:
            self.logger.error(f"Hover failed for: {description}")
            healed_locator = self.auto_healer.get_by_text(text, exact=exact)
            if healed_locator:
                self.logger.info(f"Auto-heal applied for: {description}")
                healed_locator.hover()
                self.attach_screenshot(f"After auto-heal {description}")
                return True
            return False
    
    
    
    # ---------------------------
    # Assertion helpers
    # ---------------------------
 
    @allure.step("Assert element is visible")
    def assert_visible(self, locator, description: str = "Visibility check", timeout: int = 30000):
        loc: Locator = self._as_locator(locator)
        try:
            loc.wait_for(state="visible", timeout=timeout)
            assert loc.is_visible(), f"Expected {description} to be visible, but it was not."
            self.logger.info(f"Assertion passed: {description} is visible")
            self.attach_screenshot(f"{description} visible")
        except PlaywrightTimeoutError:
            self.logger.error(f"Assertion failed: {description} not visible within {timeout}ms")
            raise AssertionError(f"{description} not visible within {timeout}ms")

    @allure.step("Assert element has exact text")
    def assert_text(self, locator, expected_text: str, description: str = "Text check", timeout: int = 30000):
        try:
            loc: Locator = self._as_locator(locator)
            loc.wait_for(state="visible", timeout=timeout)
            actual = loc.inner_text(timeout=timeout).strip()
            assert actual == expected_text, f"{description}: expected '{expected_text}', got '{actual}'"
            self.logger.info(f"Assertion passed: {description} text matches expected")
            allure.attach(actual, name=f"Text content - {description}", attachment_type=allure.attachment_type.TEXT)
        except TimeoutError:
                self.logger.error(f"Assertion failed: {description} not visible within {timeout}ms")
                raise AssertionError(f"{description} not visible within {timeout}ms")
        
    # ---------------------------
    # Locator helpers
    # ---------------------------
    def locator(self, selector: str):
        return self.page.locator(selector)

    def get_by_role(self, role: str, name: str = None, exact: bool = False):
        return self.page.get_by_role(role, name=name, exact=exact)

    def get_by_text(self, text: str, exact: bool = False):
        return self.page.get_by_text(text, exact=exact)

    def get_by_label(self, label: str, exact: bool = False):
        return self.page.get_by_label(label, exact=exact)

    def get_by_placeholder(self, placeholder: str, exact: bool = False):
        return self.page.get_by_placeholder(placeholder, exact=exact)

    def get_by_test_id(self, test_id: str):
        return self.page.get_by_test_id(test_id)

    def locator_by_xpath(self, xpath: str):
        return self.page.locator(f"xpath={xpath}")
    
    def wait_for_locator(self, selector, timeout: int = 30_000):
        self.page.locator(selector).wait_for(timeout=timeout)

    
    def get_inner_text(self, selector):
        if selector.startswith("/"):
            selector = f"xpath={selector}"
        return self.page.locator(selector).inner_text()


    def expect_to_contain(self, selector, text: str, timeout: int = 30_000):
        """wrapper round expect(locator).to_contain_text()"""
        expect(self.page.locator(selector)).to_contain_text(text,timeout=timeout)
    
    def wait_for_page_load(self,
                           state: str = "load",
                           timeout: int = 30_000) -> None:
        self.page.wait_for_load_state(state, timeout=timeout)    



    @allure.step("Select option in dropdown")
    def select_by_locator(self, locator, description="Select option", timeout: int = 30000, **kwargs) -> bool:
        
        try:
            if isinstance(locator, str):
                locator = self.page.locator(locator)
            
            locator.wait_for(state="visible", timeout=timeout)
            locator.select_option(**kwargs)
            self.logger.info(f"Selected option in {description} with {kwargs}")
            self.attach_screenshot(f"After {description}")
            return True
        except TimeoutError:
            self.logger.error(f"Select failed for: {description}")
            # Auto-heal attempt: try to find a similar select element
            healed_locator = self.auto_healer.locator(str(locator))
            if healed_locator:
                self.logger.info(f"Auto-heal applied for: {description}")
                healed_locator.select_option(**kwargs)
                self.attach_screenshot(f"After auto-heal {description}")
                return True
            return False
        
  
    @allure.step("Select by XPath (native <select>)")
    def select_by_xpath(
        self,
        select_xpath: str,
        *,
        by: Literal["label","value","index"] = "label",
        option: str,
        description: str = "Select option",
        timeout: int = 30_000
    ) -> bool:
        
        try:
            locator = self.page.locator(f"xpath={select_xpath}")
            locator.wait_for(state="visible", timeout=timeout)

            if by == "label":
                locator.select_option(label=str(option))
            elif by == "value":
                locator.select_option(value=str(option))
            elif by == "index":
                locator.select_option(index=int(option))
            else:
                raise ValueError("by must be one of: 'label', 'value', 'index'")

            self.logger.info(f"Selected option in {description}: by={by}, option={option}")
            self.attach_screenshot(f"After {description}")
            return True

        except PlaywrightTimeoutError:
            self.logger.error(f"[Timeout] {description} (select not visible) | {select_xpath}")
        except Exception as e:
            self.logger.error(f"[Select failed] {description} | {e}")

        # Auto-heal fallback
        try:
            if self.auto_healer:
                healed_xpath = self.auto_healer.locator(select_xpath) 
                if healed_xpath:
                    self.logger.info(f"Auto-heal applied for: {description}")
                    healed = self.page.locator(f"xpath={healed_xpath}")
                    healed.wait_for(state="visible", timeout=timeout)
                    if by == "label":
                        healed.select_option(label=str(option))
                    elif by == "value":
                        healed.select_option(value=str(option))
                    else:
                        healed.select_option(index=int(option))
                    self.attach_screenshot(f"After auto-heal {description}")
                    return True
        except Exception as e:
            self.logger.error(f"[Auto-heal failed] {description} | {e}")

        raise AssertionError(f"{description} Failed")
    
    def pause(self, seconds: int):
        """Pause execution for a given number of seconds"""
        self.logger.info(f"Pausing for {seconds} seconds")
        self.page.wait_for_timeout(seconds * 1000)


    
    def _as_locator(self, candidate: Union[str, Locator]) -> Locator:
        # Convert selectors (str) to Locator objects
        return self.page.locator(candidate) if isinstance(candidate, str) else candidate

    

    def _default_logger(self):
        import logging
        logger = logging.getLogger(self.__class__.__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    @allure.step("Select radio button")
    def select_radio_button(self, locator, description="Radio select", timeout: int = 30000) -> bool:
        try:
            # Ensure locator is a Playwright Locator
            if isinstance(locator, str):
                locator = self.page.locator(locator)
    
            locator.wait_for(state="visible", timeout=timeout)
    
            # Use check() only if it's a native radio input, else fallback to click()
            try:
                locator.check()
            except Exception:
                locator.click()
    
            self.logger.info(f"Selected radio button ({description})")
            self.attach_screenshot(f"After {description}")
            return True
    
        except TimeoutError:
            self.logger.error(f"Radio select failed for: {description}")
            healed_locator = self.auto_healer.locator(locator)  # pass original selector string if available
            if healed_locator:
                try:
                    healed_locator.check()
                except Exception:
                    healed_locator.click()
                self.logger.info(f"Auto-heal applied for: {description}")
                self.attach_screenshot(f"After auto-heal {description}")
                return True
            return False
    

    @allure.step("Check checkbox")
    def check_checkbox(self, locator, description="Check action", timeout: int = 30000) -> bool:
        try:
            if isinstance(locator, str):
                locator = self.page.locator(locator)
 
            locator.wait_for(state="visible", timeout=timeout)
            locator.check()
            self.logger.info(f"Checked element ({description})")
            self.attach_screenshot(f"After {description}")
            return True
        except TimeoutError:
            self.logger.error(f"Checkbox check failed for: {description}")
            healed_locator = self.auto_healer.locator(str(locator))
            if healed_locator:
                healed_locator.check()
                self.logger.info(f"Auto-heal applied for: {description}")
                self.attach_screenshot(f"After auto-heal {description}")
                return True
            return False
        
    @allure.step("Assert JSON 'status' is in allowed values")
    def assert_status_in(
        self,
        locator: Union[Locator, str],
        allowed_statuses=None,
        description: str = "Status validation",
        timeout: int = 30000
    ):
        if allowed_statuses is None:
            #allowed_statuses = {"APPROVED", "NOT APPROVED", "CAPTURED", "NOT CAPTURED", "AUTHENTICATED", "NOT AUTHENTICATED"}
            allowed_statuses = {"APPROVED", "CAPTURED", "AUTHENTICATED"}
        loc: Locator = self._as_locator(locator)
        try:
            # 1) Wait for visibility and get text
            loc.wait_for(state="visible", timeout=timeout)
            raw_text = loc.inner_text(timeout=timeout)
            # 2) Extract JSON payload (handles 'Result: { ... }')
            payload_text = self._extract_json_from_text(raw_text)
            data = json.loads(payload_text)
            # 3) Pull status
            status_value = data.get("status", "")
            status_str = (status_value or "").strip()
            # 4) Assert membership
            if status_str not in allowed_statuses:
                msg = (f"{description} failed: 'status' not in allowed set.\n"
                       f"Allowed: {sorted(allowed_statuses)}\n"
                       f"Actual: '{status_str}'")
                self.logger.error(msg)
                allure.attach(
                    json.dumps(data, indent=2, ensure_ascii=False),
                    name=f"Actual JSON - {description}",
                    attachment_type=allure.attachment_type.JSON
                )
                allure.attach(
                    status_str,
                    name=f"Actual status - {description}",
                    attachment_type=allure.attachment_type.TEXT
                )
                raise AssertionError(msg)
            # 5) Pass
            self.logger.info(f"Assertion passed: {description} -> status='{status_str}'")
            allure.attach(status_str, name=f"Status (passed) - {description}", attachment_type=allure.attachment_type.TEXT)
        except PlaywrightTimeoutError:
            err = f"{description}: element not visible within {timeout}ms"
            self.logger.error(err)
            raise AssertionError(err)
        except json.JSONDecodeError as e:
            self.logger.error(f"{description}: JSON parse error: {str(e)}")
            allure.attach(raw_text, name="Raw element text (debug)", attachment_type=allure.attachment_type.TEXT)
            raise AssertionError(f"{description}: JSON parse error: {str(e)}")

    # ---------- Helpers (same as before) ----------

    def _extract_json_from_text(self, text: str) -> str:
        # Try balanced object
        start = text.find('{')
        if start != -1:
            depth = 0
            for i in range(start, len(text)):
                if text[i] == '{':
                    depth += 1
                elif text[i] == '}':
                    depth -= 1
                    if depth == 0:
                        return text[start:i+1]
        # Try balanced array
        start = text.find('[')
        if start != -1:
            depth = 0
            for i in range(start, len(text)):
                if text[i] == '[':
                    depth += 1
                elif text[i] == ']':
                    depth -= 1
                    if depth == 0:
                        return text[start:i+1]
        # Fallback regex
        m = re.search(r'(\{.*\}|\[.*\])', text, flags=re.S)
        if m:
            return m.group(1)
        return text.strip()
    
    @allure.step("Check Application Errors")
    def check_application_errors(self):

        current_url = self.page.url

        error_urls = [
            "ErrorPages",
            "LoggedOut"
        ]

        for url in error_urls:
            if url in current_url:
                raise AssertionError(
                    f"Application redirected to error page: {current_url}"
                )

        try:
            body_text = self.page.locator("body").text_content()

            error_messages = [
                "Merchant information is insufficient",
                "Internal Server Error",
                "Something went wrong",
                "Session expired"
            ]

            for msg in error_messages:
                if msg in body_text:
                    raise AssertionError(
                        f"Application Error Found: {msg}"
                    )

        except Exception:
            pass



