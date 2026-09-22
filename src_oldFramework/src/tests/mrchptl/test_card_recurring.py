import pytest
import allure
from utils.excel_utils import ExcelUtil
from pages.payment.demo_payment_page import demoPage
from pages.payment.adpay_payment_page import PurchasePage

purchase_data = ExcelUtil.get_sheet("Datasheet", "adpay_Recurring_txn")
print("Loaded purchase_data:", purchase_data)

@pytest.mark.regression_sanity
@pytest.mark.sanity
@pytest.mark.parametrize("data", purchase_data)
@allure.feature("To verify Recurring Register & Recurring payment")
def test_adpay_Recurring_Register_Payment(page, data):
    demo = demoPage(page)
    recurring_reg=PurchasePage(page)
    demo.open_base()
    demo.go_recurring_registration()
    demo.fill_recurring_registration_form(
        tid=data["tid"],
        version=data["version"],    
        adgeid1=data["adgeid1"],
        service11=data["service11"],
        pwd=data["pwd"],
        udf1=data["udf1"]
    )
    demo.select_project_MRCHPTL()
    demo.click_buy()
    recurring_reg.fill_card_recurring_reg(
        name=data["card_name"],
        number=data["card_number"],
    )
    recurring_reg.fillcvv_recurring_reg(cvv=data["cvv"])
    recurring_reg.click_Recurringsaved_card()
    recurring_reg.capture_recurring_id()
    demo.go_back_home()
    demo.open_base()
    demo.go_recurring_payment()
    demo.fill_recurring_payment_form(
        tid=data["tid"],
        version=data["version"],
        corid=data["corid"],
        amount=data["amount"],
        pwd=data["pwd"],
        udf1=data["udf1"]
    )
    demo.select_project_MRCHPTL()
    recurring_reg.fill_capture_recurring_id()
    demo.click_buy()

purchase_data = ExcelUtil.get_sheet("Datasheet", "adpay_Recurring_txn")
print("Loaded purchase_data:", purchase_data)

@pytest.mark.regression_sanity
@pytest.mark.sanity
@pytest.mark.parametrize("data", purchase_data)
@allure.feature("To verify Recurring list, Recurring Register & Recurring payment")
def test_adpay_Listcard_Recurring_Register(page, data):
    demo = demoPage(page)
    recurring_reg=PurchasePage(page)
    demo.open_base()
    demo.go_recurring_listcards()
    demo.fill_recurring_listcards_form(
        tid=data["tid"],
        pwd=data["pwd"],
        udf1=data["udf1"]
    )
    demo.select_project_MRCHPTL()
    demo.click_buy()
    recurring_reg.capture_card_id()
    demo.open_base()
    demo.go_recurring_registration()
    demo.fill_recurring_registration_form(
        tid=data["tid"],
        version=data["version"],    
        adgeid1=data["adgeid1"],
        service11=data["service11"],
        pwd=data["pwd"],
        udf1=data["udf1"]
    )
    recurring_reg.fill_captured_card_id()
    demo.click_buy()
    recurring_reg.fillcvv_recurring_reg(cvv=data["cvv"])
    recurring_reg.click_Recurringsaved_card()
    recurring_reg.capture_recurring_id()
    demo.go_back_home()
    demo.open_base()
    demo.go_recurring_payment()
    demo.fill_recurring_payment_form(
        tid=data["tid"],
        version=data["version"],
        corid=data["corid"],
        amount=data["amount"],
        pwd=data["pwd"],
        udf1=data["udf1"]
    )
    demo.select_project_MRCHPTL()
    recurring_reg.fill_capture_recurring_id()
    demo.click_buy()


