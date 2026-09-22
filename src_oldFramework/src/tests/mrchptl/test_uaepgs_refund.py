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
@allure.feature("To Verify the ADPAy UAEPGS Refund Transactions for Versions 1.0.1, 1.0.6 & 1.0.7")
   
def test_ADPAY_UAEPGS_Refund(page, data):
    demo = demoPage(page)
    UaepgsPurchase = PurchasePage(page)
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
    demo.select_project_MRCHPTL()
    demo.fill_additionalAmounts(Amount1=data["DynamicAmount"], Amount2=data["DynamicAmount"])
    demo.fill_HeaderVersion(HeaderVersion=data["HeaderVersion"])
    demo.click_buy()
    UaepgsPurchase.click_change() 
    UaepgsPurchase.verify_adpay_summary_header()
    UaepgsPurchase.verify_Dhiramsymbol()
    UaepgsPurchase.click_direct_debit()
    UaepgsPurchase.pay()
    UaepgsPurchase.pause(10)  
    UaepgsPurchase.select_bank(data["Bank"])
    UaepgsPurchase.select_product(data["Product"])
    UaepgsPurchase.pause(10)
    UaepgsPurchase.submit()
    UaepgsPurchase.add_parameters(
        response_code=data["ResponseCode"],
        response_message=data["ResponseMessage"],
        auth_code=data["AuthCode"],
        bank_id=data["BankID"]
    )
    UaepgsPurchase.generate_hash_and_return_to_PG()
    UaepgsPurchase.pause(10)
    UaepgsPurchase.click_back_to_merchant()
    UaepgsPurchase.verify_payment_ADPay()
    UaepgsPurchase.capture_payment_id()
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
    demo.select_project_MRCHPTL()
    UaepgsPurchase.select_udf5(value=data["udf5"])
    UaepgsPurchase.fill_capture_payment_id()
    demo.click_refund()


    # Arabic changes for UAEPGS Purchase & Refund Transaction

purchase_data = ExcelUtil.get_sheet("Datasheet", "adpay_UAEPGS")
print("Loaded purchase_data:", purchase_data)

@pytest.mark.regression_sanity
@pytest.mark.sanity
@pytest.mark.parametrize("data", purchase_data)
@allure.feature("To Verify the ADPAy UAEPGS Refund Transactions for Versions 1.0.1, 1.0.6 & 1.0.7")
   
def test_ADPAY_UAEPGS_Refund_AR(page, data):
    demo = demoPage(page)
    UaepgsPurchase= PurchasePage(page)
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
    demo.select_project_MRCHPTL()
    demo.fill_additionalAmounts(Amount1=data["DynamicAmount"], Amount2=data["DynamicAmount"])
    demo.select_language(data["Lang"])
    demo.fill_HeaderVersion(HeaderVersion=data["HeaderVersion"])
    demo.click_buy()
    UaepgsPurchase.verify_adpay_summary_header_AR()
    UaepgsPurchase.verify_Dhiramsymbol_AR()
    UaepgsPurchase.click_change_AR()
    UaepgsPurchase.click_direct_debit()
    UaepgsPurchase.pay()
    UaepgsPurchase.pause(3)  
    UaepgsPurchase.select_bank(data["Bank"])
    UaepgsPurchase.select_product(data["Product"])
    UaepgsPurchase.pause(5)
    UaepgsPurchase.submit()
    UaepgsPurchase.add_parameters(
        response_code=data["ResponseCode"],
        response_message=data["ResponseMessage"],
        auth_code=data["AuthCode"],
        bank_id=data["BankID"]
    )
    UaepgsPurchase.generate_hash_and_return_to_PG()
    UaepgsPurchase.pause(10)
    UaepgsPurchase.click_back_to_merchant()
    UaepgsPurchase.verify_payment_ADPay()
    UaepgsPurchase.capture_payment_id()
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
    demo.select_project_MRCHPTL()
    UaepgsPurchase.select_udf5(value=data["udf5"])
    UaepgsPurchase.fill_capture_payment_id()
    demo.click_refund()