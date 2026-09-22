import pytest
import os
import re
from datetime import datetime
import allure
from playwright.sync_api import sync_playwright

# CLI option to pass sheet name
def pytest_addoption(parser):
    parser.addoption("--sheet", action="store", default="Login_Positive",
                     help="Excel sheet name to run")

@pytest.fixture
def sheet_name(request):
    return request.config.getoption("--sheet")

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()

    page = context.new_page()

    page.set_default_timeout(10000)
    page.set_default_navigation_timeout(15000)

    yield page

    try:
        allure.attach(
            page.screenshot(full_page=True),
            name="Final page state",
            attachment_type=allure.attachment_type.PNG
        )
    except Exception:
        pass

    context.close()

def _next_execution_dir(base_dir: str) -> str:
    """
    Return the full path of the next 'Execution_N' directory inside base_dir.
    It will scan existing 'Execution_*' dirs, find the highest N, and increment.
    """
    os.makedirs(base_dir, exist_ok=True)

    # Find existing Execution_* directories and extract numeric suffix
    execution_nums = []
    for name in os.listdir(base_dir):
        full = os.path.join(base_dir, name)
        if os.path.isdir(full) and name.startswith("Execution_"):
            m = re.match(r"Execution_(\d+)$", name)
            if m:
                try:
                    execution_nums.append(int(m.group(1)))
                except ValueError:
                    pass

    next_num = (max(execution_nums) + 1) if execution_nums else 1
    next_dir = os.path.join(base_dir, f"Execution_{next_num}")
    os.makedirs(next_dir, exist_ok=True)
    return next_dir


def pytest_configure(config):
    """
    Creates folder structure:
      Reports/<dd-mm-YYYY>/Execution_N/allure-results
    and points Allure to write results there.
    """
    # 1) Root Reports folder under the current working directory
    reports_root = os.path.join(os.getcwd(), "Results")
    os.makedirs(reports_root, exist_ok=True)

    # 2) Today's date folder (dd-mm-YYYY)
    today_str = datetime.now().strftime("%d-%m-%Y")
    date_dir = os.path.join(reports_root, today_str)
    os.makedirs(date_dir, exist_ok=True)

    # 3) Create next Execution_N folder inside today's date folder
    new_execution_dir = _next_execution_dir(date_dir)

    # 4) Final Allure results folder path inside Execution_N
    allure_output = os.path.join(new_execution_dir, "allure-results")
    os.makedirs(allure_output, exist_ok=True)

    # 5) Point pytest-allure to the folder (works with --alluredir)
    # Note: Many setups expect config.option.allure_report_dir or config.option.allure_report_dir/alluredir
    # We'll set both common variants to be safe.
    setattr(config.option, "allure_report_dir", allure_output)
    setattr(config.option, "alluredir", allure_output)

    # Optional: Also set env var so other tools pick it up
    os.environ["ALLURE_RESULTS_DIR"] = allure_output


def pytest_sessionstart(session):
    # Optional dynamic title for the report
    try:
        allure.dynamic.title("Custom Execution Report")
    except Exception:
        # In case allure plugin isn't active for this session
        pass