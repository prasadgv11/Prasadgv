import pytest
import allure
from utils.excel_utils import ExcelUtil
from pages.payment.demo_payment_page import demoPage
from pages.payment.mpay_payment_page import PurchasePage

purchase_data = ExcelUtil.get_sheet("Datasheet", "mpay_UAEPGS")
print("Loaded purchase_data:", purchase_data)

@pytest.mark.regression
@pytest.mark.sanity
@pytest.mark.parametrize("data", purchase_data)
@allure.feature("To Verify the MPAy UAEPGS EN Auth Transactions for Versions 1.0.1 & 1.0.5")
def test_MPAY_uaepgs_auth(page, data):
    demo = demoPage(page)
    uaepgsauth=PurchasePage(page)
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
    uaepgsauth.click_uaepgs()
    # uaepgsauth.fill_receipt_email(data["Receipt_email"])
    uaepgsauth.click_Mpay()
    uaepgsauth.pause(3)
    uaepgsauth.select_bank(data["Bank"])
    uaepgsauth.select_product(data["Product"])
    uaepgsauth.pause(5)
    uaepgsauth.submit()
    uaepgsauth.add_parameters(
        response_code=data["ResponseCode"],
        response_message=data["ResponseMessage"],
        auth_code=data["AuthCode"],
        bank_id=data["BankID"]
    )
    uaepgsauth.generate_hash_and_return_to_PG()
    uaepgsauth.verify_payment_Mpay()
    uaepgsauth.capture_payment_id()
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
    uaepgsauth.select_udf5(value=data["udf5"])
    uaepgsauth.fill_capture_payment_id()
    demo.click_buy()
    uaepgsauth.verify_payment_status_Mpay()
    
# Arabic language in UAEPGS flow

purchase_data = ExcelUtil.get_sheet("Datasheet", "mpay_UAEPGS")
print("Loaded purchase_data:", purchase_data)

@pytest.mark.regression
@pytest.mark.sanity
@pytest.mark.parametrize("data", purchase_data)
@allure.feature("To Verify the MPAy UAEPGS AR Auth Transactions for Versions 1.0.1 & 1.0.5")
def test_MPAY_Auth_uaepgs_AR(page, data):
    demo = demoPage(page)
    uaepgsauth=PurchasePage(page)
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
    demo.select_language(data["Lang"])
    demo.click_buy()
    uaepgsauth.click_charity1_checkbox_AR(charity_amt=data["charity_amount"])
    uaepgsauth.click_charity2_checkbox_AR(charity_amt=data["charity_amount"])
    uaepgsauth.click_charity3_checkbox_AR(charity_amt=data["charity_amount"])
    uaepgsauth.click_uaepgs()
    # uaepgsauth.fill_receipt_email(data["Receipt_email"])
    uaepgsauth.click_Mpay()
    uaepgsauth.pause(3)
    uaepgsauth.select_bank(data["Bank"])
    uaepgsauth.select_product(data["Product"])
    uaepgsauth.pause(5)
    uaepgsauth.submit()
    uaepgsauth.add_parameters(
        response_code=data["ResponseCode"],
        response_message=data["ResponseMessage"],
        auth_code=data["AuthCode"],
        bank_id=data["BankID"]
    )
    uaepgsauth.generate_hash_and_return_to_PG()
    uaepgsauth.verify_payment_Mpay()
    uaepgsauth.capture_payment_id()
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
    uaepgsauth.select_udf5(value=data["udf5"])
    uaepgsauth.fill_capture_payment_id()
    demo.click_buy()
    uaepgsauth.verify_payment_status_Mpay()