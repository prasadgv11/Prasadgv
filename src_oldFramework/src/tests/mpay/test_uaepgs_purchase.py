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
@allure.feature("To Verify the MPAy UAEPGS EN Purchase Transactions for Versions 1.0.1 & 1.0.5")
def test_MPAY_uaepgs_purchase(page, data):
    demo = demoPage(page)
    uaepgspurchase=PurchasePage(page)
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
    uaepgspurchase.click_uaepgs()
    # uaepgspurchase.fill_receipt_email(data["Receipt_email"])
    uaepgspurchase.click_Mpay()
    uaepgspurchase.pause(3)
    uaepgspurchase.select_bank(data["Bank"])
    uaepgspurchase.select_product(data["Product"])
    uaepgspurchase.pause(5)
    uaepgspurchase.submit()
    uaepgspurchase.add_parameters(
        response_code=data["ResponseCode"],
        response_message=data["ResponseMessage"],
        auth_code=data["AuthCode"],
        bank_id=data["BankID"]
    )
    uaepgspurchase.generate_hash_and_return_to_PG()
    uaepgspurchase.verify_payment_Mpay()
    uaepgspurchase.capture_payment_id()
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
    uaepgspurchase.select_udf5(value=data["udf5"])
    uaepgspurchase.fill_capture_payment_id()
    demo.click_buy()
    uaepgspurchase.verify_payment_status_Mpay()


    # Arabic language in UAEPGS flow

purchase_data = ExcelUtil.get_sheet("Datasheet", "mpay_UAEPGS")
print("Loaded purchase_data:", purchase_data)

@pytest.mark.regression
@pytest.mark.sanity
@pytest.mark.parametrize("data", purchase_data)
@allure.feature("To Verify the MPAy UAEPGS AR Purchase Transactions for Versions 1.0.1 & 1.0.5")
def test_MPAY_purchase_uaepgs_AR(page, data):
    demo = demoPage(page)
    uaepgspurchase=PurchasePage(page)
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
    uaepgspurchase.click_charity1_checkbox_AR(charity_amt=data["charity_amount"])
    uaepgspurchase.click_charity2_checkbox_AR(charity_amt=data["charity_amount"])
    uaepgspurchase.click_charity3_checkbox_AR(charity_amt=data["charity_amount"])
    uaepgspurchase.click_uaepgs()
    # uaepgspurchase.fill_receipt_email(data["Receipt_email"])
    uaepgspurchase.click_Mpay()
    uaepgspurchase.pause(3)
    uaepgspurchase.select_bank(data["Bank"])
    uaepgspurchase.select_product(data["Product"])
    uaepgspurchase.pause(5)
    uaepgspurchase.submit()
    uaepgspurchase.add_parameters(
        response_code=data["ResponseCode"],
        response_message=data["ResponseMessage"],
        auth_code=data["AuthCode"],
        bank_id=data["BankID"]
    )
    uaepgspurchase.generate_hash_and_return_to_PG()
    uaepgspurchase.verify_payment_Mpay()
    uaepgspurchase.capture_payment_id()
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
    uaepgspurchase.select_udf5(value=data["udf5"])
    uaepgspurchase.fill_capture_payment_id()
    demo.click_buy()
    uaepgspurchase.verify_payment_status_Mpay()
    