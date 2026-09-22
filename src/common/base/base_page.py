"""
BasePage provides the core Playwright actions (navigate, click_by_*, fill_by_*, hover_by_*, select_*, assert_*, get_text, and locator helpers). It includes a simple heuristic LocatorAutoHeal fallback using Playwright’s own strategies (no AI/LLM). Every step is logged to the console and recorded into ExtentReporter for inclusion in the final HTML report.
"""
from __future__ import annotations

import os
import re
import time
from pathlib import Path
from typing import Optional

import pyotp
from playwright.sync_api import Page, Locator, TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError

from src.common.utilities.logger import get_logger
from src.common.utilities.config_loader import ConfigManager
from src.common.utilities.extent_reporter import reporter

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class ActionFailedError(Exception):
    """
    Raised when a base action (click/fill/select/navigate/etc.) fails after
    any retry/auto-heal attempt, so the test stops at this step instead of
    silently continuing to the next line. Distinguishes step-level action
    failures from assertion failures (AssertionError) in logs/reports while
    still failing the pytest test either way.
    """
    pass


class LocatorAutoHeal:
    """
    Heuristic locator fallback using ONLY Playwright's own strategies.
    Playwright has no built-in AI/self-healing locator feature - this is a
    best-effort chain of alternate lookups (role/text/placeholder/label
    matches derived from the broken selector), not true self-healing.
    """

    def __init__(self, page: Page):
        self.page = page

    @staticmethod
    def _extract_hint(selector: str) -> str:
        cleaned = selector.strip("#.[]='\" ")
        cleaned = re.sub(r"[-_]+", " ", cleaned).strip()
        return cleaned

    def _first_visible(self, candidates: list[Locator]) -> Optional[Locator]:
        for cand in candidates:
            try:
                if cand.count() > 0 and cand.first.is_visible():
                    return cand.first
            except Exception:
                continue
        return None

    def locator(self, original_selector: str) -> Optional[Locator]:
        """Best-effort fallback: derives a text hint from the broken selector and tries get_by_text/get_by_role/get_by_placeholder/get_by_label until one matches a visible element. Returns None if nothing matched."""
        hint = self._extract_hint(original_selector)
        if not hint:
            return None
        candidates = [
            self.page.get_by_text(hint, exact=False),
            self.page.get_by_role("button", name=hint),
            self.page.get_by_placeholder(hint),
            self.page.get_by_label(hint),
        ]
        return self._first_visible(candidates)

    def get_by_role(self, role: str, name: Optional[str] = None) -> Optional[Locator]:
        """Fallback lookup by ARIA role + accessible name. Returns None if no name given or no match found."""
        if not name:
            return None
        try:
            cand = self.page.get_by_role(role, name=name)
            return cand if cand.count() > 0 else None
        except Exception:
            return None

    def get_by_text(self, text: str, exact: bool = False) -> Optional[Locator]:
        """Fallback lookup by visible text content. Returns None if no match found."""
        try:
            cand = self.page.get_by_text(text, exact=exact)
            return cand if cand.count() > 0 else None
        except Exception:
            return None


class BasePage:
    def __init__(self, page: Page, module_name: str = "General"):
        self.page = page
        self.logger = get_logger(self.__class__.__name__)
        self.auto_healer = LocatorAutoHeal(page)
        self.module_name = module_name
        self.bank = ConfigManager.load_bank_config()["bank"]
        self.screenshot_dir = PROJECT_ROOT / "reports" / "screenshots" / module_name
        os.makedirs(self.screenshot_dir, exist_ok=True)
        self.screenshot_count = 1

    # ------------------------------------------------------------------ #
    def attach_screenshot(self, step_name: str) -> str:
        """Save screenshot in the module folder and record it against the
        currently running test in the ExtentReporter."""
        file_name = f"{self.screenshot_count:03d}_{step_name}.png"
        path = self.screenshot_dir / file_name
        try:
            self.page.screenshot(path=str(path), full_page=True)
        except Exception as exc:
            self.logger.error(f"Could not capture screenshot: {exc}")
            return ""
        self.screenshot_count += 1
        return str(path)

    def _record(self, message: str, level: str = "info", screenshot_path: Optional[str] = None) -> None:
        try:
            reporter.log(message, level=level, screenshot_path=screenshot_path)
        except Exception as e:
            self.logger.error(f"Failed to record step to report: {e}")

    # ------------------------------------------------------------------ #
    # Navigation
    # ------------------------------------------------------------------ #
    def navigate(self, url: str, timeout: int = 30000) -> bool:
        """Navigates the browser to url. Returns True on success; raises ActionFailedError on failure."""
        try:
            self.page.goto(url, timeout=timeout)
            self.logger.info(f"Navigated to URL: {url}")
            self._record(f"Navigated to URL: {url}", "info")
            return True
        except (PlaywrightTimeoutError, PlaywrightError) as e:
            self.logger.error(f"Failed to navigate to URL: {url} ({e})")
            shot = self.attach_screenshot("navigate_failed")
            self._record(f"Failed to navigate to URL: {url}", "error", shot)
            raise ActionFailedError(f"Failed to navigate to URL: {url}")

    # ------------------------------------------------------------------ #
    # Role-based actions
    # ------------------------------------------------------------------ #
    def hover_by_role(self, role: str, name: str, exact: bool = True, timeout: int = 10000) -> bool:
        """Hovers over an element found by ARIA role + accessible name. Raises on failure after screenshotting."""
        try:
            element = self.page.get_by_role(role, name=name, exact=exact)
            element.wait_for(state="visible", timeout=timeout)
            element.hover()
            self.logger.info(f"Hovered on element with role '{role}' and name '{name}'")
            self._record(f"Hovered on role '{role}' name '{name}'")
            return True
        except Exception as e:
            self.logger.error(f"Failed to hover on role '{role}' with name '{name}': {e}")
            shot = self.attach_screenshot(f"hover_by_role_failed_{role}")
            self._record(f"Failed to hover on role '{role}' name '{name}': {e}", "error", shot)
            raise

    def fill_by_role(self, role: str, name: str, value: str, use_regex: bool = False) -> None:
        """Fills a text field found by ARIA role + accessible name (use_regex allows a regex name match). Raises on failure."""
        try:
            if use_regex:
                locator = self.page.get_by_role(role, name=re.compile(name, re.I))
            else:
                locator = self.page.get_by_role(role, name=name)
            locator.wait_for(state="visible", timeout=10000)
            locator.fill(value)
            self.logger.info(f"Filled '{value}' in role '{role}' with name '{name}'")
            self._record(f"Filled role '{role}' name '{name}' with '{value}'")
        except Exception as e:
            self.logger.error(f"Failed to fill role '{role}' with name '{name}': {e}")
            shot = self.attach_screenshot(f"fill_by_role_failed_{role}")
            self._record(f"Failed to fill role '{role}' name '{name}': {e}", "error", shot)
            raise

    def click_by_role(self, role: str, name: str, exact: bool = True, timeout: int = 10000) -> None:
        """Clicks an element found by ARIA role + accessible name. Raises on failure after screenshotting."""
        try:
            element = self.page.get_by_role(role, name=name, exact=exact)
            element.wait_for(state="visible", timeout=timeout)
            element.click()
            self.logger.info(f"Clicked element with role '{role}' and name '{name}'")
            self._record(f"Clicked role '{role}' name '{name}'")
        except Exception as e:
            self.logger.error(f"Failed to click role '{role}' with name '{name}': {e}")
            shot = self.attach_screenshot(f"click_by_role_failed_{role}")
            self._record(f"Failed to click role '{role}' name '{name}': {e}", "error", shot)
            raise

    # ------------------------------------------------------------------ #
    # Locator-based actions (with heuristic auto-heal fallback)
    # ------------------------------------------------------------------ #
    def click_by_locator(self, locator, description: str = "Click action", timeout: int = 30000) -> bool:
        """Clicks an element given as a CSS selector string or a resolved Playwright Locator. Retries once via heuristic auto-heal on timeout. Returns True on success; raises ActionFailedError on failure."""
        try:
            if isinstance(locator, str):
                locator = self.page.locator(locator)
            locator.wait_for(state="visible", timeout=timeout)
            locator.click()
            self.logger.info(f"Clicked element: {description}")
            self._record(f"Clicked: {description}")
            return True
        except (PlaywrightTimeoutError, PlaywrightError) as e:
            self.logger.error(f"Click failed for: {description} ({e})")
            fail_shot = self.attach_screenshot(f"click_failed_{description}")
            self._record(f"Click failed for: {description}", "fail", fail_shot)
            healed = self.auto_healer.locator(str(locator))
            if healed:
                self.logger.info(f"Auto-heal applied for: {description}")
                healed.click()
                shot = self.attach_screenshot(f"after_autoheal_{description}")
                self._record(f"Auto-heal applied for: {description}", "info", shot)
                return True
            raise ActionFailedError(f"Click failed for: {description}")

    def fill_by_locator(self, locator, text: str, description: str = "Fill action", timeout: int = 30000) -> bool:
        """Fills a text field given as a CSS selector string or a resolved Locator. Retries once via heuristic auto-heal on timeout. Returns True on success; raises ActionFailedError on failure."""
        try:
            if isinstance(locator, str):
                locator = self.page.locator(locator)
            locator.wait_for(state="visible", timeout=timeout)
            locator.fill(text)
            self.logger.info(f"Filled element ({description}) with text: {text}")
            self._record(f"Filled {description} with '{text}'")
            return True
        except (PlaywrightTimeoutError, PlaywrightError) as e:
            self.logger.error(f"Fill failed for: {description} ({e})")
            fail_shot = self.attach_screenshot(f"fill_failed_{description}")
            self._record(f"Fill failed for: {description}", "fail", fail_shot)
            healed = self.auto_healer.locator(str(locator))
            if healed:
                self.logger.info(f"Auto-heal applied for: {description}")
                healed.fill(text)
                shot = self.attach_screenshot(f"after_autoheal_{description}")
                self._record(f"Auto-heal applied for: {description}", "info", shot)
                return True
            raise ActionFailedError(f"Fill failed for: {description}")

    def select_by_locator(self, locator, value: str, description: str = "Select dropdown", timeout: int = 30000) -> bool:
        """Selects an option in a native <select> dropdown by value. Returns True on success; raises ActionFailedError on failure."""
        try:
            if isinstance(locator, str):
                locator = self.page.locator(locator)
            locator.wait_for(state="visible", timeout=timeout)
            locator.select_option(value)
            self.logger.info(f"{description}: {value}")
            self._record(f"{description}: {value}")
            return True
        except Exception as e:
            self.logger.error(f"{description} failed: {e}")
            shot = self.attach_screenshot(f"select_failed_{description}")
            self._record(f"{description} failed: {e}", "fail", shot)
            raise ActionFailedError(f"{description} failed: {e}")

    def select_custom_dropdown(self, dropdown_id: str, value: str) -> None:
        """Opens a custom (non-native) JS dropdown by its container id and clicks the option matching value text. Raises on failure."""
        try:
            self.page.locator(f"#{dropdown_id}").click()
            option = self.page.locator(f"#{dropdown_id} span", has_text=value)
            option.wait_for(state="visible", timeout=10000)
            option.click()
            self.logger.info(f"Selected '{value}' from dropdown '{dropdown_id}'")
            self._record(f"Selected '{value}' from dropdown '{dropdown_id}'")
        except Exception as e:
            self.logger.error(f"Dropdown selection failed: {e}")
            shot = self.attach_screenshot(f"dropdown_failed_{dropdown_id}")
            self._record(f"Dropdown selection failed: {e}", "error", shot)
            raise

    def click_by_xpath(self, xpath: str, description: str = "Click by XPath", timeout: int = 30000) -> bool:
        """Clicks an element located by an XPath expression. Returns True on success; raises ActionFailedError on failure."""
        try:
            locator = self.page.locator(f"xpath={xpath}")
            locator.wait_for(state="visible", timeout=timeout)
            locator.click()
            self.logger.info(f"Clicked element by XPath: {xpath}")
            self._record(f"Clicked by XPath: {xpath}")
            return True
        except (PlaywrightTimeoutError, PlaywrightError) as e:
            self.logger.error(f"Element not visible for XPath click: {xpath} ({e})")
            shot = self.attach_screenshot(f"xpath_click_failed_{description}")
            self._record(f"XPath click failed: {xpath}", "fail", shot)
            raise ActionFailedError(f"XPath click failed: {xpath}")

    # ------------------------------------------------------------------ #
    # get_by_role / get_by_text based actions (auto-heal fallback)
    # ------------------------------------------------------------------ #
    def click_by_getbyrole(self, get_by_role, description: str = "Click action", timeout: int = 30000) -> bool:
        """Clicks a role string or a pre-resolved get_by_role() Locator. Returns True on success; raises ActionFailedError on failure."""
        try:
            locator = self.page.get_by_role(get_by_role) if isinstance(get_by_role, str) else get_by_role
            locator.wait_for(state="visible", timeout=timeout)
            locator.click()
            self.logger.info(f"Clicked element: {description}")
            self._record(f"Clicked: {description}")
            return True
        except Exception as e:
            self.logger.error(f"Click failed for: {description} | Error: {e}")
            shot = self.attach_screenshot(f"click_getbyrole_failed_{description}")
            self._record(f"Click failed for: {description} | {e}", "fail", shot)
            raise ActionFailedError(f"Click failed for: {description} | {e}")

    def fill_by_getbyrole(self, get_by_role, text: str, description: str = "Fill action", timeout: int = 30000) -> bool:
        """Fills a role string or a pre-resolved get_by_role() Locator; silently skips if text is blank/None/"(blank)". Raises on other failures."""
        try:
            locator = self.page.get_by_role(get_by_role) if isinstance(get_by_role, str) else get_by_role
            if text in [None, "", "(blank)"]:
                self.logger.info(f"Skipping fill for {description} (blank value)")
                self._record(f"Skipped fill for {description} (blank value)")
                return True
            locator.wait_for(state="visible", timeout=timeout)
            locator.fill(text)
            self.logger.info(f"Filled element ({description}) with text: {text}")
            self._record(f"Filled {description} with '{text}'")
            return True
        except Exception as e:
            self.logger.error(f"Fill failed for: {description} | Error: {e}")
            shot = self.attach_screenshot(f"fill_getbyrole_failed_{description}")
            self._record(f"Fill failed for: {description} | {e}", "fail", shot)
            raise

    def hover_by_getbyrole(self, get_by_role, description: str = "Hover action", timeout: int = 30000) -> bool:
        """Hovers a role string or a pre-resolved get_by_role() Locator. Retries once via auto-heal on timeout. Returns True on success; raises ActionFailedError on failure."""
        try:
            locator = self.page.get_by_role(get_by_role) if isinstance(get_by_role, str) else get_by_role
            locator.wait_for(state="visible", timeout=timeout)
            locator.hover()
            self.logger.info(f"Hovered element ({description}) successfully")
            self._record(f"Hovered: {description}")
            return True
        except (PlaywrightTimeoutError, PlaywrightError) as e:
            self.logger.error(f"Hover failed for: {description} ({e})")
            fail_shot = self.attach_screenshot(f"hover_getbyrole_failed_{description}")
            self._record(f"Hover failed for: {description}", "fail", fail_shot)
            healed = self.auto_healer.get_by_role(str(get_by_role))
            if healed:
                self.logger.info(f"Auto-heal applied for: {description}")
                healed.hover()
                shot = self.attach_screenshot(f"after_autoheal_{description}")
                self._record(f"Auto-heal applied for: {description}", "info", shot)
                return True
            raise ActionFailedError(f"Hover failed for: {description}")

    def click_by_getbytext(self, text: str, description: str = "Click action", exact: bool = False, timeout: int = 30000) -> bool:
        """Clicks an element found by visible text. Retries once via auto-heal on timeout. Returns True on success; raises ActionFailedError on failure."""
        try:
            locator = self.page.get_by_text(text, exact=exact)
            locator.wait_for(state="visible", timeout=timeout)
            locator.click()
            self.logger.info(f"Clicked element ({description}) successfully")
            self._record(f"Clicked by text '{text}': {description}")
            return True
        except (PlaywrightTimeoutError, PlaywrightError) as e:
            self.logger.error(f"Click failed for: {description} ({e})")
            fail_shot = self.attach_screenshot(f"click_getbytext_failed_{description}")
            self._record(f"Click failed for: {description}", "fail", fail_shot)
            healed = self.auto_healer.get_by_text(text, exact=exact)
            if healed:
                self.logger.info(f"Auto-heal applied for: {description}")
                healed.click()
                shot = self.attach_screenshot(f"after_autoheal_{description}")
                self._record(f"Auto-heal applied for: {description}", "info", shot)
                return True
            raise ActionFailedError(f"Click failed for: {description}")

    def hover_by_getbytext(self, text: str, description: str = "Hover action", exact: bool = False, timeout: int = 30000) -> bool:
        """Hovers an element found by visible text. Retries once via auto-heal on timeout. Returns True on success; raises ActionFailedError on failure."""
        try:
            locator = self.page.get_by_text(text, exact=exact)
            locator.wait_for(state="visible", timeout=timeout)
            locator.hover()
            self.logger.info(f"Hovered element ({description}) successfully")
            self._record(f"Hovered by text '{text}': {description}")
            return True
        except (PlaywrightTimeoutError, PlaywrightError) as e:
            self.logger.error(f"Hover failed for: {description} ({e})")
            fail_shot = self.attach_screenshot(f"hover_getbytext_failed_{description}")
            self._record(f"Hover failed for: {description}", "fail", fail_shot)
            healed = self.auto_healer.get_by_text(text, exact=exact)
            if healed:
                self.logger.info(f"Auto-heal applied for: {description}")
                healed.hover()
                shot = self.attach_screenshot(f"after_autoheal_{description}")
                self._record(f"Auto-heal applied for: {description}", "info", shot)
                return True
            raise ActionFailedError(f"Hover failed for: {description}")

    # ------------------------------------------------------------------ #
    # Read / assertion helpers
    # ------------------------------------------------------------------ #
    def get_text(self, locator, description: str = "Get text", timeout: int = 30000) -> str:
        """Reads the text content of an element. Returns "" on timeout instead of raising."""
        try:
            locator.wait_for(state="visible", timeout=timeout)
            text = locator.text_content()
            self.logger.info(f"Got text from {description}: {text}")
            self._record(f"Got text from {description}: {text}")
            return text
        except (PlaywrightTimeoutError, PlaywrightError) as e:
            self.logger.error(f"Get text failed for: {description} ({e})")
            shot = self.attach_screenshot(f"get_text_failed_{description}")
            self._record(f"Get text failed for: {description}", "fail", shot)
            return ""

    def assert_visible(self, locator, description: str = "Visibility check", timeout: int = 30000) -> None:
        """Asserts an element is visible; screenshots on both pass and fail. Raises AssertionError on failure."""
        try:
            locator.wait_for(state="visible", timeout=timeout)
            assert locator.is_visible(), f"Expected {description} to be visible, but it was not."
            self.logger.info(f"Assertion passed: {description} is visible")
            shot = self.attach_screenshot(f"{description}_visible")
            self._record(f"PASS: {description} is visible", "pass", shot)
        except (PlaywrightTimeoutError, AssertionError) as e:
            message = f"{description} not visible within {timeout}ms" if isinstance(e, PlaywrightTimeoutError) else str(e)
            self.logger.error(f"Assertion failed: {message}")
            shot = self.attach_screenshot(f"{description}_not_visible_FAILED")
            self._record(f"FAIL: {message}", "fail", shot)
            raise AssertionError(message)

    def assert_not_visible(self, locator, description: str = "Invisibility check", timeout: int = 5000) -> None:
        """Asserts an element is NOT visible (short default timeout, since this checks absence); screenshots on both pass and fail. Raises AssertionError on failure."""
        try:
            locator.wait_for(state="visible", timeout=timeout)
            is_visible = locator.is_visible()
        except PlaywrightTimeoutError:
            is_visible = False
        if is_visible:
            self.logger.error(f"Assertion failed: {description} was visible but should not be")
            shot = self.attach_screenshot(f"{description}_unexpectedly_visible_FAILED")
            self._record(f"FAIL: {description} was visible but should not be", "fail", shot)
            raise AssertionError(f"{description} was visible but should not be")
        self.logger.info(f"Assertion passed: {description} is not visible")
        shot = self.attach_screenshot(f"{description}_not_visible")
        self._record(f"PASS: {description} is not visible", "pass", shot)

    def assert_text(self, locator, expected_text: str, description: str = "Text assertion", timeout: int = 30000) -> None:
        """Asserts an element's exact text equals expected_text; screenshots on both pass and fail. Raises AssertionError with expected-vs-actual on mismatch."""
        try:
            locator.wait_for(state="visible", timeout=timeout)
            actual_text = locator.text_content()
            assert actual_text == expected_text, (
                f"Expected text '{expected_text}' for {description}, but got '{actual_text}'"
            )
            self.logger.info(f"Assertion passed: {description} text matched '{expected_text}'")
            shot = self.attach_screenshot(f"{description}_text_assertion")
            self._record(f"PASS: {description} matched '{expected_text}'", "pass", shot)
        except (PlaywrightTimeoutError, AssertionError) as e:
            message = f"{description} not visible within {timeout}ms" if isinstance(e, PlaywrightTimeoutError) else str(e)
            self.logger.error(f"Assertion failed: {message}")
            shot = self.attach_screenshot(f"{description}_text_assertion_FAILED")
            self._record(f"FAIL: {message}", "fail", shot)
            raise AssertionError(message)

    def assert_image_visible(self, locator, description: str = "Image validation", timeout: int = 30000) -> None:
        """Asserts an <img> is visible, has a non-empty src, and actually loaded (naturalWidth > 0). Raises AssertionError on any check failing."""
        try:
            image = locator
            image.wait_for(state="visible", timeout=timeout)
            assert image.is_visible(), f"{description} - Image not visible"
            src = image.get_attribute("src")
            assert src is not None and src != "", f"{description} - Image src missing"
            natural_width = image.evaluate("img => img.naturalWidth")
            assert natural_width > 0, f"{description} - Broken image"
            self.logger.info(f"{description} passed successfully")
            shot = self.attach_screenshot(f"{description}_image_assertion")
            self._record(f"PASS: {description}", "pass", shot)
        except Exception as e:
            self.logger.error(f"{description} failed: {e}")
            shot = self.attach_screenshot(f"{description}_image_assertion_FAILED")
            self._record(f"FAIL: {description}: {e}", "fail", shot)
            raise

    # ------------------------------------------------------------------ #
    # Checkboxes & Radio buttons
    # ------------------------------------------------------------------ #
    def check_by_locator(self, locator, description: str = "Check checkbox", timeout: int = 30000) -> bool:
        """Checks a checkbox/radio input. Retries once via auto-heal on timeout. Returns True on success; raises ActionFailedError on failure."""
        try:
            if isinstance(locator, str):
                locator = self.page.locator(locator)
            locator.wait_for(state="visible", timeout=timeout)
            locator.check()
            self.logger.info(f"Checked: {description}")
            self._record(f"Checked: {description}")
            return True
        except (PlaywrightTimeoutError, PlaywrightError) as e:
            self.logger.error(f"Check failed for: {description} ({e})")
            shot = self.attach_screenshot(f"check_failed_{description}")
            self._record(f"Check failed for: {description}", "fail", shot)
            healed = self.auto_healer.locator(str(locator))
            if healed:
                self.logger.info(f"Auto-heal applied for: {description}")
                healed.check()
                shot = self.attach_screenshot(f"after_autoheal_{description}")
                self._record(f"Auto-heal applied for: {description}", "info", shot)
                return True
            raise ActionFailedError(f"Check failed for: {description}")

    def uncheck_by_locator(self, locator, description: str = "Uncheck checkbox", timeout: int = 30000) -> bool:
        """Unchecks a checkbox input. Retries once via auto-heal on timeout. Returns True on success; raises ActionFailedError on failure."""
        try:
            if isinstance(locator, str):
                locator = self.page.locator(locator)
            locator.wait_for(state="visible", timeout=timeout)
            locator.uncheck()
            self.logger.info(f"Unchecked: {description}")
            self._record(f"Unchecked: {description}")
            return True
        except (PlaywrightTimeoutError, PlaywrightError) as e:
            self.logger.error(f"Uncheck failed for: {description} ({e})")
            shot = self.attach_screenshot(f"uncheck_failed_{description}")
            self._record(f"Uncheck failed for: {description}", "fail", shot)
            healed = self.auto_healer.locator(str(locator))
            if healed:
                self.logger.info(f"Auto-heal applied for: {description}")
                healed.uncheck()
                shot = self.attach_screenshot(f"after_autoheal_{description}")
                self._record(f"Auto-heal applied for: {description}", "info", shot)
                return True
            raise ActionFailedError(f"Uncheck failed for: {description}")

    def is_checked(self, locator, description: str = "Checkbox state", timeout: int = 30000) -> bool:
        """Returns True/False for the current checked state of a checkbox/radio. Returns False on error."""
        try:
            if isinstance(locator, str):
                locator = self.page.locator(locator)
            locator.wait_for(state="visible", timeout=timeout)
            state = locator.is_checked()
            self.logger.info(f"{description} checked state: {state}")
            self._record(f"{description} checked state: {state}")
            return state
        except Exception as e:
            self.logger.error(f"Could not read checked state for {description}: {e}")
            shot = self.attach_screenshot(f"is_checked_failed_{description}")
            self._record(f"Could not read checked state for {description}: {e}", "fail", shot)
            return False

    def select_radio_by_locator(self, locator, description: str = "Select radio option", timeout: int = 30000) -> bool:
        """Radio buttons use the same .check() API as checkboxes in Playwright -
        this is a distinctly-named alias so test code reads clearly."""
        return self.check_by_locator(locator, description=description, timeout=timeout)

    # ------------------------------------------------------------------ #
    # Dropdowns (multi-select, autocomplete)
    # ------------------------------------------------------------------ #
    def select_multiple_options(self, locator, values: list, description: str = "Select multiple options", timeout: int = 30000) -> bool:
        """Selects multiple options in a native multi-select <select> element. Returns True on success; raises ActionFailedError on failure."""
        try:
            if isinstance(locator, str):
                locator = self.page.locator(locator)
            locator.wait_for(state="visible", timeout=timeout)
            locator.select_option(values)
            self.logger.info(f"{description}: {values}")
            self._record(f"{description}: {values}")
            return True
        except Exception as e:
            self.logger.error(f"{description} failed: {e}")
            shot = self.attach_screenshot(f"multiselect_failed_{description}")
            self._record(f"{description} failed: {e}", "fail", shot)
            raise ActionFailedError(f"{description} failed: {e}")

    def select_autocomplete(self, input_locator, option_text: str, description: str = "Autocomplete selection", timeout: int = 30000) -> bool:
        """Types into a type-ahead input then clicks the suggestion matching option_text. Returns True on success; raises ActionFailedError on failure."""
        try:
            if isinstance(input_locator, str):
                input_locator = self.page.locator(input_locator)
            input_locator.wait_for(state="visible", timeout=timeout)
            input_locator.fill(option_text)
            option = self.page.get_by_text(option_text, exact=False)
            option.wait_for(state="visible", timeout=timeout)
            option.click()
            self.logger.info(f"{description}: selected '{option_text}'")
            self._record(f"{description}: selected '{option_text}'")
            return True
        except Exception as e:
            self.logger.error(f"{description} failed: {e}")
            shot = self.attach_screenshot(f"autocomplete_failed_{description}")
            self._record(f"{description} failed: {e}", "fail", shot)
            raise ActionFailedError(f"{description} failed: {e}")

    # ------------------------------------------------------------------ #
    # Calendar / Date picker
    # ------------------------------------------------------------------ #
    def select_date_native(self, locator, date_str: str, description: str = "Select date", timeout: int = 30000) -> bool:
        """date_str format: YYYY-MM-DD, for a native <input type="date">."""
        try:
            if isinstance(locator, str):
                locator = self.page.locator(locator)
            locator.wait_for(state="visible", timeout=timeout)
            locator.fill(date_str)
            self.logger.info(f"{description}: {date_str}")
            self._record(f"{description}: {date_str}")
            return True
        except Exception as e:
            self.logger.error(f"{description} failed: {e}")
            shot = self.attach_screenshot(f"date_native_failed_{description}")
            self._record(f"{description} failed: {e}", "fail", shot)
            raise ActionFailedError(f"{description} failed: {e}")

    def select_date_custom(self, day: str, month: str = None, year: str = None,
                            next_month_locator: str = None, header_locator: str = ".calendar-header",
                            description: str = "Select date from calendar", timeout: int = 30000) -> bool:
        """
        Generic custom-calendar-widget handler: clicks the 'next month' arrow
        until the header shows the target month/year (if given), then clicks
        the day cell matching `day`. Calendar markup varies a lot between
        apps - page objects may need to override for a specific widget's DOM.
        """
        try:
            if month and year and next_month_locator:
                target_label = f"{month} {year}"
                header = self.page.locator(header_locator).first
                max_clicks = 24
                clicks = 0
                while target_label not in (header.text_content() or "") and clicks < max_clicks:
                    self.page.locator(next_month_locator).click()
                    clicks += 1
            day_cell = self.page.get_by_text(str(day), exact=True)
            day_cell.wait_for(state="visible", timeout=timeout)
            day_cell.click()
            self.logger.info(f"{description}: day={day} month={month} year={year}")
            self._record(f"{description}: day={day} month={month} year={year}")
            return True
        except Exception as e:
            self.logger.error(f"{description} failed: {e}")
            shot = self.attach_screenshot(f"date_custom_failed_{description}")
            self._record(f"{description} failed: {e}", "fail", shot)
            raise ActionFailedError(f"{description} failed: {e}")

    def select_date_range(self, start_date: str, end_date: str, start_locator, end_locator,
                           description: str = "Select date range", timeout: int = 30000) -> bool:
        """For simple native from/to date inputs. For custom range-picker
        widgets, compose select_date_custom() twice from the page object instead."""
        try:
            ok1 = self.select_date_native(start_locator, start_date, description=f"{description} (start)", timeout=timeout)
            ok2 = self.select_date_native(end_locator, end_date, description=f"{description} (end)", timeout=timeout)
            return ok1 and ok2
        except Exception as e:
            self.logger.error(f"{description} failed: {e}")
            shot = self.attach_screenshot(f"date_range_failed_{description}")
            self._record(f"{description} failed: {e}", "fail", shot)
            raise ActionFailedError(f"{description} failed: {e}")

    # ------------------------------------------------------------------ #
    # File upload
    # ------------------------------------------------------------------ #
    def upload_file(self, locator, file_path: str, description: str = "Upload file", timeout: int = 30000) -> bool:
        """Sets file_path on a file input element. Returns True on success; raises ActionFailedError on failure."""
        try:
            if isinstance(locator, str):
                locator = self.page.locator(locator)
            locator.wait_for(state="attached", timeout=timeout)
            locator.set_input_files(file_path)
            self.logger.info(f"{description}: {file_path}")
            self._record(f"{description}: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"{description} failed: {e}")
            shot = self.attach_screenshot(f"upload_failed_{description}")
            self._record(f"{description} failed: {e}", "fail", shot)
            raise ActionFailedError(f"{description} failed: {e}")

    # ------------------------------------------------------------------ #
    # Dialogs / Alerts (native browser alert/confirm/prompt)
    # ------------------------------------------------------------------ #
    def accept_dialog(self, prompt_text: str = None) -> None:
        """Registers a ONE-TIME handler that accepts the next native dialog.
        Must be called BEFORE the action that triggers the dialog, since
        Playwright dialogs block the page until handled."""
        try:
            def _handler(dialog):
                self.logger.info(f"Accepting dialog: {dialog.message}")
                self._record(f"Accepted dialog: {dialog.message}")
                dialog.accept(prompt_text) if prompt_text else dialog.accept()
            self.page.once("dialog", _handler)
        except Exception as e:
            self.logger.error(f"Could not register accept_dialog handler: {e}")
            shot = self.attach_screenshot("accept_dialog_registration_failed")
            self._record(f"Could not register accept_dialog handler: {e}", "fail", shot)

    def dismiss_dialog(self) -> None:
        """Registers a ONE-TIME handler that dismisses the next native dialog.
        Must be called BEFORE the action that triggers the dialog."""
        try:
            def _handler(dialog):
                self.logger.info(f"Dismissing dialog: {dialog.message}")
                self._record(f"Dismissed dialog: {dialog.message}")
                dialog.dismiss()
            self.page.once("dialog", _handler)
        except Exception as e:
            self.logger.error(f"Could not register dismiss_dialog handler: {e}")
            shot = self.attach_screenshot("dismiss_dialog_registration_failed")
            self._record(f"Could not register dismiss_dialog handler: {e}", "fail", shot)

    # ------------------------------------------------------------------ #
    # Tabs & Accordions
    # ------------------------------------------------------------------ #
    def click_tab(self, tab_name: str, description: str = None, timeout: int = 30000) -> bool:
        """Clicks a tab found by ARIA role="tab" + name. Returns True on success; raises ActionFailedError on failure."""
        description = description or f"Tab '{tab_name}'"
        try:
            tab = self.page.get_by_role("tab", name=tab_name)
            tab.wait_for(state="visible", timeout=timeout)
            tab.click()
            self.logger.info(f"Clicked tab: {tab_name}")
            self._record(f"Clicked tab: {tab_name}")
            return True
        except Exception as e:
            self.logger.error(f"Click tab failed for: {tab_name} | {e}")
            shot = self.attach_screenshot(f"tab_failed_{tab_name}")
            self._record(f"Click tab failed for: {tab_name} | {e}", "fail", shot)
            raise ActionFailedError(f"Click tab failed for: {tab_name} | {e}")

    def expand_accordion(self, section_name: str, timeout: int = 30000) -> bool:
        """Clicks an accordion section header (found by visible text) to expand it. Returns True on success; raises ActionFailedError on failure."""
        try:
            header = self.page.get_by_text(section_name, exact=False)
            header.wait_for(state="visible", timeout=timeout)
            header.click()
            self.logger.info(f"Expanded accordion section: {section_name}")
            self._record(f"Expanded accordion section: {section_name}")
            return True
        except Exception as e:
            self.logger.error(f"Expand accordion failed for: {section_name} | {e}")
            shot = self.attach_screenshot(f"accordion_failed_{section_name}")
            self._record(f"Expand accordion failed for: {section_name} | {e}", "fail", shot)
            raise ActionFailedError(f"Expand accordion failed for: {section_name} | {e}")

    def collapse_accordion(self, section_name: str, timeout: int = 30000) -> bool:
        """Most accordions toggle open/closed on the same header click."""
        return self.expand_accordion(section_name, timeout=timeout)

    # ------------------------------------------------------------------ #
    # Tables
    # ------------------------------------------------------------------ #
    def get_table_row_by_text(self, table_locator, text: str, description: str = "Find table row", timeout: int = 30000):
        """Finds the first <tr> within table_locator containing text. Returns the row Locator, or None if not found."""
        try:
            if isinstance(table_locator, str):
                table_locator = self.page.locator(table_locator)
            row = table_locator.locator("tr", has_text=text)
            row.first.wait_for(state="visible", timeout=timeout)
            self.logger.info(f"{description}: found row containing '{text}'")
            self._record(f"{description}: found row containing '{text}'")
            return row.first
        except Exception as e:
            self.logger.error(f"{description} failed: {e}")
            shot = self.attach_screenshot(f"table_row_failed_{description}")
            self._record(f"{description} failed: {e}", "fail", shot)
            return None

    def get_cell_value(self, table_locator, row_index: int, col_index: int, description: str = "Get cell value", timeout: int = 30000) -> str:
        """Reads the text of a specific table cell by zero-based row/col index. Returns "" on failure."""
        try:
            if isinstance(table_locator, str):
                table_locator = self.page.locator(table_locator)
            table_locator.wait_for(state="visible", timeout=timeout)
            cell = table_locator.locator("tr").nth(row_index).locator("td").nth(col_index)
            text = cell.text_content()
            self.logger.info(f"{description} [{row_index}][{col_index}]: {text}")
            self._record(f"{description} [{row_index}][{col_index}]: {text}")
            return text or ""
        except Exception as e:
            self.logger.error(f"{description} failed: {e}")
            shot = self.attach_screenshot(f"cell_value_failed_{description}")
            self._record(f"{description} failed: {e}", "fail", shot)
            return ""

    def get_row_count(self, table_locator, description: str = "Get row count", timeout: int = 30000) -> int:
        """Returns the number of <tr> rows in a table. Returns 0 on failure."""
        try:
            if isinstance(table_locator, str):
                table_locator = self.page.locator(table_locator)
            table_locator.wait_for(state="visible", timeout=timeout)
            count = table_locator.locator("tr").count()
            self.logger.info(f"{description}: {count}")
            self._record(f"{description}: {count}")
            return count
        except Exception as e:
            self.logger.error(f"{description} failed: {e}")
            shot = self.attach_screenshot(f"row_count_failed_{description}")
            self._record(f"{description} failed: {e}", "fail", shot)
            return 0

    # ------------------------------------------------------------------ #
    # Modals / Iframes / New tabs
    # ------------------------------------------------------------------ #
    def wait_for_modal(self, locator, description: str = "Modal", timeout: int = 30000) -> bool:
        """Waits for a modal/dialog element to become visible. Returns True on success; raises ActionFailedError on failure."""
        try:
            if isinstance(locator, str):
                locator = self.page.locator(locator)
            locator.wait_for(state="visible", timeout=timeout)
            self.logger.info(f"{description} appeared")
            self._record(f"{description} appeared")
            return True
        except (PlaywrightTimeoutError, PlaywrightError) as e:
            self.logger.error(f"{description} did not appear within {timeout}ms ({e})")
            shot = self.attach_screenshot(f"modal_wait_failed_{description}")
            self._record(f"{description} did not appear within {timeout}ms", "fail", shot)
            raise ActionFailedError(f"{description} did not appear within {timeout}ms")

    def close_modal(self, close_button_locator, description: str = "Close modal", timeout: int = 30000) -> bool:
        """Clicks a modal's close button (thin wrapper over click_by_locator). Returns True on success; raises ActionFailedError on failure."""
        return self.click_by_locator(close_button_locator, description=description, timeout=timeout)

    def switch_to_frame(self, frame_locator: str):
        """Returns a Playwright FrameLocator for chaining .locator() calls
        inside an iframe. No wait applies here - FrameLocator construction is
        synchronous and lazy; the actual wait happens on whatever action is
        chained onto it next (e.g. switch_to_frame(...).locator(...).click())."""
        try:
            self.logger.info(f"Switched to frame: {frame_locator}")
            self._record(f"Switched to frame: {frame_locator}")
            return self.page.frame_locator(frame_locator)
        except Exception as e:
            self.logger.error(f"Could not switch to frame '{frame_locator}': {e}")
            shot = self.attach_screenshot(f"switch_frame_failed_{frame_locator}")
            self._record(f"Could not switch to frame '{frame_locator}': {e}", "fail", shot)
            return None

    def switch_to_new_tab(self, trigger_locator=None, description: str = "Switch to new tab", timeout: int = 30000):
        """Waits for a new tab/popup (optionally triggered by clicking
        trigger_locator first) and returns the new Page object."""
        try:
            with self.page.context.expect_page(timeout=timeout) as new_page_info:
                if trigger_locator is not None:
                    if isinstance(trigger_locator, str):
                        trigger_locator = self.page.locator(trigger_locator)
                    trigger_locator.click()
            new_page = new_page_info.value
            new_page.wait_for_load_state()
            self.logger.info(f"{description}: new tab opened - {new_page.url}")
            self._record(f"{description}: new tab opened - {new_page.url}")
            return new_page
        except (PlaywrightTimeoutError, PlaywrightError) as e:
            self.logger.error(f"{description} failed - no new tab opened within {timeout}ms ({e})")
            shot = self.attach_screenshot(f"new_tab_failed_{description}")
            self._record(f"{description} failed - no new tab opened within {timeout}ms", "fail", shot)
            return None

    # ------------------------------------------------------------------ #
    # Scrolling / Keyboard / Mouse
    # ------------------------------------------------------------------ #
    def scroll_into_view(self, locator, description: str = "Scroll into view", timeout: int = 30000) -> bool:
        """Scrolls the page until the given element is in the viewport. Returns True on success; raises ActionFailedError on failure."""
        try:
            if isinstance(locator, str):
                locator = self.page.locator(locator)
            locator.scroll_into_view_if_needed(timeout=timeout)
            self.logger.info(description)
            self._record(description)
            return True
        except Exception as e:
            self.logger.error(f"{description} failed: {e}")
            shot = self.attach_screenshot(f"scroll_failed_{description}")
            self._record(f"{description} failed: {e}", "fail", shot)
            raise ActionFailedError(f"{description} failed: {e}")

    def scroll_to_top(self) -> None:
        """Scrolls the page to the very top via JS window.scrollTo."""
        try:
            self.page.evaluate("window.scrollTo(0, 0)")
            self.logger.info("Scrolled to top of page")
            self._record("Scrolled to top of page")
        except Exception as e:
            self.logger.error(f"Scroll to top failed: {e}")
            shot = self.attach_screenshot("scroll_to_top_failed")
            self._record(f"Scroll to top failed: {e}", "fail", shot)

    def scroll_to_bottom(self) -> None:
        """Scrolls the page to the very bottom via JS window.scrollTo."""
        try:
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            self.logger.info("Scrolled to bottom of page")
            self._record("Scrolled to bottom of page")
        except Exception as e:
            self.logger.error(f"Scroll to bottom failed: {e}")
            shot = self.attach_screenshot("scroll_to_bottom_failed")
            self._record(f"Scroll to bottom failed: {e}", "fail", shot)

    def press_key(self, key: str, description: str = None) -> bool:
        """Presses a single keyboard key (e.g. "Enter", "Escape", "Tab", "ArrowDown"). Returns True on success; raises ActionFailedError on failure."""
        description = description or f"Press key '{key}'"
        try:
            self.page.keyboard.press(key)
            self.logger.info(description)
            self._record(description)
            return True
        except Exception as e:
            self.logger.error(f"{description} failed: {e}")
            shot = self.attach_screenshot(f"keypress_failed_{key}")
            self._record(f"{description} failed: {e}", "fail", shot)
            raise ActionFailedError(f"{description} failed: {e}")

    def double_click_by_locator(self, locator, description: str = "Double-click action", timeout: int = 30000) -> bool:
        """Double-clicks an element. Retries once via auto-heal on timeout. Returns True on success; raises ActionFailedError on failure."""
        try:
            if isinstance(locator, str):
                locator = self.page.locator(locator)
            locator.wait_for(state="visible", timeout=timeout)
            locator.dblclick()
            self.logger.info(f"Double-clicked: {description}")
            self._record(f"Double-clicked: {description}")
            return True
        except (PlaywrightTimeoutError, PlaywrightError) as e:
            self.logger.error(f"Double-click failed for: {description} ({e})")
            shot = self.attach_screenshot(f"dblclick_failed_{description}")
            self._record(f"Double-click failed for: {description}", "fail", shot)
            healed = self.auto_healer.locator(str(locator))
            if healed:
                self.logger.info(f"Auto-heal applied for: {description}")
                healed.dblclick()
                shot = self.attach_screenshot(f"after_autoheal_{description}")
                self._record(f"Auto-heal applied for: {description}", "info", shot)
                return True
            raise ActionFailedError(f"Double-click failed for: {description}")

    def right_click_by_locator(self, locator, description: str = "Right-click action", timeout: int = 30000) -> bool:
        """Right-clicks an element (opens context menus). Retries once via auto-heal on timeout. Returns True on success; raises ActionFailedError on failure."""
        try:
            if isinstance(locator, str):
                locator = self.page.locator(locator)
            locator.wait_for(state="visible", timeout=timeout)
            locator.click(button="right")
            self.logger.info(f"Right-clicked: {description}")
            self._record(f"Right-clicked: {description}")
            return True
        except (PlaywrightTimeoutError, PlaywrightError) as e:
            self.logger.error(f"Right-click failed for: {description} ({e})")
            shot = self.attach_screenshot(f"rightclick_failed_{description}")
            self._record(f"Right-click failed for: {description}", "fail", shot)
            healed = self.auto_healer.locator(str(locator))
            if healed:
                self.logger.info(f"Auto-heal applied for: {description}")
                healed.click(button="right")
                shot = self.attach_screenshot(f"after_autoheal_{description}")
                self._record(f"Auto-heal applied for: {description}", "info", shot)
                return True
            raise ActionFailedError(f"Right-click failed for: {description}")

    def drag_and_drop(self, source_locator, target_locator, description: str = "Drag and drop", timeout: int = 30000) -> bool:
        """Drags source_locator onto target_locator. Returns True on success; raises ActionFailedError on failure."""
        try:
            if isinstance(source_locator, str):
                source_locator = self.page.locator(source_locator)
            if isinstance(target_locator, str):
                target_locator = self.page.locator(target_locator)
            source_locator.wait_for(state="visible", timeout=timeout)
            target_locator.wait_for(state="visible", timeout=timeout)
            source_locator.drag_to(target_locator)
            self.logger.info(f"{description}: dragged successfully")
            self._record(f"{description}: dragged successfully")
            return True
        except Exception as e:
            self.logger.error(f"{description} failed: {e}")
            shot = self.attach_screenshot(f"dragdrop_failed_{description}")
            self._record(f"{description} failed: {e}", "fail", shot)
            raise ActionFailedError(f"{description} failed: {e}")

    # ------------------------------------------------------------------ #
    # Loading spinners / Toasts
    # ------------------------------------------------------------------ #
    def wait_for_spinner_to_disappear(self, spinner_locator, description: str = "Loading spinner", timeout: int = 30000) -> bool:
        """Waits for a loading spinner/indicator element to become hidden. Returns True on success; raises ActionFailedError on failure."""
        try:
            if isinstance(spinner_locator, str):
                spinner_locator = self.page.locator(spinner_locator)
            spinner_locator.wait_for(state="hidden", timeout=timeout)
            self.logger.info(f"{description} disappeared")
            self._record(f"{description} disappeared")
            return True
        except (PlaywrightTimeoutError, PlaywrightError) as e:
            self.logger.error(f"{description} still visible after {timeout}ms ({e})")
            shot = self.attach_screenshot(f"spinner_failed_{description}")
            self._record(f"{description} still visible after {timeout}ms", "fail", shot)
            raise ActionFailedError(f"{description} still visible after {timeout}ms")

    def get_toast_message(self, toast_locator, description: str = "Toast message", timeout: int = 10000) -> str:
        """Waits for a toast/notification to appear and returns its text. Returns "" on timeout."""
        try:
            if isinstance(toast_locator, str):
                toast_locator = self.page.locator(toast_locator)
            toast_locator.wait_for(state="visible", timeout=timeout)
            text = toast_locator.text_content()
            self.logger.info(f"{description}: {text}")
            self._record(f"{description}: {text}")
            return text or ""
        except (PlaywrightTimeoutError, PlaywrightError) as e:
            self.logger.error(f"{description} did not appear within {timeout}ms ({e})")
            shot = self.attach_screenshot(f"toast_failed_{description}")
            self._record(f"{description} did not appear within {timeout}ms", "fail", shot)
            return ""

    def wait_for_toast_to_disappear(self, toast_locator, description: str = "Toast message", timeout: int = 15000) -> bool:
        """Waits for a toast/notification element to become hidden. Returns True on success; raises ActionFailedError on failure."""
        try:
            if isinstance(toast_locator, str):
                toast_locator = self.page.locator(toast_locator)
            toast_locator.wait_for(state="hidden", timeout=timeout)
            self.logger.info(f"{description} disappeared")
            self._record(f"{description} disappeared")
            return True
        except (PlaywrightTimeoutError, PlaywrightError) as e:
            self.logger.error(f"{description} still visible after {timeout}ms ({e})")
            shot = self.attach_screenshot(f"toast_disappear_failed_{description}")
            self._record(f"{description} still visible after {timeout}ms", "fail", shot)
            raise ActionFailedError(f"{description} still visible after {timeout}ms")

    # ------------------------------------------------------------------ #
    # Browser navigation (back / forward / refresh)
    # ------------------------------------------------------------------ #
    def go_back(self, description: str = "Go back", timeout: int = 30000) -> bool:
        """Navigates to the previous page in browser history. Returns True on success; raises ActionFailedError on failure."""
        try:
            self.page.go_back(timeout=timeout)
            self.logger.info(f"{description}: navigated back")
            self._record(f"{description}: navigated back")
            return True
        except Exception as e:
            self.logger.error(f"{description} failed: {e}")
            shot = self.attach_screenshot(f"go_back_failed_{description}")
            self._record(f"{description} failed: {e}", "fail", shot)
            raise ActionFailedError(f"{description} failed: {e}")

    def go_forward(self, description: str = "Go forward", timeout: int = 30000) -> bool:
        """Navigates forward in browser history (undoes a previous go_back). Returns True on success; raises ActionFailedError on failure."""
        try:
            self.page.go_forward(timeout=timeout)
            self.logger.info(f"{description}: navigated forward")
            self._record(f"{description}: navigated forward")
            return True
        except Exception as e:
            self.logger.error(f"{description} failed: {e}")
            shot = self.attach_screenshot(f"go_forward_failed_{description}")
            self._record(f"{description} failed: {e}", "fail", shot)
            raise ActionFailedError(f"{description} failed: {e}")

    def refresh_page(self, description: str = "Refresh page", timeout: int = 30000) -> bool:
        """Reloads the current page. Returns True on success; raises ActionFailedError on failure."""
        try:
            self.page.reload(timeout=timeout)
            self.logger.info(f"{description}: page reloaded")
            self._record(f"{description}: page reloaded")
            return True
        except Exception as e:
            self.logger.error(f"{description} failed: {e}")
            shot = self.attach_screenshot(f"refresh_failed_{description}")
            self._record(f"{description} failed: {e}", "fail", shot)
            raise ActionFailedError(f"{description} failed: {e}")

    # ------------------------------------------------------------------ #
    # File download
    # ------------------------------------------------------------------ #
    def download_file(self, trigger_locator, save_dir: str = None, description: str = "Download file", timeout: int = 30000) -> str:
        """Clicks trigger_locator, waits for the resulting browser download, saves
        it (to save_dir if given, else Playwright's default temp location), and
        returns the saved file path as a string ("" on failure)."""
        try:
            if isinstance(trigger_locator, str):
                trigger_locator = self.page.locator(trigger_locator)
            with self.page.expect_download(timeout=timeout) as download_info:
                trigger_locator.click()
            download = download_info.value
            if save_dir:
                save_path = str(Path(save_dir) / download.suggested_filename)
                download.save_as(save_path)
            else:
                save_path = download.path()
            self.logger.info(f"{description}: saved to {save_path}")
            self._record(f"{description}: saved to {save_path}")
            return str(save_path)
        except Exception as e:
            self.logger.error(f"{description} failed: {e}")
            shot = self.attach_screenshot(f"download_failed_{description}")
            self._record(f"{description} failed: {e}", "fail", shot)
            return ""

    # ------------------------------------------------------------------ #
    # Generic attribute / state readers
    # ------------------------------------------------------------------ #
    def get_attribute(self, locator, attribute_name: str, description: str = "Get attribute", timeout: int = 30000) -> str:
        """Reads any HTML attribute (href, value, data-*, class, etc.) from an
        element. Returns the attribute value as a string, or "" if missing/failed."""
        try:
            if isinstance(locator, str):
                locator = self.page.locator(locator)
            locator.wait_for(state="visible", timeout=timeout)
            value = locator.get_attribute(attribute_name)
            self.logger.info(f"{description} [{attribute_name}]: {value}")
            self._record(f"{description} [{attribute_name}]: {value}")
            return value or ""
        except Exception as e:
            self.logger.error(f"{description} failed: {e}")
            shot = self.attach_screenshot(f"get_attribute_failed_{description}")
            self._record(f"{description} failed: {e}", "fail", shot)
            return ""

    def is_enabled(self, locator, description: str = "Enabled state check", timeout: int = 30000) -> bool:
        """Returns True if the element is enabled (not disabled), False on
        disabled state or any error - useful for checking a button stays
        disabled during validation/loading."""
        try:
            if isinstance(locator, str):
                locator = self.page.locator(locator)
            locator.wait_for(state="visible", timeout=timeout)
            state = locator.is_enabled()
            self.logger.info(f"{description}: {state}")
            self._record(f"{description}: {state}")
            return state
        except Exception as e:
            self.logger.error(f"{description} failed: {e}")
            shot = self.attach_screenshot(f"is_enabled_failed_{description}")
            self._record(f"{description} failed: {e}", "fail", shot)
            return False

    def get_element_count(self, locator, description: str = "Get element count") -> int:
        """Returns how many elements match the given locator (e.g. list items,
        validation error messages) - a generic version of get_row_count for
        non-table cases. Returns 0 on failure."""
        try:
            if isinstance(locator, str):
                locator = self.page.locator(locator)
            count = locator.count()
            self.logger.info(f"{description}: {count}")
            self._record(f"{description}: {count}")
            return count
        except Exception as e:
            self.logger.error(f"{description} failed: {e}")
            shot = self.attach_screenshot(f"element_count_failed_{description}")
            self._record(f"{description} failed: {e}", "fail", shot)
            return 0

    def get_all_text(self, locator, description: str = "Get all text") -> list:
        """Returns the text content of EVERY element matching the given locator
        as a list, e.g. reading all validation errors or all menu labels at
        once. Returns an empty list on failure."""
        try:
            if isinstance(locator, str):
                locator = self.page.locator(locator)
            texts = locator.all_text_contents()
            self.logger.info(f"{description}: {texts}")
            self._record(f"{description}: {texts}")
            return texts
        except Exception as e:
            self.logger.error(f"{description} failed: {e}")
            shot = self.attach_screenshot(f"get_all_text_failed_{description}")
            self._record(f"{description} failed: {e}", "fail", shot)
            return []

    def wait_for_url(self, url_pattern: str, description: str = "Wait for URL", timeout: int = 30000) -> bool:
        """Waits until the page URL matches url_pattern (substring, glob, or
        regex per Playwright's wait_for_url) - useful for confirming a redirect
        after login/payment completes. Returns True on success; raises ActionFailedError on failure."""
        try:
            self.page.wait_for_url(url_pattern, timeout=timeout)
            self.logger.info(f"{description}: URL matched '{url_pattern}'")
            self._record(f"{description}: URL matched '{url_pattern}'")
            return True
        except (PlaywrightTimeoutError, PlaywrightError) as e:
            self.logger.error(f"{description}: URL did not match '{url_pattern}' within {timeout}ms ({e})")
            shot = self.attach_screenshot(f"wait_for_url_failed_{description}")
            self._record(f"{description}: URL did not match '{url_pattern}' within {timeout}ms", "fail", shot)
            raise ActionFailedError(f"{description}: URL did not match '{url_pattern}' within {timeout}ms")

    def clear_field(self, locator, description: str = "Clear field", timeout: int = 30000) -> bool:
        """Clears a text input's current value without typing anything new
        afterwards. Returns True on success; raises ActionFailedError on failure."""
        try:
            if isinstance(locator, str):
                locator = self.page.locator(locator)
            locator.wait_for(state="visible", timeout=timeout)
            locator.clear()
            self.logger.info(f"{description}: cleared")
            self._record(f"{description}: cleared")
            return True
        except Exception as e:
            self.logger.error(f"{description} failed: {e}")
            shot = self.attach_screenshot(f"clear_failed_{description}")
            self._record(f"{description} failed: {e}", "fail", shot)
            raise ActionFailedError(f"{description} failed: {e}")

    # ------------------------------------------------------------------ #
    # MFA / TOTP entry - for banks whose login flow requires a
    # time-based one-time-password from an authenticator app secret.
    # ------------------------------------------------------------------ #
    def enter_authenticator(self, secret_key: str, otp_locator: str = "#otpvalue", timeout: int = 30000) -> bool:
        """
        Generates a TOTP code from the given authenticator secret and fills
        it into the OTP field. otp_locator defaults to '#otpvalue' but should
        be passed in from the bank's own locator class (e.g. loc.otp_field)
        since the real selector differs per bank/portal. Returns False (does
        NOT raise) if secret_key is empty, since that's a deliberate "this
        bank has no MFA configured" case, not a failure. Raises
        ActionFailedError if a secret_key IS provided but TOTP generation or
        filling the OTP field fails.
        """
        try:
            secret_key = secret_key.strip() if secret_key else ""
            if not secret_key:
                self.logger.warning("Empty TOTP secret key provided, skipping TOTP entry")
                return False

            totp = pyotp.TOTP(secret_key)
            otp_code = totp.now()

            otp_field = self.page.locator(otp_locator) if isinstance(otp_locator, str) else otp_locator
            otp_field.wait_for(state="visible", timeout=timeout)
            otp_field.fill(otp_code)

            self.logger.info(f"Entered TOTP code: {otp_code}")
            self._record(f"Entered TOTP code: {otp_code}")
            shot = self.attach_screenshot("After entering TOTP code")
            self._record("After entering TOTP code", "info", shot)
            return True
        except Exception as e:
            self.logger.error(f"Failed to generate TOTP code from secret '{secret_key}': {e}")
            shot = self.attach_screenshot("TOTP entry failed")
            self._record(f"Failed to generate TOTP code: {e}", "fail", shot)
            raise ActionFailedError(f"Failed to generate TOTP code: {e}")

    # ------------------------------------------------------------------ #
    # CAPTCHA reading (OCR) - for QA/test-environment CAPTCHAs ONLY.
    # This reads a deliberately OCR-readable distorted-text/digit image, the
    # kind test/staging environments commonly use so login flows stay
    # automatable. It does NOT and cannot defeat a real anti-bot CAPTCHA
    # (reCAPTCHA/hCaptcha) - those are specifically designed to block this.
    # ------------------------------------------------------------------ #
    def read_captcha_via_ocr(self, locator, save_path: str = None,
                              description: str = "Read CAPTCHA", timeout: int = 30000) -> str:
        """
        Screenshots a CAPTCHA image element, preprocesses it (grayscale,
        upscale, threshold) to improve OCR accuracy, then runs Tesseract OCR
        to extract the text/digits. Requires the pytesseract package AND the
        Tesseract OCR engine installed on the machine (a system package, not
        just pip - e.g. `apt install tesseract-ocr` on Linux, or the Windows
        installer from the Tesseract project). Returns the extracted text
        (whitespace-stripped), or "" on failure.

        NOTE: OCR is not 100% accurate even on clean test CAPTCHAs - pair
        this with attempt_login_with_captcha_retry() below if your CAPTCHA
        occasionally misreads.
        """
        try:
            import pytesseract
            from PIL import Image

            if isinstance(locator, str):
                locator = self.page.locator(locator)
            locator.wait_for(state="visible", timeout=timeout)

            path = save_path or str(self.screenshot_dir / f"captcha_{self.screenshot_count:03d}.png")
            locator.screenshot(path=path)

            img = Image.open(path).convert("L")
            img = img.resize((img.width * 3, img.height * 3), Image.LANCZOS)
            img = img.point(lambda p: 255 if p > 140 else 0)

            captcha_text = pytesseract.image_to_string(
                img, config="--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
            ).strip()

            self.logger.info(f"{description}: extracted '{captcha_text}'")
            self._record(f"{description}: extracted '{captcha_text}'")
            return captcha_text
        except ImportError:
            self.logger.error(f"{description} failed: pytesseract not installed (pip install pytesseract, plus the Tesseract OCR engine on the system)")
            self._record(f"{description} failed: pytesseract not installed", "fail")
            return ""
        except Exception as e:
            self.logger.error(f"{description} failed: {e}")
            shot = self.attach_screenshot(f"captcha_ocr_failed_{description}")
            self._record(f"{description} failed: {e}", "fail", shot)
            return ""

    def attempt_login_with_captcha_retry(self, login_fn, captcha_locator,
                                          success_check_fn, max_attempts: int = 5,
                                          description: str = "Login with CAPTCHA retry") -> bool:
        """
        Retries a login flow when OCR misreads the CAPTCHA - since OCR is not
        100% reliable even on clean test CAPTCHAs, this re-reads a fresh
        CAPTCHA and retries login up to max_attempts times.

        login_fn: callable(captcha_text: str) -> None - performs one full
            login attempt using the given captcha text (fill fields, click submit).
        captcha_locator: locator/selector for the CAPTCHA image, re-read fresh
            each attempt (most apps generate a new CAPTCHA on each page load/attempt).
        success_check_fn: callable() -> bool - returns True if login succeeded
            (e.g. dashboard visible), called after each attempt.
        Returns True if any attempt succeeded, False if all max_attempts failed.
        """
        for attempt in range(1, max_attempts + 1):
            try:
                captcha_text = self.read_captcha_via_ocr(
                    captcha_locator, description=f"{description} - attempt {attempt} CAPTCHA read"
                )
                login_fn(captcha_text)
                if success_check_fn():
                    self.logger.info(f"{description}: succeeded on attempt {attempt}")
                    self._record(f"{description}: succeeded on attempt {attempt}", "pass")
                    return True
            except Exception as e:
                self.logger.error(f"{description}: attempt {attempt} raised an error: {e}")
                self._record(f"{description}: attempt {attempt} raised an error: {e}", "fail")
            self.logger.info(f"{description}: attempt {attempt} failed, retrying" if attempt < max_attempts else f"{description}: attempt {attempt} failed, no attempts left")
        shot = self.attach_screenshot(f"captcha_retry_exhausted_{description}")
        self._record(f"{description}: all {max_attempts} attempts failed", "fail", shot)
        raise ActionFailedError(f"{description}: all {max_attempts} attempts failed")

    # ------------------------------------------------------------------ #
    # OTP entry (common banking pattern - split single-digit input boxes)
    # ------------------------------------------------------------------ #
    def enter_otp(self, otp_value: str, box_locators: list, description: str = "Enter OTP") -> bool:
        """
        Fills a one-time-password/PIN split across multiple single-digit input
        boxes - a very common banking UI pattern. box_locators is an ordered
        list of locators/selectors, one per digit box, matched to otp_value's
        digits in the same order (len(box_locators) must equal len(otp_value)).
        Returns True on success; raises ActionFailedError on failure.
        """
        try:
            if len(box_locators) != len(otp_value):
                raise ValueError(
                    f"box_locators has {len(box_locators)} boxes but otp_value has {len(otp_value)} digits"
                )
            for digit, box in zip(otp_value, box_locators):
                box_loc = self.page.locator(box) if isinstance(box, str) else box
                box_loc.wait_for(state="visible", timeout=10000)
                box_loc.fill(digit)
            self.logger.info(f"{description}: entered {len(otp_value)}-digit OTP")
            self._record(f"{description}: entered {len(otp_value)}-digit OTP")
            return True
        except Exception as e:
            self.logger.error(f"{description} failed: {e}")
            shot = self.attach_screenshot(f"otp_failed_{description}")
            self._record(f"{description} failed: {e}", "fail", shot)
            raise ActionFailedError(f"{description} failed: {e}")

    # ------------------------------------------------------------------ #
    # Pagination & table sorting
    # ------------------------------------------------------------------ #
    def click_next_page(self, next_button_locator: str = "button[aria-label='Next']", description: str = "Next page", timeout: int = 30000) -> bool:
        """Clicks the 'next page' control on a paginated table/list. Returns True on success; raises ActionFailedError on failure."""
        return self.click_by_locator(next_button_locator, description=description, timeout=timeout)

    def click_previous_page(self, prev_button_locator: str = "button[aria-label='Previous']", description: str = "Previous page", timeout: int = 30000) -> bool:
        """Clicks the 'previous page' control on a paginated table/list. Returns True on success; raises ActionFailedError on failure."""
        return self.click_by_locator(prev_button_locator, description=description, timeout=timeout)

    def go_to_page(self, page_number: int, description: str = None, timeout: int = 30000) -> bool:
        """Clicks a specific numbered page control (e.g. page '3' in pagination). Returns True on success; raises ActionFailedError on failure."""
        description = description or f"Go to page {page_number}"
        try:
            page_link = self.page.get_by_text(str(page_number), exact=True)
            page_link.wait_for(state="visible", timeout=timeout)
            page_link.click()
            self.logger.info(description)
            self._record(description)
            return True
        except Exception as e:
            self.logger.error(f"{description} failed: {e}")
            shot = self.attach_screenshot(f"go_to_page_failed_{page_number}")
            self._record(f"{description} failed: {e}", "fail", shot)
            raise ActionFailedError(f"{description} failed: {e}")

    def sort_table_by_column(self, column_header_text: str, description: str = None, timeout: int = 30000) -> bool:
        """Clicks a table's column header to trigger sorting - most data grids
        sort ascending/descending on header click. Returns True on success; raises ActionFailedError on failure."""
        description = description or f"Sort by column '{column_header_text}'"
        try:
            header = self.page.get_by_role("columnheader", name=column_header_text)
            header.wait_for(state="visible", timeout=timeout)
            header.click()
            self.logger.info(description)
            self._record(description)
            return True
        except Exception as e:
            self.logger.error(f"{description} failed: {e}")
            shot = self.attach_screenshot(f"sort_failed_{column_header_text}")
            self._record(f"{description} failed: {e}", "fail", shot)
            raise ActionFailedError(f"{description} failed: {e}")

    # ------------------------------------------------------------------ #
    # Locator helpers
    # ------------------------------------------------------------------ #
    def locator(self, selector: str):
        """Wraps a CSS selector string in a Playwright Locator, for use with any *_by_locator method."""
        return self.page.locator(selector)

    def get_by_role(self, role: str, name: str = None, exact: bool = False):
        """Returns a Locator resolved by ARIA role + accessible name."""
        return self.page.get_by_role(role, name=name, exact=exact)

    def get_by_text(self, text: str, exact: bool = False):
        """Returns a Locator resolved by visible text content."""
        return self.page.get_by_text(text, exact=exact)

    def get_by_label(self, label: str, exact: bool = False):
        """Returns a Locator resolved by an associated <label> element's text."""
        return self.page.get_by_label(label, exact=exact)

    def get_by_placeholder(self, placeholder: str, exact: bool = False):
        """Returns a Locator resolved by an input's placeholder text."""
        return self.page.get_by_placeholder(placeholder, exact=exact)

    def get_by_test_id(self, test_id: str):
        """Returns a Locator resolved by a data-testid attribute - the most refactor-resistant strategy when the app supports it."""
        return self.page.get_by_test_id(test_id)

    def locator_by_xpath(self, xpath: str):
        """Returns a Locator resolved by an XPath expression."""
        return self.page.locator(f"xpath={xpath}")
    
    def select_custom_dropdown(self, dropdown_locator: str, value: str) -> None:
        try:
            self.page.locator(dropdown_locator).click()
 
            option = self.page.get_by_text(value, exact=True)
            option.wait_for(state="visible", timeout=10000)
            option.click()
 
            self.logger.info(f"Selected '{value}' from dropdown '{dropdown_locator}'")
            self._record(f"Selected '{value}' from dropdown '{dropdown_locator}'")
 
        except Exception as e:
            self.logger.error(f"Dropdown selection failed: {e}")
            shot = self.attach_screenshot(f"dropdown_failed")
            self._record(f"Dropdown selection failed: {e}", "error", shot)
            raise
 
 
    def wait_for_field_populated(self,locator,expected_value: Optional[str] = None,description: str = "Wait for field to be populated",timeout: int = 30000,) -> bool:
        """Waits until an input field has a value (auto-population done).
        If expected_value is provided, waits for that exact value.
        Returns True once the condition is met; raises ActionFailedError on timeout.
        """
        try:
            if isinstance(locator, str):
                locator = self.page.locator(locator)
            if expected_value is None:
                expect(locator).not_to_have_value("", timeout=timeout)
            else:
                expect(locator).to_have_value(expected_value, timeout=timeout)
            self.logger.info(f"{description}: populated")
            self._record(f"{description}: populated")
            return True
        except PlaywrightTimeoutError as e:
            self.logger.error(f"{description}: timeout waiting for value ({e})")
            shot = self.attach_screenshot(f"wait_populate_failed_{description}")
            self._record(f"{description}: timeout", "fail", shot)
            raise ActionFailedError(f"{description}: timeout waiting for value")
 
       
 
    def multi_select(self, dropdown_id: str, value: str, description: str = "") -> None:
        try:
            values = [v.strip() for v in value.split(",")] if "," in value else [value]
 
        # Open dropdown once
            self.page.locator(dropdown_id).click()
 
            for v in values:
                option = self.page.get_by_text(v, exact=True)
                option.wait_for(state="visible", timeout=10000)
                option.click()
 
        # Close dropdown
            self.page.keyboard.press("Escape")
 
            log_value = value if value else ", ".join(values)
            desc = description or f"Multi select in dropdown '{dropdown_id}'"
            self.logger.info(f"{desc}: {log_value}")
            self._record(f"{desc}: {log_value}")
 
        except Exception as e:
            self.logger.error(f"Multi select failed: {e}")
            shot = self.attach_screenshot("multiselect_failed")
            self._record(f"Multi select failed: {e}", "error", shot)
            raise