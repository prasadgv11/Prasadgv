import pytest
import allure
from utils.excel_utils import ExcelUtil
from pages.payment.demo_payment_page import demoPage
from pages.payment.mpay_payment_page import PurchasePage

purchase_data = ExcelUtil.get_sheet("Datasheet", "mpay_tabby")
print("Loaded purchase_data:", purchase_data)

@pytest.mark.regression
@pytest.mark.sanity
@pytest.mark.parametrize("data", purchase_data)
@allure.feature("To Verify the MPAy Tabby EN Refund Transactions for Versions 1.0.1 & 1.0.5")
def test_MPAY_Refund_Tabby(page, data):
    demo = demoPage(page)
    tabbypurchase=PurchasePage(page)
    demo.open_base()
    demo.go_purchase()
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
    demo.select_project()
    demo.select_endpoint()
    demo.fill_purchase_form_mpaytabby(
        udf11=data["udf11"],
        udf12=data["udf12"]
    )
    demo.fill_EntityId(EntityId=data["ENTITYID"])
    demo.click_buy()
    tabbypurchase.select_tabbypayment()
    # tabbypurchase.fill_receipt_email(data["Receipt_email"])
    tabbypurchase.click_Mpay()
    tabbypurchase.pause(10)  # Adjust the pause duration as needed for the Tabby interface to load
    tabbypurchase.fill_tabby_email(
        email=data["email_tabby"], 
        otp=data["otp_tabby"]
        )
    tabbypurchase.accept_continue_button()
    tabbypurchase.no_of_emi_payments()
    tabbypurchase.verify_payment_Mpay()
    tabbypurchase.capture_payment_id()
    demo.go_back_home()
    demo.open_base()
    demo.go_refund()
    demo.fill_refund_form(
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
    demo.select_project()
    demo.select_endpoint()
    tabbypurchase.select_udf5(value=data["udf5"])
    tabbypurchase.fill_capture_payment_id()
    demo.click_refund()
   

# Arabic language
purchase_data = ExcelUtil.get_sheet("Datasheet", "mpay_tabby")
print("Loaded purchase_data:", purchase_data)

@pytest.mark.regression
@pytest.mark.sanity
@pytest.mark.parametrize("data", purchase_data)
@allure.feature("To Verify the MPAy Tabby AR Tabby Transactions for Versions 1.0.1 & 1.0.5")
def test_MPAY_Refund_Tabby_AR(page, data):
    demo = demoPage(page)
    tabbypurchase=PurchasePage(page)
    demo.open_base()
    demo.go_purchase()
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
    demo.select_project()
    demo.select_endpoint()
    demo.fill_purchase_form_mpaytabby(
        udf11=data["udf11"],
        udf12=data["udf12"]
    )
    demo.fill_EntityId(EntityId=data["ENTITYID"])
    demo.select_language(data["Lang"])
    demo.click_buy()
    tabbypurchase.click_charity1_checkbox_AR(charity_amt=data["charity_amount"])
    tabbypurchase.click_charity2_checkbox_AR(charity_amt=data["charity_amount"])
    tabbypurchase.click_charity3_checkbox_AR(charity_amt=data["charity_amount"])
    tabbypurchase.select_tabbypayment()
    # tabbypurchase.fill_receipt_email(data["Receipt_email"])
    tabbypurchase.click_Mpay()
    tabbypurchase.fill_tabby_emailcontinue_AR(
        Tabbyemail=data["email_tabby"], 
        otp=data["otp_tabby"]
    )
    tabbypurchase.accept_continue_button()
    tabbypurchase.no_of_emi_payments_AR()
    tabbypurchase.verify_payment_Mpay()
    tabbypurchase.capture_payment_id()
    demo.go_back_home()
    demo.open_base()
    demo.go_refund()
    demo.fill_refund_form(
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
    demo.select_project()
    demo.select_endpoint()
    tabbypurchase.select_udf5(value=data["udf5"])
    tabbypurchase.fill_capture_payment_id()
    demo.click_refund()
    