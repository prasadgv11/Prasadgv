import pytest
import allure
from utils.excel_utils import ExcelUtil
from pages.payment.demo_payment_page import demoPage
from pages.payment.adpay_payment_page import PurchasePage

purchase_data = ExcelUtil.get_sheet("Datasheet", "adpay_UAGEPGS_ICP")
print("Loaded purchase_data:", purchase_data)

@pytest.mark.regression_sanity
@pytest.mark.sanity
@pytest.mark.parametrize("data", purchase_data)
@allure.feature("To Verify the ADPAy EN ICP Changes Purchase Transactions for Versions 1.0.1 & 1.0.6")
def test_ADPAY_ICP_UAEPGS_Auth(page, data):
    demo = demoPage(page)
    icpUAEPGS=PurchasePage(page)
    demo.open_base()
    demo.go_purchase()
    demo.fill_ICP_form(
        tid=data["TID"],
        version=data["Version"],
        adgeid1=data["ADGEID1"],
        service1=data["Service1"],
        pwd=data["Password"],
        corid=data["CORID"],
        amount=data["Amount"],
        qty=data["Quantity"],
        Amount1=data["DynamicAmount1"],
        Amount2=data["DynamicAmount2"],
        Amount3=data["DynamicAmount3"],
        udf1=data["UDF1"])
    demo.fill_ICP_form_additionalservice(
        service2=data["Service2"],
        servamount2=data["Service2Amount"])
    demo.fill_ICP_form_Vndormerchant1(
        Venadgeid1=data["VendorADGEID1"],
        venserv1=data["VendorService1"],
        venserv1Amount=data["VendorService1Amount"],
        VenAmount1=data["VendorDynamicAmount1"],
        VenAmount2=data["VendorDynamicAmount2"],
        VenAmount3=data["VendorDynamicAmount3"])
    demo.fill_ICP_form_Vndormerchant2(
        Venadgeid2=data["VendorADGEID2"],
        venserv2=data["VendorService2"],
        venserv2Amount=data["VendorService2Amount"])
    demo.click_buy()
    icpUAEPGS.verify_adpay_summary_header()
    icpUAEPGS.verify_Dhiramsymbol()
    icpUAEPGS.click_selectpayment()
    icpUAEPGS.click_direct_debit()
    icpUAEPGS.pay()
    icpUAEPGS.pause(3)  
    icpUAEPGS.select_bank(data["Bank"])
    icpUAEPGS.select_product(data["Product"])
    icpUAEPGS.pause(5)
    icpUAEPGS.submit()
    icpUAEPGS.add_parameters(
        response_code=data["ResponseCode"],
        response_message=data["ResponseMessage"],
        auth_code=data["AuthCode"],
        bank_id=data["BankID"]
    )
    icpUAEPGS.generate_hash_and_return_to_PG()
    icpUAEPGS.pause(5)
    icpUAEPGS.verify_payment_ADPay()
    icpUAEPGS.capture_payment_id()
    demo.go_back_home()
    demo.open_base()
    demo.go_inquiry()
    demo.fill_inquiry_form(
        tid=data["TID"],
        version=data["Version"],
        pwd=data["Password"],
        InqType=data["InqType"]
    )
    icpUAEPGS.select_udf5(value=data["udf5"])
    icpUAEPGS.fill_capture_payment_id()
    demo.click_buy()
    icpUAEPGS.verify_payment_status()