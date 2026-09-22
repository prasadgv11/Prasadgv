import pytest
import allure
from pages.payment.demo_payment_page import demoPage
from utils.excel_utils import ExcelUtil
from pages.payment.adpay_payment_page import PurchasePage
 
purchase_data = ExcelUtil.get_sheet("Datasheet", "adpay_UAEPGS")
print("Loaded purchase_data:", purchase_data)

@pytest.mark.regression_sanity
@pytest.mark.sanity
@pytest.mark.parametrize("data", purchase_data)
@allure.feature("To Verify the ADPAy UAEPGS Auth Transactions for Versions 1.0.1, 1.0.6 & 1.0.7")
   
def test_ADPAY_UAEPGS_Auth(page, data):
    demo = demoPage(page)
    UaepgsAuth = PurchasePage(page)
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
    demo.select_project_MRCHPTL()
    demo.fill_additionalAmounts(Amount1=data["DynamicAmount"], Amount2=data["DynamicAmount"])
    demo.fill_HeaderVersion(HeaderVersion=data["HeaderVersion"])
    demo.click_buy()
    UaepgsAuth.click_change() 
    UaepgsAuth.verify_adpay_summary_header()
    UaepgsAuth.verify_Dhiramsymbol()
    UaepgsAuth.click_direct_debit()
    UaepgsAuth.pay()
    UaepgsAuth.pause(10)  
    UaepgsAuth.select_bank(data["Bank"])
    UaepgsAuth.select_product(data["Product"])
    UaepgsAuth.pause(10)
    UaepgsAuth.submit()
    UaepgsAuth.add_parameters(
        response_code=data["ResponseCode"],
        response_message=data["ResponseMessage"],
        auth_code=data["AuthCode"],
        bank_id=data["BankID"]
    )
    UaepgsAuth.generate_hash_and_return_to_PG()
    UaepgsAuth.pause(10)
    UaepgsAuth.verify_payment_ADPay()
    UaepgsAuth.capture_payment_id()
    demo.go_back_home()
    demo.open_base()
    demo.go_inquiry()
    demo.fill_inquiry_form(
        tid=data["tid"],
        version=data["version"],
        pwd=data["pwd"],
        InqType=data["InqType"]
    )
    demo.select_project_MRCHPTL()
    UaepgsAuth.select_udf5(value=data["udf5"])
    UaepgsAuth.fill_capture_payment_id()
    demo.click_buy()
    UaepgsAuth.verify_payment_status()

# Arabic changes for UAEPGS Auth Transaction

purchase_data = ExcelUtil.get_sheet("Datasheet", "adpay_UAEPGS")
print("Loaded purchase_data:", purchase_data)

@pytest.mark.regression_sanity
@pytest.mark.sanity
@pytest.mark.parametrize("data", purchase_data)
@allure.feature("To Verify the ADPAy UAEPGS Auth Transactions for Versions 1.0.1, 1.0.6 & 1.0.7")
   
def test_ADPAY_UAEPGS_Auth_AR(page, data):
    demo = demoPage(page)
    UaepgsAuth = PurchasePage(page)
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
    demo.select_project_MRCHPTL()
    demo.fill_additionalAmounts(Amount1=data["DynamicAmount"], Amount2=data["DynamicAmount"])
    demo.select_language(data["Lang"])
    demo.fill_HeaderVersion(HeaderVersion=data["HeaderVersion"])
    demo.click_buy()
    UaepgsAuth.verify_adpay_summary_header_AR()
    UaepgsAuth.verify_Dhiramsymbol_AR()
    UaepgsAuth.click_change_AR()
    UaepgsAuth.click_direct_debit()
    UaepgsAuth.pay()
    UaepgsAuth.pause(3)  
    UaepgsAuth.select_bank(data["Bank"])
    UaepgsAuth.select_product(data["Product"])
    UaepgsAuth.pause(5)
    UaepgsAuth.submit()
    UaepgsAuth.add_parameters(
        response_code=data["ResponseCode"],
        response_message=data["ResponseMessage"],
        auth_code=data["AuthCode"],
        bank_id=data["BankID"]
    )
    UaepgsAuth.generate_hash_and_return_to_PG()
    UaepgsAuth.pause(10)
    UaepgsAuth.verify_payment_ADPay()
    UaepgsAuth.capture_payment_id()
    demo.go_back_home()
    demo.open_base()
    demo.go_inquiry()
    demo.fill_inquiry_form(
        tid=data["tid"],
        version=data["version"],
        pwd=data["pwd"],
        InqType=data["InqType"]
    )
    demo.select_project_MRCHPTL()
    UaepgsAuth.select_udf5(value=data["udf5"])
    UaepgsAuth.fill_capture_payment_id()
    demo.click_buy()
    UaepgsAuth.verify_payment_status()