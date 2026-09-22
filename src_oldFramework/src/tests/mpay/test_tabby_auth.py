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
@allure.feature("To Verify the MPAy Tabby EN Auth Transactions for Versions 1.0.1 & 1.0.5")
def test_MPAY_Auth_Tabby(page, data):
    demo = demoPage(page)
    tabbyauth=PurchasePage(page)
    demo.open_base()
    demo.go_authorization()
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
    tabbyauth.select_tabbypayment()
    # tabbyauth.fill_receipt_email(data["Receipt_email"])
    tabbyauth.click_Mpay()
    tabbyauth.pause(10)  # Adjust the pause duration as needed for the Tabby interface to load
    tabbyauth.fill_tabby_email(
        email=data["email_tabby"], 
        otp=data["otp_tabby"]
        )
    tabbyauth.accept_continue_button()
    tabbyauth.no_of_emi_payments()
    tabbyauth.verify_payment_Mpay()
    tabbyauth.capture_payment_id()
    demo.go_back_home()
    demo.open_base()
    demo.go_inquiry()
    demo.fill_inquiry_form(
        tid=data["tid"],
        version=data["version"],
        pwd=data["pwd"],
        InqType=data["InqType"]
    )
    demo.select_project()
    demo.select_endpoint()
    tabbyauth.select_udf5(value=data["udf5"])
    tabbyauth.fill_capture_payment_id()
    demo.click_buy()
    tabbyauth.verify_payment_status_Mpay()


 # Arabic language
purchase_data = ExcelUtil.get_sheet("Datasheet", "mpay_tabby")
print("Loaded purchase_data:", purchase_data)

@pytest.mark.regression
@pytest.mark.sanity
@pytest.mark.parametrize("data", purchase_data)
@allure.feature("To Verify the MPAy Tabby AR Auth Transactions for Versions 1.0.1 & 1.0.5")
def test_MPAY_Auth_Tabby_AR(page, data):
    demo = demoPage(page)
    tabbyauth=PurchasePage(page)
    demo.open_base()
    demo.go_authorization()
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
    demo.select_language(data["Lang"])
    demo.fill_EntityId(EntityId=data["ENTITYID"])
    demo.click_buy()
    tabbyauth.click_charity1_checkbox_AR(charity_amt=data["charity_amount"])
    tabbyauth.click_charity2_checkbox_AR(charity_amt=data["charity_amount"])
    tabbyauth.click_charity3_checkbox_AR(charity_amt=data["charity_amount"])
    tabbyauth.select_tabbypayment()
    # tabbyauth.fill_receipt_email(data["Receipt_email"])
    tabbyauth.click_Mpay()
    tabbyauth.fill_tabby_emailcontinue_AR(
        Tabbyemail=data["email_tabby"], 
        otp=data["otp_tabby"]
    )
    # tabbyauth.accept_continue_button()
    tabbyauth.no_of_emi_payments_AR()
    tabbyauth.verify_payment_Mpay()
    tabbyauth.capture_payment_id()
    demo.go_back_home()
    demo.open_base()
    demo.go_inquiry()
    demo.fill_inquiry_form(
        tid=data["tid"],
        version=data["version"],
        pwd=data["pwd"],
        InqType=data["InqType"]
    )
    demo.select_project()
    demo.select_endpoint()
    tabbyauth.select_udf5(value=data["udf5"])
    tabbyauth.fill_capture_payment_id()
    demo.click_buy()
    tabbyauth.verify_payment_status_Mpay()
   
    