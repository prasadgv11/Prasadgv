"""
Core pytest fixtures: browser, context, page. Page objects are now built
directly inside each test (LoginPage(page), PaymentsPage(page)) rather than
handed out as fixtures, matching the real convention.
"""
import pytest
from playwright.sync_api import sync_playwright

from src.common.utilities.config_loader import ConfigManager


@pytest.fixture(scope="session")
def run_config():
    return ConfigManager.load_bank_config()


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance, run_config):
    browser_type = getattr(playwright_instance, run_config["browser"])
    browser_obj = browser_type.launch(headless=run_config["headless"])
    yield browser_obj
    browser_obj.close()


@pytest.fixture
def context(browser):
    ctx = browser.new_context()
    yield ctx
    ctx.close()


@pytest.fixture
def page(context):
    pg = context.new_page()
    yield pg
    pg.close()
