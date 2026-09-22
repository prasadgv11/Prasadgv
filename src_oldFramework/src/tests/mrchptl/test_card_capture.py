import pytest
import allure
from utils.excel_utils import ExcelUtil
from pages.payment.demo_payment_page import demoPage
from pages.payment.adpay_payment_page import PurchasePage

purchase_data = ExcelUtil.get_sheet("Datasheet", "adpay_card")
print("Loaded purchase_data:", purchase_data)

@pytest.mark.regression_sanity
@pytest.mark.sanity
@pytest.mark.parametrize("data", purchase_data)
@allure.feature("To Verify the ADPAy EN Capture Transactions for Versions 1.0.1, 1.0.6 & 1.0.7")
def test_ADPAY_cardAuth_Capture(page, data):
    demo = demoPage(page)
    auth=PurchasePage(page)
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
    auth.verify_adpay_summary_header()
    auth.verify_Dhiramsymbol()
    auth.click_change()
    auth.add_card(
        name=data["card_name"],
        number=data["card_number"],
        cvv=data["cvv"],
    )
    auth.Select_month()
    auth.Select_Year()
    auth.pay_card()
    auth.verify_payment_ADPay()
    auth.capture_payment_id()
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
        udf1=data["udf1"]
    )
    demo.select_project_MRCHPTL()
    auth.select_udf5(value=data["udf5"])
    auth.fill_capture_payment_id()
    demo.click_buy()


# Arabic changes for Auth & Capture Transaction

purchase_data = ExcelUtil.get_sheet("Datasheet", "adpay_card")
print("Loaded purchase_data:", purchase_data)

@pytest.mark.regression_sanity
@pytest.mark.sanity
@pytest.mark.parametrize("data", purchase_data)
@allure.feature("To Verify the ADPAy AR Capture Transactions for Versions 1.0.1, 1.0.6 & 1.0.7")
def test_ADPAY_cardAuth_Capture_AR(page, data):
    demo = demoPage(page)
    auth=PurchasePage(page)
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
        udf1=data["udf1"],
    )
    demo.select_project_MRCHPTL()
    demo.fill_additionalAmounts(Amount1=data["DynamicAmount"], Amount2=data["DynamicAmount"])
    demo.select_language(data["Lang"])
    demo.fill_HeaderVersion(HeaderVersion=data["HeaderVersion"])
    demo.click_buy()
    auth.verify_adpay_summary_header_AR()
    auth.verify_Dhiramsymbol_AR()
    auth.click_charity1_amt5_AR()
    auth.click_charity1_amt10_AR()
    auth.click_charity1_others_AR(charity_amt=data["charity_amount"])
    auth.click_charity2_amt5_AR()
    auth.click_charity2_amt10_AR()
    auth.click_charity2_others_AR(charity_amt=data["charity_amount"])
    auth.click_charity3_amt5_AR()
    auth.click_charity3_amt10_AR()
    auth.click_charity3_others_AR(charity_amt=data["charity_amount"])
    auth.click_change_AR()
    auth.add_card_AR(
        name=data["card_name"],
        number=data["card_number"],
        cvv=data["cvv"],
    )
    auth.Select_month()
    auth.Select_Year()
    auth.pay_card()
    auth.verify_payment_ADPay()
    auth.capture_payment_id()
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
        udf1=data["udf1"]
    )
    demo.select_project_MRCHPTL()
    auth.select_udf5(value=data["udf5"])
    auth.fill_capture_payment_id()
    demo.click_buy()


