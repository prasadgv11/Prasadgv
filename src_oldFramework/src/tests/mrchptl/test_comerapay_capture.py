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
@allure.feature("To Verify the ADPAy EN Comerapay Capture Transactions for Versions 1.0.1, 1.0.6 & 1.0.7")
def test_ADPAY_comerapay_authorization(page, data):
    demo = demoPage(page)
    ComeraAuth = PurchasePage(page)
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
    ComeraAuth.verify_adpay_summary_header()
    ComeraAuth.verify_Dhiramsymbol()
    ComeraAuth.click_change()
    ComeraAuth.select_comerapay()
    ComeraAuth.comerapay_validations(
        ComerapayNumber=data["ComerapayNumber"],  
        ComerapayOTP=data["ComerapayOTP"]
    )
    ComeraAuth.pay()
    ComeraAuth.verify_payment_ADPay()
    ComeraAuth.capture_payment_id()
    demo.go_back_home()
    demo.open_base()
    demo.go_capture()
    demo.fill_capture_form(
       tid=data["tid"],
        version=data["version"],
        adgeid1=data["adgeid1"],
        service11=data["service11"],
        pwd=data["pwd"],
        corid=data["corid"],
        amount=data["amount"],
        qty=data["qty"],
        udf1=data["udf1"],
    )
    demo.select_project_MRCHPTL()
    ComeraAuth.select_udf5(value=data["udf5"])
    ComeraAuth.fill_capture_payment_id()
    demo.click_buy()


# Arabic changes for Comerapay Auth & Capture Transaction

purchase_data = ExcelUtil.get_sheet("Datasheet", "adpay_comerapay")
print("Loaded purchase_data:", purchase_data)

@pytest.mark.regression_sanity
@pytest.mark.sanity
@pytest.mark.parametrize("data", purchase_data)
@allure.feature("To Verify the ADPAy AR Comerapay Capture Transactions for Versions 1.0.1, 1.0.6 & 1.0.7")
def test_ADPAY_comerapay_authorization_AR(page, data):
    demo = demoPage(page)
    ComeraAuth = PurchasePage(page)
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
    ComeraAuth.verify_adpay_summary_header_AR()
    ComeraAuth.verify_Dhiramsymbol_AR()
    ComeraAuth.click_charity1_amt5_AR()
    ComeraAuth.click_charity1_amt10_AR()
    ComeraAuth.click_charity1_others_AR(charity_amt=data["charity_amount"])
    ComeraAuth.click_charity2_amt5_AR()
    ComeraAuth.click_charity2_amt10_AR()
    ComeraAuth.click_charity2_others_AR(charity_amt=data["charity_amount"])
    ComeraAuth.click_charity3_amt5_AR()
    ComeraAuth.click_charity3_amt10_AR()
    ComeraAuth.click_charity3_others_AR(amocharity_amtunt=data["charity_amount"])
    ComeraAuth.click_change_AR()
    ComeraAuth.click_comerapay_AR()
    ComeraAuth.comerapay_validations(
        ComerapayNumber=data["ComerapayNumber"],  
        ComerapayOTP=data["ComerapayOTP"]
    )
    ComeraAuth.pay()
    ComeraAuth.verify_payment_ADPay()
    ComeraAuth.capture_payment_id()
    demo.go_back_home()
    demo.open_base()
    demo.go_capture()
    demo.fill_capture_form(
       tid=data["tid"],
        version=data["version"],
        adgeid1=data["adgeid1"],
        service11=data["service11"],
        pwd=data["pwd"],
        corid=data["corid"],
        amount=data["amount"],
        qty=data["qty"],
        udf1=data["udf1"],
    )
    demo.select_project_MRCHPTL()
    ComeraAuth.select_udf5(value=data["udf5"])
    ComeraAuth.fill_capture_payment_id()
    demo.click_buy()

