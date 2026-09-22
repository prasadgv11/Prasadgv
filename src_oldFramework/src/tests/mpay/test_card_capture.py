import pytest
import allure
from utils.excel_utils import ExcelUtil
from pages.payment.demo_payment_page import demoPage
from pages.payment.mpay_payment_page import PurchasePage

purchase_data = ExcelUtil.get_sheet("Datasheet", "mpay_card")
print("Loaded purchase_data:", purchase_data)

@pytest.mark.regression
@pytest.mark.sanity
@pytest.mark.parametrize("data", purchase_data)
@allure.feature("To Verify the MPay EN Capture Transactions for Versions 1.0.1 & 1.0.5")
def test_MPAY_Capture_card(page, data):
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
    demo.fill_EntityId(EntityId=data["ENTITYID"])
    demo.select_project()
    demo.select_endpoint()
    demo.fill_purchase_form_mpaytabby(udf11=data["udf11"], udf12=data["udf12"])
    demo.click_buy()
    auth.click_charity_checkbox(charity_amt=data["charity_amount"])
    auth.click_newcard()
    auth.fill_card_details(
        name=data["card_name"],
        number=data["card_number"],
        cvv=data["cvv"]
    )
    auth.select_MM(data["Exp_Month"])
    auth.select_YYYY(data["Exp_Year"])
    # auth.fill_receipt_email(data["Receipt_email"])
    auth.click_Mpay()
    auth.verify_payment_Mpay()
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
    demo.select_project()
    demo.select_endpoint()
    auth.select_udf5(value=data["udf5"])
    auth.fill_capture_payment_id()
    demo.click_buy()

# Arabic Language Auth
    
purchase_data = ExcelUtil.get_sheet("Datasheet", "mpay_card")
print("Loaded purchase_data:", purchase_data)

@pytest.mark.regression
@pytest.mark.sanity
@pytest.mark.parametrize("data", purchase_data)
@allure.feature("To Verify the MPay AR Capture Transactions for Versions 1.0.1 & 1.0.5")
def test_MPAY_Capture_card_AR(page, data):
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
    demo.select_project()
    demo.select_endpoint()
    demo.fill_EntityId(EntityId=data["ENTITYID"])   
    demo.select_language(data["Lang"])
    demo.click_buy()
    auth.click_newcard()
    auth.fill_card_details(
        name=data["card_name"],
        number=data["card_number"],
        cvv=data["cvv"]
    )
    auth.select_MM(data["Exp_Month"])
    auth.select_YYYY(data["Exp_Year"])
    auth.click_charity1_checkbox_AR(charity_amt=data["charity_amount"])
    auth.click_charity2_checkbox_AR(charity_amt=data["charity_amount"])
    auth.click_charity3_checkbox_AR(charity_amt=data["charity_amount"])
    # auth.fill_receipt_email(data["Receipt_email"])
    auth.click_Mpay()
    auth.verify_payment_Mpay()
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
    demo.select_project()
    demo.select_endpoint()
    auth.select_udf5(value=data["udf5"])
    auth.fill_capture_payment_id()
    demo.click_buy()
