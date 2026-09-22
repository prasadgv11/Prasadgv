# src/pages/adpay/purchase_page.py
import allure
from pages.base_page import BasePage
from locator.Home_locators import HomeLocators


class demoPage(BasePage):

    def __init__(self, page, module_name="Payments"):
        super().__init__(page, module_name=module_name)
        self.captured_payment_id = None  # Store payment ID for reuse

    @allure.step("Open Demo URL (from HomeLocators)")
    def open_base(self):
        self.navigate(HomeLocators.Demo_URL)
        
    @allure.step("Go back to Home Page")
    def go_back_home(self):
        self.page.get_by_role("link", name="Home Page").click()

    @allure.step("Go to Purchase Page Action code :1 ")
    def go_purchase(self):
        self.page.get_by_role("link", name="Purchase", exact=True).click()

    @allure.step("Go back to Refund Page Action code :2")
    def go_refund(self):
        self.page.get_by_role("link", name="Refund").click()

    @allure.step("Go back to Void Page Action code :3")
    def go_void(self):
        self.page.get_by_role("link", name="Void").click()

    @allure.step("Go back to Authorization Page Action code :4")
    def go_authorization(self):
        self.page.get_by_role("link", name="Authorization").click()
    
    @allure.step("Go to  Capture  Page Action code :5")
    def go_capture(self):
        self.page.get_by_role("link", name=" Capture ", exact=True).click()

    @allure.step("Go to Inquiry Page Action code :8")
    def go_inquiry(self):
        self.page.get_by_role("link", name="Inquiry", exact=True).click()


    @allure.step("Fill Purchase & Authorization form")
    def fill_purchase_form(self, tid, version, adgeid1, service11, pwd, corid, amount, qty, udf1):
        self.fill_by_locator(HomeLocators.TID, tid, description="TID")
        self.fill_by_locator(HomeLocators.Version, version, description="Version")
        self.fill_by_locator(HomeLocators.ADGEID1, adgeid1, description="ADGEID1")
        self.fill_by_locator(HomeLocators.Service11, service11, description="Service11")
        self.fill_by_locator(HomeLocators.Password, pwd, description="Password")
        self.fill_by_locator(HomeLocators.CORID, corid, description="CORID")
        self.fill_by_locator(HomeLocators.Amount, amount, description="Amount")
        self.fill_by_locator(HomeLocators.Quantity, qty, description="Quantity")
        self.fill_by_locator(HomeLocators.UDF1, udf1, description="UDF1")

    @allure.step("Fill refund form")
    def fill_refund_form(self, tid, version, adgeid1, service11, pwd, corid, amount, qty, udf1):
        self.fill_by_locator(HomeLocators.TID, tid, description="TID")
        self.fill_by_locator(HomeLocators.Version, version, description="Version")
        self.fill_by_locator(HomeLocators.ADGEID1, adgeid1, description="ADGEID1")
        self.fill_by_locator(HomeLocators.Service11, service11, description="Service11")
        self.fill_by_locator(HomeLocators.Password, pwd, description="Password")
        self.fill_by_locator(HomeLocators.CORID, corid, description="CORID")
        self.fill_by_locator(HomeLocators.Amount, amount, description="Amount")
        self.fill_by_locator(HomeLocators.Quantity, qty, description="Quantity")
        self.fill_by_locator(HomeLocators.UDF1, udf1, description="UDF1")


    @allure.step("Fill capture form")
    def fill_capture_form(self, tid, version, adgeid1, service11, pwd, corid, amount, qty, udf1):
        self.fill_by_locator(HomeLocators.TID, tid, description="TID")
        self.fill_by_locator(HomeLocators.Version, version, description="Version")
        self.fill_by_locator(HomeLocators.ADGEID1, adgeid1, description="ADGEID1")
        self.fill_by_locator(HomeLocators.Service11, service11, description="Service11")
        self.fill_by_locator(HomeLocators.Password, pwd, description="Password")
        self.fill_by_locator(HomeLocators.CORID, corid, description="CORID")
        self.fill_by_locator(HomeLocators.Amount, amount, description="Amount")
        self.fill_by_locator(HomeLocators.Quantity, qty, description="Quantity")
        self.fill_by_locator(HomeLocators.UDF1, udf1, description="UDF1")

    @allure.step("Fill void form")
    def fill_void_form(self, tid, version, pwd, corid):
        self.fill_by_locator(HomeLocators.TID, tid, description="TID")
        self.fill_by_locator(HomeLocators.Version, version, description="Version")
        self.fill_by_locator(HomeLocators.Password, pwd, description="Password")
        self.fill_by_locator(HomeLocators.CORID, corid, description="CORID")
    

    @allure.step("Fill inquiry form")
    def fill_inquiry_form(self, tid, version, pwd, InqType):
        self.fill_by_locator(HomeLocators.TID, tid, description="TID")
        self.fill_by_locator(HomeLocators.Version, version, description="Version")
        self.fill_by_locator(HomeLocators.Password, pwd, description="Password")
        self.fill_by_locator(HomeLocators.InqType, InqType, description="InqType")

    @allure.step("Fill Additional Mpay purchase form")
    def fill_purchase_form_mpaytabby(self,udf11, udf12):
        self.fill_by_locator(HomeLocators.udf11, udf11, description="UDF11")
        self.fill_by_locator(HomeLocators.UDF12, udf12, description="UDF12")


    @allure.step("Fill Additional Amounts for Dynamic Fee charges version 1.0.6")
    def fill_additionalAmounts(self,Amount1, Amount2):
        self.fill_by_xpath(HomeLocators.dynamicamount1, Amount1, description="Dynamic Fee Amount")
        self.fill_by_xpath(HomeLocators.dynamicamount2, Amount2, description="Dynamic Fee Amount")

    
    @allure.step("Select endpoint")
    def select_endpoint(self):
        self.select_by_xpath(HomeLocators.select_endpoint, by="index", option=2, description="select the MPay endpoints") 
    
    @allure.step("Select Project for MPAY")
    def select_project(self):
        self.select_by_xpath(HomeLocators.select_project, by="index", option=4, description="select the MPay Project") 

    @allure.step("Select Project for MRCHPTL")
    def select_project_MRCHPTL(self):
        self.select_by_xpath(HomeLocators.select_project, by="index", option=1, description="select the MRCHPTL Project") 
        


    @allure.step("Click Buy")
    def click_buy(self):
        self.click_by_xpath(HomeLocators.Buy_Button, description="Buy button")

    @allure.step("Go to Home Page")
    def go_home(self):
        self.click(HomeLocators.Home_Link, description="Home Page link")

   
    @allure.step("Click refund button")
    def click_refund(self):
        self.click_by_getbyrole(HomeLocators.Refund_Button, description="Refund button")

    @allure.step("Click refund button")
    def click_refund(self):
        self.click_by_getbyrole(HomeLocators.Refund_Button, description="Refund button")

    @allure.step("Select language: {value}")
    def select_language(self, value: str) -> None:
        self.select_by_xpath(HomeLocators.Language, description="Select Language", option=value)

 # Recurring ListCards:
    
    @allure.step("Go to Recurring ListCards Page")
    def go_recurring_listcards(self):
        self.page.get_by_role("link", name="Recurring ListCards", exact=True).click()
    
    @allure.step("Fill Recurring ListCards form")
    def fill_recurring_listcards_form(self, tid, pwd, udf1):
        self.fill_by_locator(HomeLocators.TID, tid, description="TID")
        self.fill_by_locator(HomeLocators.Password, pwd, description="Password")
        self.fill_by_locator(HomeLocators.UDF1, udf1, description="UDF1")
        
    # Recurring Registration:
    
    @allure.step("Go to Recurring Registration Page")
    def go_recurring_registration(self):
        self.page.get_by_role("link", name="Recurring Registration", exact=True).click()
        
    @allure.step("Fill Recurring Registration form")
    def fill_recurring_registration_form(self, tid, version, adgeid1, service11, pwd, udf1):
        self.fill_by_locator(HomeLocators.TID, tid, description="TID")
        self.fill_by_locator(HomeLocators.Version, version, description="Version")
        self.fill_by_locator(HomeLocators.ADGEID1, adgeid1, description="ADGEID1")
        self.fill_by_locator(HomeLocators.Service11, service11, description="Service11")
        self.fill_by_locator(HomeLocators.Password, pwd, description="Password")
        self.fill_by_locator(HomeLocators.UDF1, udf1, description="UDF1")
        
    @allure.step("Click saved card")
    def click_saved_card(self):
        self.click_by_xpath(HomeLocators.saved_card, description="Click saved card")
        
    # Recurring Payments:
    
    @allure.step("Go to Recurring Registration Page")
    def go_recurring_payment(self):
        self.page.get_by_role("link", name="Recurring Payment", exact=True).click()
    
    @allure.step("Fill Recurring Payment form")
    def fill_recurring_payment_form(self, tid, version, corid, amount, pwd, udf1):
        self.fill_by_locator(HomeLocators.TID, tid, description="TID")
        self.fill_by_locator(HomeLocators.Version, version, description="Version")
        self.fill_by_locator(HomeLocators.Password, pwd, description="Password")
        self.fill_by_locator(HomeLocators.CORID, corid, description="CORID")
        self.fill_by_locator(HomeLocators.RP_amount, amount, description="Amount")
        self.fill_by_xpath(HomeLocators.RP_udf1, udf1, description="UDF1")


    @allure.step("Select Project for MPAY")
    def select_recurring_project(self):
        self.select_by_xpath(HomeLocators.select_project, by="index", option=5, description="select the MPay Project") 
        
    # Finalization API:
    
    @allure.step("Go to Finalization API Page")
    def go_finalization_api(self):
        self.page.get_by_role("link", name="Finalization API", exact=True).click()
    
    @allure.step("Fill Finalization API form")
    def fill_finalization_api_form(self, tid, version, pwd):
        self.fill_by_locator(HomeLocators.TID, tid, description="TID")
        self.fill_by_locator(HomeLocators.Version, version, description="Version")
        self.fill_by_locator(HomeLocators.Password, pwd, description="Password")


    @allure.step("Verify ADPAY Summary header with exact text")
    def verify_Supporting_transactions_refund(self, Refund_Value):
        self.assert_visible(HomeLocators.Refund_Assert, description="Refund Aseert validations Results")
        self.assert_text(HomeLocators.Refund_Assert, expected_text=Refund_Value, description="Payment Result text")

    @allure.step("Select UDF5 option: {value}")
    def select_udf5(self, value: str) -> None:
       self.select_by_xpath(HomeLocators.UDF5_Select, description="UDF5 dropdown", option=value)

    @allure.step("Fill paymentid, corid or Transactions ID")
    def fill_refundID(self, refundId):
        self.fill_by_xpath(HomeLocators.refundId, refundId, description="refundId")
        
    
    @allure.step("Fill Entity ID")
    def fill_EntityId(self, EntityId):
        self.fill_by_xpath(HomeLocators.EntityId, EntityId, description="EntityId")
    
    @allure.step("Fill HeaderVersion")
    def fill_HeaderVersion(self, HeaderVersion):
        self.fill_by_xpath(HomeLocators.HeaderVersion, HeaderVersion, description="HeaderVersion")

    @allure.step("Verify payment status")
    def verify_Inquiry_status(self, Inquiry_value):
        self.assert_visible(HomeLocators.Inquiry_response, description="Refund Aseert validations Results")
        self.assert_text(HomeLocators.Inquiry_response, expected_text=Inquiry_value, description="Payment Result text")

    @allure.step("Fill ICP Purchase & Authorization form")
    def fill_ICP_form(self, tid, version, adgeid1, service1, pwd, corid, amount, qty, Amount1, Amount2, Amount3, udf1):
        self.fill_by_locator(HomeLocators.TID, tid, description="TID")
        self.fill_by_locator(HomeLocators.Password, pwd, description="Password")
        self.fill_by_locator(HomeLocators.Version, version, description="Version")
        self.fill_by_locator(HomeLocators.CORID, corid, description="CORID")
        self.fill_by_locator(HomeLocators.ADGEID1, adgeid1, description="ADGEID1")
        self.fill_by_locator(HomeLocators.Service11, service1, description="Service1")
        self.fill_by_locator(HomeLocators.Quantity, qty, description="Quantity")
        self.fill_by_locator(HomeLocators.Amount, amount, description="Amount")
        self.fill_by_xpath(HomeLocators.dynamicamount1, Amount1, description="Dynamic Fee Amount")
        self.fill_by_xpath(HomeLocators.dynamicamount2, Amount2, description="Dynamic Fee Amount")
        self.fill_by_xpath(HomeLocators.dynamicamount3, Amount3, description="Dynamic Fee Amount")
        self.fill_by_locator(HomeLocators.UDF1, udf1, description="UDF1")

    @allure.step("Fill ICP Purchase & Authorization form")
    def fill_ICP_form_additionalservice(self,service2, servamount2):
        self.fill_by_xpath(HomeLocators.service2, service2, description="Additional Service Name")
        self.fill_by_xpath(HomeLocators.serviceAmount2, servamount2, description="Additional Service Amount")
    

    @allure.step("Fill ICP Vendor merchant Purchase & Authorization form")
    def fill_ICP_form_Vndormerchant1(self,Venadgeid1, venserv1, venserv1Amount, VenAmount1, VenAmount2, VenAmount3):
        self.fill_by_xpath(HomeLocators.venADGEID1, Venadgeid1, description="Vendor Merchant Name")
        self.fill_by_xpath(HomeLocators.venserv1, venserv1, description="Vendor Service Name")
        self.fill_by_xpath(HomeLocators.venserv1Amount, venserv1Amount, description="Vendor Service Amount")
        self.fill_by_xpath(HomeLocators.vendynamicamount1, VenAmount1, description="Vendor Service Dynamic Amount1")
        self.fill_by_xpath(HomeLocators.vendynamicamount2, VenAmount2, description="Vendor Service Dynamic Amount2")
        self.fill_by_xpath(HomeLocators.vendynamicamount3, VenAmount3, description="Vendor Service Dynamic Amount3")

    @allure.step("Fill ICP Vendor merchant Purchase & Authorization form")
    def fill_ICP_form_Vndormerchant2(self,Venadgeid2, venserv2, venserv2Amount):
        self.fill_by_xpath(HomeLocators.venADGEID2, Venadgeid2, description="Vendor Merchant Name")
        self.fill_by_xpath(HomeLocators.venserv2, venserv2, description="Vendor Service Name")
        self.fill_by_xpath(HomeLocators.venserv2Amount, venserv2Amount, description="Vendor Service Amount")
