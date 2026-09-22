import pytest
import allure
from utils.excel_utils import ExcelUtil
from pages.payment.demo_payment_page import demoPage
from pages.payment.adpay_payment_page import PurchasePage
 
# Master saved card details:
 
purchase_data = ExcelUtil.get_sheet("Datasheet", "Saved_card_adpay")
print("Loaded purchase_data:", purchase_data)
 
@pytest.mark.regression_sanity
@pytest.mark.sanity
@pytest.mark.parametrize("data", purchase_data)
@allure.feature("To Verify the ADPAy Master Saved card Purchase Transactions for Versions 1.0.1, 1.0.6 & 1.0.7")
def test_ADPAY_Master_savedcardpurchase_AR(page, data):
    demo = demoPage(page)
    savedcardpurchase=PurchasePage(page)
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
    savedcardpurchase.verify_adpay_summary_header_AR()
    savedcardpurchase.verify_Dhiramsymbol_AR()
    savedcardpurchase.click_charity1_amt5_AR()
    savedcardpurchase.click_charity1_amt10_AR()
    savedcardpurchase.click_charity1_others_AR(charity_amt=data["charity_amount"])
    savedcardpurchase.click_charity2_amt5_AR()
    savedcardpurchase.click_charity2_amt10_AR()
    savedcardpurchase.click_charity2_others_AR(charity_amt=data["charity_amount"])
    savedcardpurchase.click_charity3_amt5_AR()
    savedcardpurchase.click_charity3_amt10_AR()
    savedcardpurchase.click_charity3_others_AR(charity_amt=data["charity_amount"])
    savedcardpurchase.click_change_AR()
    savedcardpurchase.saved_card_details_Mastercard(cvv=data["cvv"])
    savedcardpurchase.pay()
    savedcardpurchase.verify_payment_ADPay()
    savedcardpurchase.capture_payment_id()
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
    savedcardpurchase.select_udf5(value=data["udf5"])
    savedcardpurchase.fill_capture_payment_id()
    demo.click_buy()
    savedcardpurchase.verify_payment_status()

# Amex saved card details:
   
purchase_data = ExcelUtil.get_sheet("Datasheet", "Saved_card_adpay")
print("Loaded purchase_data:", purchase_data)
 
@pytest.mark.regression_sanity
@pytest.mark.sanity
@pytest.mark.parametrize("data", purchase_data)
@allure.feature("To Verify the ADPAy Amex Saved card Purchase Transactions for Versions 1.0.1, 1.0.6 & 1.0.7")
def test_ADPAY_Amex_savedcardpurchase_AR(page, data):
    demo = demoPage(page)
    savedcardpurchase=PurchasePage(page)
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
    savedcardpurchase.verify_adpay_summary_header_AR()
    savedcardpurchase.verify_Dhiramsymbol_AR()
    savedcardpurchase.click_charity1_amt5_AR()
    savedcardpurchase.click_charity1_amt10_AR()
    savedcardpurchase.click_charity1_others_AR(charity_amt=data["charity_amount"])
    savedcardpurchase.click_charity2_amt5_AR()
    savedcardpurchase.click_charity2_amt10_AR()
    savedcardpurchase.click_charity2_others_AR(charity_amt=data["charity_amount"])
    savedcardpurchase.click_charity3_amt5_AR()
    savedcardpurchase.click_charity3_amt10_AR()
    savedcardpurchase.click_charity3_others_AR(charity_amt=data["charity_amount"])
    savedcardpurchase.click_change_AR()
    savedcardpurchase.saved_card_details_amex(cvv=data["cvv"])
    savedcardpurchase.pay()
    savedcardpurchase.verify_payment_ADPay()
    savedcardpurchase.capture_payment_id()
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
    savedcardpurchase.select_udf5(value=data["udf5"])
    savedcardpurchase.fill_capture_payment_id()
    demo.click_buy()
    savedcardpurchase.verify_payment_status()
   
# Visa saved card details
   
purchase_data = ExcelUtil.get_sheet("Datasheet", "Saved_card_adpay")
print("Loaded purchase_data:", purchase_data)
 
@pytest.mark.regression_sanity
@pytest.mark.sanity
@pytest.mark.parametrize("data", purchase_data)
@allure.feature("To Verify the Visa ADPAy Saved card Purchase Transactions for Versions 1.0.1, 1.0.6 & 1.0.7")
def test_ADPAY_Visa_savedcardpurchase_AR(page, data):
    demo = demoPage(page)
    savedcardpurchase=PurchasePage(page)
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
    savedcardpurchase.verify_adpay_summary_header_AR()
    savedcardpurchase.verify_Dhiramsymbol_AR()
    savedcardpurchase.click_charity1_amt5_AR()
    savedcardpurchase.click_charity1_amt10_AR()
    savedcardpurchase.click_charity1_others_AR(charity_amt=data["charity_amount"])
    savedcardpurchase.click_charity2_amt5_AR()
    savedcardpurchase.click_charity2_amt10_AR()
    savedcardpurchase.click_charity2_others_AR(charity_amt=data["charity_amount"])
    savedcardpurchase.click_charity3_amt5_AR()
    savedcardpurchase.click_charity3_amt10_AR()
    savedcardpurchase.click_charity3_others_AR(charity_amt=data["charity_amount"])
    savedcardpurchase.click_change_AR()
    savedcardpurchase.click_viewmore()
    savedcardpurchase.saved_card_details_visa(cvv=data["cvv"])
    savedcardpurchase.pay()
    savedcardpurchase.verify_payment_ADPay()
    savedcardpurchase.capture_payment_id()
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
    savedcardpurchase.select_udf5(value=data["udf5"])
    savedcardpurchase.fill_capture_payment_id()
    demo.click_buy()
    savedcardpurchase.verify_payment_status()


# Jaywan saved card details
   
purchase_data = ExcelUtil.get_sheet("Datasheet", "Saved_card_adpay")
print("Loaded purchase_data:", purchase_data)
 
@pytest.mark.regression_sanity
@pytest.mark.sanity
@pytest.mark.parametrize("data", purchase_data)
@allure.feature("To Verify the ADPAy Jaywan Saved card Purchase Transactions for Versions 1.0.1, 1.0.6 & 1.0.7")
def test_ADPAY_Jaywan_savedcardpurchase_AR(page, data):
    demo = demoPage(page)
    savedcardpurchase=PurchasePage(page)
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
    savedcardpurchase.verify_adpay_summary_header_AR()
    savedcardpurchase.verify_Dhiramsymbol_AR()
    savedcardpurchase.click_charity1_amt5_AR()
    savedcardpurchase.click_charity1_amt10_AR()
    savedcardpurchase.click_charity1_others_AR(charity_amt=data["charity_amount"])
    savedcardpurchase.click_charity2_amt5_AR()
    savedcardpurchase.click_charity2_amt10_AR()
    savedcardpurchase.click_charity2_others_AR(charity_amt=data["charity_amount"])
    savedcardpurchase.click_charity3_amt5_AR()
    savedcardpurchase.click_charity3_amt10_AR()
    savedcardpurchase.click_charity3_others_AR(charity_amt=data["charity_amount"])
    savedcardpurchase.click_change_AR()
    savedcardpurchase.saved_card_details_jaywan(cvv=data["cvv"])
    savedcardpurchase.pay()
    savedcardpurchase.verify_payment_ADPay()
    savedcardpurchase.capture_payment_id()
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
    savedcardpurchase.select_udf5(value=data["udf5"])
    savedcardpurchase.fill_capture_payment_id()
    demo.click_buy()
    savedcardpurchase.verify_payment_status()