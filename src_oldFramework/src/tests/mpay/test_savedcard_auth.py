import pytest
import allure
from utils.excel_utils import ExcelUtil
from pages.payment.demo_payment_page import demoPage
from pages.payment.mpay_payment_page import PurchasePage
    
purchase_data = ExcelUtil.get_sheet("Datasheet", "mpay_savedcard")
print("Loaded purchase_data:", purchase_data)

@pytest.mark.regression
@pytest.mark.sanity
@pytest.mark.parametrize("data", purchase_data)
@allure.feature("To Verify the MPAY Saved card Auth Transactions for Versions 1.0.1 & 1.0.5")
def test_MPAY_auth_saved_card(page, data):
    savedcardauth = PurchasePage(page)
    demo = demoPage(page)
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
    demo.fill_EntityId(EntityId=data["ENTITYID"])
    demo.click_buy()
    savedcardauth.click_saved_Mastercard(sc_cvv=data["cvv"])
    savedcardauth.click_charity_checkbox(charity_amt=data["charity_amount"])
    # savedcardauth.fill_receipt_email(data["Receipt_email"])
    savedcardauth.click_Mpay()
    savedcardauth.verify_payment_Mpay()
    savedcardauth.capture_payment_id()
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
    savedcardauth.select_udf5(value=data["udf5"])
    savedcardauth.fill_capture_payment_id()
    demo.click_buy()
    savedcardauth.verify_payment_status_Mpay()