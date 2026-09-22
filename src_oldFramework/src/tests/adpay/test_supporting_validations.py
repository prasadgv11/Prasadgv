import pytest
import allure
from utils.excel_utils import ExcelUtil
from pages.payment.demo_payment_page import demoPage


purchase_data = ExcelUtil.get_sheet("Datasheet", "Refund_page")
print("Loaded purchase_data:", purchase_data)

@pytest.mark.regression_sanity
@pytest.mark.sanity
@pytest.mark.parametrize("data", purchase_data)
@allure.feature("To verify the Refund page validations")
def test_DemoRefund_Validations(page, data):
    demo = demoPage(page)
    demo.open_base()
    demo.go_refund()
    demo.fill_purchase_form(
         tid=data["tid"],
        version=data["version"],
        adgeid1=data["adgeid1"],
        service11=data["service11"],
        pwd=data["pwd"],
        corid=data["corid"],
        amount=data["amount"],
        qty=data["qty"],
        udf1=data["udf1"]
    )
    demo.click_refund()
    demo.verify_Supporting_transactions_refund(Refund_Value=data["Assertvalue"])



purchase_data = ExcelUtil.get_sheet("Datasheet", "Void_page")
print("Loaded purchase_data:", purchase_data)

@pytest.mark.regression_sanity
@pytest.mark.sanity
@pytest.mark.parametrize("data", purchase_data)
@allure.feature("To verify the Void page validations")
def test_DemoVoid_Validations(page, data):
    demo = demoPage(page)
    demo.open_base()
    demo.go_void()
    demo.fill_void_form(
         tid=data["tid"],
        version=data["version"],
        pwd=data["pwd"],
        corid=data["corid"],
    )
    demo.click_buy()
    demo.verify_Supporting_transactions_refund(Refund_Value=data["Assertvalue"])


purchase_data = ExcelUtil.get_sheet("Datasheet", "Inquiry_page")
print("Loaded purchase_data:", purchase_data)

@pytest.mark.regression_sanity
@pytest.mark.sanity
@pytest.mark.parametrize("data", purchase_data)
@allure.feature("To verify the Inquiry page validations")
def test_DemoInquiry_Validations(page, data):
    demo = demoPage(page)
    demo.open_base()
    demo.go_inquiry()
    demo.fill_inquiry_form(
         tid=data["tid"],
        version=data["version"],
        pwd=data["pwd"],
        InqType=data["InqType"],
    )
    
    demo.click_buy()
    demo.verify_Inquiry_status(Inquiry_value=data["Assertvalue"])