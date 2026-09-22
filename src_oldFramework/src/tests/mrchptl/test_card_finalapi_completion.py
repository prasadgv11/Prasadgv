import pytest
import allure
from utils.excel_utils import ExcelUtil
from pages.payment.demo_payment_page import demoPage
from pages.payment.adpay_payment_page import PurchasePage

purchase_data = ExcelUtil.get_sheet("Datasheet", "adpay_finalapi")
print("Loaded purchase_data:", purchase_data)

@pytest.mark.regression_sanity
@pytest.mark.sanity
@pytest.mark.parametrize("data", purchase_data)
@allure.feature("To verify Finalization API Transactions for ADPAY")
def test_adpay_Finalapi_Authcompletion(page, data):
    demo = demoPage(page)
    Finalizationapi=PurchasePage(page)
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
    Finalizationapi.verify_adpay_summary_header()
    Finalizationapi.verify_Dhiramsymbol()
    Finalizationapi.click_change()
    Finalizationapi.add_card(
        name=data["card_name"],
        number=data["card_number"],
        cvv=data["cvv"],
    )
    Finalizationapi.Select_month()
    Finalizationapi.Select_Year()
    Finalizationapi.pay_card()
    Finalizationapi.capture_finalizationapiID()
    demo.go_back_home()
    demo.open_base()
    demo.go_finalization_api()
    demo.fill_finalization_api_form(
        tid=data["tid"],
        version=data["version"],
        pwd=data["pwd"],
    )
    demo.select_project_MRCHPTL()
    Finalizationapi.fill_capture_finalizationapiID_completion()
    demo.click_buy()



purchase_data = ExcelUtil.get_sheet("Datasheet", "adpay_finalapi")
print("Loaded purchase_data:", purchase_data)

@pytest.mark.regression_sanity
@pytest.mark.sanity
@pytest.mark.parametrize("data", purchase_data)
@allure.feature("To verify Finalization API Transactions for ADPAY")
def test_adpay_Finalapi_Purchasecompletion(page, data):
    demo = demoPage(page)
    Finalizationapi=PurchasePage(page)
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
    Finalizationapi.verify_adpay_summary_header()
    Finalizationapi.verify_Dhiramsymbol()
    Finalizationapi.click_change()
    Finalizationapi.add_card(
        name=data["card_name"],
        number=data["card_number"],
        cvv=data["cvv"],
    )
    Finalizationapi.Select_month()
    Finalizationapi.Select_Year()
    Finalizationapi.pay_card()
    Finalizationapi.capture_finalizationapiID()
    demo.go_back_home()
    demo.open_base()
    demo.go_finalization_api()
    demo.fill_finalization_api_form(
        tid=data["tid"],
        version=data["version"],
        pwd=data["pwd"],
    )
    demo.select_project_MRCHPTL()
    Finalizationapi.fill_capture_finalizationapiID_completion()
    demo.click_buy()