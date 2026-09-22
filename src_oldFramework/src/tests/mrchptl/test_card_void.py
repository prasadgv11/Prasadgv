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
@allure.feature("To Verify the ADPAy EN Void Transactions for Versions 1.0.1, 1.0.6 & 1.0.7")
def test_ADPAY_cardpurchase(page, data):
    demo = demoPage(page)
    purchase=PurchasePage(page)
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
    purchase.verify_adpay_summary_header()
    purchase.verify_Dhiramsymbol()
    purchase.click_change()
    purchase.add_card(
        name=data["card_name"],
        number=data["card_number"],
        cvv=data["cvv"],
    )
    purchase.Select_month()
    purchase.Select_Year()
    purchase.pay_card()
    purchase.verify_payment_ADPay()
    purchase.capture_payment_id()
    demo.go_back_home()
    demo.open_base()
    demo.go_void()
    demo.fill_void_form(
        tid=data["tid"],
        version=data["version"],
        pwd=data["pwd"],
        corid=data["corid"],
    )
    demo.select_project_MRCHPTL()
    purchase.select_udf5(value=data["udf5"])
    purchase.fill_capture_payment_id()
    demo.click_buy()

# Arabic changes for Purchase & Void Transaction

purchase_data = ExcelUtil.get_sheet("Datasheet", "adpay_card")
print("Loaded purchase_data:", purchase_data)

@pytest.mark.regression_sanity
@pytest.mark.sanity
@pytest.mark.parametrize("data", purchase_data)
@allure.feature("To Verify the ADPAy AR Void Transactions for Versions 1.0.1, 1.0.6 & 1.0.7")
def test_ADPAY_cardVoid_AR(page, data):
    demo = demoPage(page)
    purchase=PurchasePage(page)
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
        udf1=data["udf1"],
    )
    demo.select_project_MRCHPTL()
    demo.fill_additionalAmounts(Amount1=data["DynamicAmount"], Amount2=data["DynamicAmount"])
    demo.select_language(data["Lang"])
    demo.fill_HeaderVersion(HeaderVersion=data["HeaderVersion"])
    demo.click_buy()
    purchase.verify_adpay_summary_header_AR()
    purchase.verify_Dhiramsymbol_AR()
    purchase.click_charity1_amt5_AR()
    purchase.click_charity1_amt10_AR()
    purchase.click_charity1_others_AR(charity_amt=data["charity_amount"])
    purchase.click_charity2_amt5_AR()
    purchase.click_charity2_amt10_AR()
    purchase.click_charity2_others_AR(charity_amt=data["charity_amount"])
    purchase.click_charity3_amt5_AR()
    purchase.click_charity3_amt10_AR()
    purchase.click_charity3_others_AR(charity_amt=data["charity_amount"])
    purchase.click_change_AR()
    purchase.add_card_AR(
        name=data["card_name"],
        number=data["card_number"],
        cvv=data["cvv"],
    )
    purchase.Select_month()
    purchase.Select_Year()
    purchase.pay_card()
    purchase.verify_payment_ADPay()
    purchase.capture_payment_id()
    demo.go_back_home()
    demo.open_base()
    demo.go_void()
    demo.fill_void_form(
        tid=data["tid"],
        version=data["version"],
        pwd=data["pwd"],
        corid=data["corid"],
    )
    demo.select_project_MRCHPTL()
    purchase.select_udf5(value=data["udf5"])
    purchase.fill_capture_payment_id()
    demo.click_buy()