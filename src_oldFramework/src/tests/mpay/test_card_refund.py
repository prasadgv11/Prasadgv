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
@allure.feature("To Verify the MPay EN Refund Transactions for Versions 1.0.1 & 1.0.5")
def test_MPAY_Refund_card(page, data):
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
    demo.select_project()
    demo.select_endpoint()
    demo.fill_purchase_form_mpaytabby(udf11=data["udf11"], udf12=data["udf12"])
    demo.fill_EntityId(EntityId=data["ENTITYID"])
    demo.click_buy()
    purchase.click_charity_checkbox(
        charity_amt=data["charity_amt"]
    )
    purchase.click_newcard()
    purchase.fill_card_details(
        name=data["card_name"],
        number=data["card_number"],
        cvv=data["cvv"]
    )
    purchase.select_MM(data["Exp_Month"])
    purchase.select_YYYY(data["Exp_Year"])
    purchase.fill_receipt_email(data["Receipt_email"])
    purchase.click_Mpay()
    purchase.verify_payment_Mpay()
    purchase.capture_payment_id()
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
    demo.select_project()
    demo.select_endpoint()
    purchase.select_udf5(value=data["udf5"])
    purchase.fill_capture_payment_id()
    demo.click_refund()

    
# Arabic Language  Purchase
    
purchase_data = ExcelUtil.get_sheet("Datasheet", "mpay_card")
print("Loaded purchase_data:", purchase_data)

@pytest.mark.regression
@pytest.mark.sanity
@pytest.mark.parametrize("data", purchase_data)
@allure.feature("To Verify the MPay AR Refund Transactions for Versions 1.0.1 & 1.0.5")
def test_MPAY_Refund_card_AR(page, data):
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
    demo.select_project()
    demo.select_endpoint()    
    demo.select_language(data["Lang"])
    demo.fill_EntityId(EntityId=data["ENTITYID"])
    demo.click_buy()
    purchase.click_newcard()
    purchase.fill_card_details(
        name=data["card_name"],
        number=data["card_number"],
        cvv=data["cvv"]
    )
    purchase.select_MM(data["Exp_Month"])
    purchase.select_YYYY(data["Exp_Year"])
    purchase.click_charity1_checkbox_AR(charity_amt=data["charity_amt"])
    purchase.click_charity2_checkbox_AR(charity_amt=data["charity_amt"])
    purchase.click_charity3_checkbox_AR(charity_amt=data["charity_amt"])
    # purchase.fill_receipt_email(data["Receipt_email"])
    purchase.click_Mpay()
    purchase.verify_payment_Mpay()
    purchase.capture_payment_id()
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
    demo.select_project()
    demo.select_endpoint()
    purchase.select_udf5(value=data["udf5"])
    purchase.fill_capture_payment_id()
    demo.click_refund()
 
    