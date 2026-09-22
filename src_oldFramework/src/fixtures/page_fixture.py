import pytest
import allure

@pytest.fixture
def page(browser, request):
    context = browser.new_context()
    page = context.new_page()
    yield page

    screenshot = page.screenshot()
    allure.attach(
        screenshot,
        name=request.node.name,
        attachment_type=allure.attachment_type.PNG
    )

    context.close()
