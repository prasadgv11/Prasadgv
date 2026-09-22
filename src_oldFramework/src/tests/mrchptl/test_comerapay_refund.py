import pytest
import allure
from pages.payment.demo_payment_page import demoPage
from utils.excel_utils import ExcelUtil
from pages.payment.adpay_payment_page import PurchasePage

purchase_data = ExcelUtil.get_sheet("Datasheet", "adpay_comerapay")
print("Loaded purchase_data:", purchase_data)

@pytest.mark.regression_sanity
@pytest.mark.sanity
@pytest.mark.parametrize("data", purchase_data)
@allure.feature("To Verify the ADPAy EN Comerapay Refund Transactions for Versions 1.0.1, 1.0.6 & 1.0.7")
def test_ADPAY_comerapay_refund(page, data):
    demo = demoPage(page)
    ComeraPurchase = PurchasePage(page)
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
    ComeraPurchase.verify_adpay_summary_header()
    ComeraPurchase.verify_Dhiramsymbol()
    ComeraPurchase.click_change()
    ComeraPurchase.select_comerapay()
    ComeraPurchase.comerapay_validations(
        ComerapayNumber=data["ComerapayNumber"],  
        ComerapayOTP=data["ComerapayOTP"]
    )
    ComeraPurchase.pay()
    ComeraPurchase.verify_payment_ADPay()
    ComeraPurchase.capture_payment_id()
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
    ComeraPurchase.select_udf5(value=data["udf5"])
    ComeraPurchase.fill_capture_payment_id()
    demo.click_refund()


# Arabic changes for Comerapay Purchase & Refund Transaction

purchase_data = ExcelUtil.get_sheet("Datasheet", "adpay_comerapay")
print("Loaded purchase_data:", purchase_data)

@pytest.mark.regression_sanity
@pytest.mark.sanity
@pytest.mark.parametrize("data", purchase_data)
@allure.feature("To Verify the ADPAy AR Comerapay Refund Transactions for Versions 1.0.1, 1.0.6 & 1.0.7")
def test_ADPAY_comerapay_Refund_AR(page, data):
    demo = demoPage(page)
    ComeraPurchase= PurchasePage(page)
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
    ComeraPurchase.verify_adpay_summary_header_AR()
    ComeraPurchase.verify_Dhiramsymbol_AR()
    ComeraPurchase.click_charity1_amt5_AR()
    ComeraPurchase.click_charity1_amt10_AR()
    ComeraPurchase.click_charity1_others_AR(charity_amt=data["charity_amount"])
    ComeraPurchase.click_charity2_amt5_AR()
    ComeraPurchase.click_charity2_amt10_AR()
    ComeraPurchase.click_charity2_others_AR(charity_amt=data["charity_amount"])
    ComeraPurchase.click_charity3_amt5_AR()
    ComeraPurchase.click_charity3_amt10_AR()
    ComeraPurchase.click_charity3_others_AR(charity_amt=data["charity_amount"])
    ComeraPurchase.click_change_AR()
    ComeraPurchase.click_comerapay_AR()
    ComeraPurchase.comerapay_validations(
        ComerapayNumber=data["ComerapayNumber"],  
        ComerapayOTP=data["ComerapayOTP"]
    )
    ComeraPurchase.pay()
    ComeraPurchase.verify_payment_ADPay()
    ComeraPurchase.capture_payment_id()
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
    ComeraPurchase.select_udf5(value=data["udf5"])
    ComeraPurchase.fill_capture_payment_id()
    demo.click_refund()