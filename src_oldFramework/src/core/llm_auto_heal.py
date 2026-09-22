# llm_auto_heal.py
import os
import json
import time
from openai import OpenAI
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

class LocatorAutoHeal:
    
    

    def __init__(self, page: Page, timeout=3000, model="gpt-4.1-mini"):
        self.page = page
        self.timeout = timeout
        self.model = model

        # Check if API key is set
        if not self.OPENAI_API_KEY:
            raise Exception("OPENAI_API_KEY is not set. Please set it at class level or via environment variable.")

        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.OPENAI_API_KEY)
        
        
        # Declare OpenAI API KEY HERE - Using environment variable for security
        #self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        # If user did not set it, throw user-friendly error
        #if not os.getenv("OPENAI_API_KEY"):
            #raise Exception(" OPENAI_API_KEY is not set. Please set environment variable.")
         
    # Declare Merlin Forge AI API KEY HERE
        #self.client = OpenAI(api_key=os.getenv("MERLIN_FORGE_API_KEY"))
        #if not os.getenv("MERLIN_FORGE_API_KEY"):
            #raise Exception("MERLIN_FORGE_API_KEY is not set. Please set environment variable.")

    # ---------------------------
    # Generic locator
    # ---------------------------
    def locator(self, selector: str):
        return self._heal_wrapper("locator", selector)

    # ---------------------------
    # Role-based locator
    # ---------------------------
    def get_by_role(self, role: str, name: str = None, exact: bool = False):
        return self._heal_wrapper("get_by_role", role, name=name, exact=exact)

    # ---------------------------
    # Text-based locator
    # ---------------------------
    def get_by_text(self, text: str, exact: bool = False):
        return self._heal_wrapper("get_by_text", text, exact=exact)

    # ---------------------------
    # Label-based locator
    # ---------------------------
    def get_by_label(self, label: str, exact: bool = False):
        return self._heal_wrapper("get_by_label", label, exact=exact)

    # ---------------------------
    # Placeholder-based locator
    # ---------------------------
    def get_by_placeholder(self, placeholder: str, exact: bool = False):
        return self._heal_wrapper("get_by_placeholder", placeholder, exact=exact)

    # ---------------------------
    # Test ID locator
    # ---------------------------
    def get_by_test_id(self, test_id: str):
        return self._heal_wrapper("get_by_test_id", test_id)

    # ---------------------------
    # XPath locator
    # ---------------------------
    def locator_by_xpath(self, xpath: str):
        return self._heal_wrapper("xpath", xpath)

    # ---------------------------
    # Core wrapper for healing
    # ---------------------------
    def _heal_wrapper(self, strategy: str, value: str, **kwargs):
        print(f"[AutoHeal] Trying {strategy}('{value}')")

        try:
            if strategy == "locator":
                loc = self.page.locator(value)
            elif strategy == "get_by_role":
                loc = self.page.get_by_role(value, **kwargs)
            elif strategy == "get_by_text":
                loc = self.page.get_by_text(value, **kwargs)
            elif strategy == "get_by_label":
                loc = self.page.get_by_label(value, **kwargs)
            elif strategy == "get_by_placeholder":
                loc = self.page.get_by_placeholder(value, **kwargs)
            elif strategy == "get_by_test_id":
                loc = self.page.get_by_test_id(value)
            elif strategy == "xpath":
                loc = self.page.locator(f"xpath={value}")
            else:
                raise ValueError(f"Unsupported locator strategy: {strategy}")

            loc.wait_for(state="visible", timeout=self.timeout)
            return loc

        except PlaywrightTimeoutError:
            print(f"[AutoHeal] {strategy} failed for: {value}")
            healed_selector = self._run_auto_heal(strategy, value)
            if healed_selector:
                print(f"[AutoHeal] Using healed locator: {healed_selector}")
                return self.page.locator(healed_selector)
            print("[AutoHeal] Auto-heal failed. Returning original locator.")
            return loc

    # ---------------------------
    # Auto-heal core function
    # ---------------------------
    def _run_auto_heal(self, strategy: str, bad_selector: str):
        dom = self.page.content()
        screenshot = f"autoheal_{int(time.time())}.png"
        self.page.screenshot(path=screenshot)
        print(f"[AutoHeal] Screenshot captured: {screenshot}")

        prompt = f"""
        You are an expert Playwright QA engineer.
        The locator strategy '{strategy}' failed.

        Broken selector: {bad_selector}

        DOM snapshot:
        {dom[:15000]}

        Task:
        - Suggest the MOST LIKELY correct locator.
        - Return ONLY JSON. Example:
          {{"locator": "role=button[name='Login']"}}
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
            )

            print("[AutoHeal] LLM Response:", response.choices[0].message.content)
            result = json.loads(response.choices[0].message.content)
            healed = result.get("locator")

            if not healed:
                return None

            try:
                test_loc = self.page.locator(healed)
                test_loc.wait_for(timeout=self.timeout)
                return healed
            except PlaywrightTimeoutError:
                print(f"[AutoHeal] LLM suggested invalid locator: {healed}")
                return None

        except Exception as e:
            print(f"[AutoHeal] LLM Error: {e}")
            return None