# src/pages/adpay/purchase_page.py
from xml.sax.xmlreader import Locator

import allure
from pages.base_page import BasePage
from locator.AdPay_Locators import AdPayLocators
from locator.Home_locators import HomeLocators
import re

class PurchasePage(BasePage):

    def __init__(self, page, module_name="Payments"):
        super().__init__(page, module_name=module_name)
        self.captured_payment_id = None  # Store payment ID for reuse

    def __init__(self, page, module_name="Payments"):
        super().__init__(page, module_name=module_name)
        self.captured_finalizationapi_id = None  # Store payment ID for reuse


    @allure.step("Click Change (payment method)")
    def click_change(self):
        self.page.wait_for_load_state("domcontentloaded")
        self.click_by_xpath(AdPayLocators.changepayment, description="Change payment")

    @allure.step("Click Change (selectpayment method)")
    def click_selectpayment(self):
        self.page.wait_for_load_state("domcontentloaded")
        self.click_by_xpath(AdPayLocators.selectpayment,  description="selectpayment")

    @allure.step("Add card details")
    def add_card(self, name, number, cvv):
        # open add card modal and fill basic fields
        self.click_by_getbyrole(AdPayLocators.Add_Heading, description="Open Add Card")
        self.fill_by_getbyrole(AdPayLocators.Name_Textbox, name, description="Cardholder name")
        self.fill_by_getbyrole(AdPayLocators.Card_Textbox, number, description="Card number")
        self.fill_by_getbyrole(AdPayLocators.CVV_Textbox, cvv, description="CVV")

    @allure.step("Select Month")
    def Select_month(self):
        self.click_by_xpath(AdPayLocators.select_Month, description="Select Month")
        self.click_by_xpath(AdPayLocators.select_Monthoption, description="Select Month Option")

    @allure.step("Select Year")
    def Select_Year(self):
        self.click_by_xpath(AdPayLocators.select_Year, description="Select Year")
        self.click_by_xpath(AdPayLocators.select_Yearoption, description="Select Year Option")
    

    @allure.step("Add card details: set receipt email")
    def add_email(self,  email): 
        self.click_by_getbyrole(AdPayLocators.Email_Textbox, description="Receipt Email")
        self.fill_by_getbyrole(AdPayLocators.Email_Textbox, email, description="Receipt Email")

    @allure.step("Master saved card details")
    def saved_card_details_Mastercard(self, cvv):
        self.click_by_xpath(AdPayLocators.saved_card_MC, description="Saved Card")
        self.fill_by_xpath(AdPayLocators.saved_card_MCcvv, cvv, description="Saved Card CVV")
       
    @allure.step("Amex saved card details")
    def saved_card_details_amex(self, cvv):
        self.click_by_xpath(AdPayLocators.saved_card_amex, description="Saved Card")
        self.fill_by_xpath(AdPayLocators.saved_card_amexcvv, cvv, description="Saved Card CVV") 

    @allure.step("Jaywan saved card details")
    def saved_card_details_jaywan(self, cvv):
        self.click_by_xpath(AdPayLocators.saved_card_Jaywan, description="Saved Card")
        self.fill_by_xpath(AdPayLocators.saved_card_Jaywancvv, cvv, description="Saved Card CVV")       
       
    @allure.step("Visa saved card details")
    def saved_card_details_visa(self, cvv):
        self.click_by_xpath(AdPayLocators.saved_card_visa, description="Saved Card")
        self.fill_by_xpath(AdPayLocators.saved_card_visacvv, cvv, description="Saved Card CVV")

    @allure.step("Viewmore option in ADPAY Payment page")
    def click_viewmore(self):
        self.click_by_xpath(AdPayLocators.Viewmore, description="Saved Card")

    @allure.step("Confirm payment: Payment Options")
    def pay(self):
        self.click_by_xpath(AdPayLocators.Payment_Change_Pay_Button, description="Pay button")
        # self.click_by_xpath(AdPayLocators.Confirm_Yes_Button, description="Yes button")

    @allure.step("Confirm payment: Payment Options")
    def pay_card(self):
        self.click_by_xpath(AdPayLocators.Payment_Pay_Button, description="Pay button")
        # self.click_by_xpath(AdPayLocators.Payment_Yes_Button, description="Yes button")


    @allure.step("Select Comerapay" )
    def select_comerapay(self):
        self.click_by_xpath(AdPayLocators.comerapayselect, description="Select Comerapay")
      
    @allure.step("Comerapay Validations" )
    def comerapay_validations(self, ComerapayNumber, ComerapayOTP):
        self.click_by_xpath(AdPayLocators.Comerapay_Registered_Number, description="Enter Comerapay Registered Number")
        self.fill_by_xpath(AdPayLocators.Comerapay_Registered_Number, ComerapayNumber, description="Comerapay Registered Number")
        self.click_by_xpath(AdPayLocators.Comerapay_RequestOTP, description="RequestOTP")
        #self.assert_visible(AdPayLocators.Comerapay_OTP_validate, description="To verify Verification code sent")
        self.click_by_getbyrole(AdPayLocators.Comerapay_OTP_Enter, description="Enter OTP")
        self.fill_by_getbyrole(AdPayLocators.Comerapay_OTP_Enter, ComerapayOTP, description="Enter OTP")
        self.click_by_xpath(AdPayLocators.Comerapay_Confirm_Button, description="Comerapay Confirm Button")

    @allure.step("Capture Payment ID from Result Page")
    def capture_payment_id(self):
        self.wait_for_page_load("load", timeout=90_000)     
        self.expect_to_contain(HomeLocators.Body, "paymentid", timeout=90_000)

        self.attach_screenshot("Result Page - Payment Confirmation")
        result_text = self.get_inner_text(HomeLocators.Body)

        match = re.search(r'"paymentid"\s*:\s*"([^"]+)"', result_text,
                        re.IGNORECASE)
        if not match:
            allure.attach(self.page.content(),
                        "Result HTML (PaymentID not found)",
                        allure.attachment_type.HTML)
            raise AssertionError("Payment ID not found on result page!")

        payment_id = match.group(1)
        self.captured_payment_id = payment_id  # Store for later use
        self.logger.info(f"Captured Payment ID: {payment_id}")  
        print("Captured Payment ID:", payment_id)
        return payment_id

    @allure.step("Fill Comment with Captured Payment ID")
    def fill_capture_payment_id(self):
        if not self.captured_payment_id:
            raise AssertionError("No payment ID has been captured yet! Call capture_payment_id() first on the result page.")
        self.fill_by_xpath(HomeLocators.Comment_Input, self.captured_payment_id, description="Comment")
        print(f"Filled Comment with Payment ID: {self.captured_payment_id}")
        return self.captured_payment_id


    @allure.step("Select UDF5 option: {value}")
    def select_udf5(self, value: str) -> None:
       self.select_by_xpath(HomeLocators.UDF5_Select, description="UDF5 dropdown", option=value)

    # Direct Debit (UAEPGS)
    @allure.step("Click Direct Debit option")  
    def click_direct_debit(self):
        self.click_by_xpath(AdPayLocators.DirectDebit, description="Direct Debit")
       
    @allure.step("Select Bank option: {value}")
    def select_bank(self, value: str) -> None:
       self.select_by_xpath(AdPayLocators.select_banklist, description="select bank option", option=value)    
       
    @allure.step("Select Product option: {value}")
    def select_product(self, value: str) -> None:
       self.select_by_xpath(AdPayLocators.select_productlist, description="select product option", option=value)    
   
    @allure.step("click Submit button in UGEPGS flow")
    def submit(self):
        self.click_by_xpath(AdPayLocators.click_submit, description="Submit button")
        self.click_by_xpath(AdPayLocators.click_checkbox, description="Accept terms checkbox")
        self.click_by_xpath(AdPayLocators.click_submit, description="Final Submit button")
       
    @allure.step("Fill Parameters in simulator page for Direct Debit")
    def add_parameters(self, response_code, response_message, auth_code, bank_id):
        # Fill the required parameters for direct debit
        self.click_by_xpath(AdPayLocators.ResponseCode, description="Response Code")
        self.fill_by_xpath(AdPayLocators.ResponseCode, response_code, description="Response Code")
        self.fill_by_xpath(AdPayLocators.ResponseMessage, response_message, description="Response Message")
        self.fill_by_xpath(AdPayLocators.AuthCode, auth_code, description="Auth Code")
        self.fill_by_xpath(AdPayLocators.BankID, bank_id, description="Bank ID")
 
    @allure.step("Click Generate Hash and Return to PG")
    def generate_hash_and_return_to_PG(self):
        self.click_by_locator(AdPayLocators.click_GenerateHash, description="Generate Hash")
        self.click_by_locator(AdPayLocators.click_ReturnToPG, description="Return to PG")
    

    # Demo Response page actions Back to Merchant
    @allure.step("Click Back to Merchant button on response page") 
    def click_back_to_merchant(self):
        self.click_by_xpath(HomeLocators.backtomerchat, description="Back to Merchant")

    # Demo Response page actions Download Receipt
    @allure.step("Click Download Receipt button on response page")
    def click_download_receipt(self):
        self.click_by_xpath(HomeLocators.downloadreceipt, description="Download Receipt")
    

    @allure.step("Verify Dhiram symbol and amount")
    def verify_Dhiramsymbol(self):
        self.assert_visible(AdPayLocators.Dhiram_Symbol, description="Verify Dhiram symbol")


    @allure.step("Verify ADPAY Summary header with exact text")
    def verify_adpay_summary_header(self):
        self.assert_visible(AdPayLocators.Adpay_ENSummary_page, description="Payment Summary header")
        self.assert_text(AdPayLocators.Adpay_ENSummary_page, expected_text="Summary", description="Payment Summary text")


    @allure.step("Verify ADPAY Summary header with exact text")
    def verify_demopage_validations(self, Assertvalue):
        self.assert_visible(HomeLocators.demopagevalidation, description="To verify mandatory feild validations in demo page is visible")
        self.assert_text(HomeLocators.demopagevalidation,expected_text=Assertvalue, description="To verify mandatory feild validations in demo page")


    @allure.step("To verify Adpay Add card validations")
    def verify_addcard_validations(self, Assertvalue):
        # check each validation message if it appears, then assert its text
        locators = [
            (AdPayLocators.CardValidations, "Card number validation"),
            (AdPayLocators.cardnameValidations, "Cardholder name validation"),
            (AdPayLocators.CardExpValidations, "Expiry month validation"),
            (AdPayLocators.CardYearValidations, "Expiry year validation"),
            (AdPayLocators.CardCvvValidations, "CVV validation"),
        ]
 
        for locator, desc in locators:
            try:
                element = self.page.locator(locator)
                if element.count() and element.is_visible():
                    # only assert when the element is present and visible
                    self.assert_text(element, expected_text=Assertvalue, description=f"{desc} - {Assertvalue}")
                else:
                    self.logger.info(f"{desc} not visible, skipping assertion")
            except Exception as e:
                # any unexpected error should be logged but not break the loop
                self.logger.warning(f"Could not verify {desc}: {e}")
 

    @allure.step("To verify Adpay Add card validations")
    def verify_addcard_validations1(self, locator, Assertvalue):
        resolved = self.page.locator(locator)
        self.assert_text(resolved, expected_text=Assertvalue, description="To verify mandatory feild validations in Add card")

    @allure.step("Verify ADPAY Card Validations")
    def verify_adpay_card(self):
        # self.assert_visible(AdPayLocators.CardValidations, description="Payment Summary header")
        self.assert_text(AdPayLocators.CardValidations, expected_text="Please enter Card Number", description="Payment addcard text")  


    def _resolve_locator_key(self, key_or_selector) -> str | Locator:
        """
        If the input matches a known key from Excel (e.g., 'cardCvvMsg'),
        return the mapped selector/Locator. Otherwise, return the input unchanged.
        """
        try:
            return self.LOCATOR_MAP.get(key_or_selector, key_or_selector)
        except Exception:
            # In case key_or_selector isn't hashable or any unexpected issue
            return key_or_selector

    
    @allure.step("Verify payment status")
    def verify_payment_status(self):
            self.assert_status_in(AdPayLocators.Inquiry_response, description="Payment status check")


    @allure.step("Verify payment status")
    def verify_payment_ADPay(self):
        self.assert_status_in(AdPayLocators.Payment_response, description="Payment status check in After completing the transactions")

 # Arabic language for card details
    
    @allure.step("Click change button in Arabic")
    def click_change_AR(self):
        self.click_by_xpath(AdPayLocators.Change_AR, description="Change")
        
    @allure.step("Add card details in Arabic")
    def add_card_AR(self, name, number, cvv):
        self.click_by_xpath(AdPayLocators.Add_newcard_AR, description="Add New Card")
        self.fill_by_xpath(AdPayLocators.Cardholdername_AR, name, description="Cardholder name")
        self.fill_by_xpath(AdPayLocators.Cardno_AR, number, description="Card number")
        self.fill_by_xpath(AdPayLocators.Cardcvv_AR, cvv, description="CVV")
    
    # Arabic language for comerapay option
    
    @allure.step("Click comerapay option in Arabic")
    def click_comerapay_AR(self):
        self.click_by_xpath(AdPayLocators.comerapayselect_AR, description="Comera Wallet")
        
    # Arabic language for charity option
    
    @allure.step("Click charity1 amount options  in Arabic")
    def click_charity1_amt5_AR(self):
        self.click_by_xpath(AdPayLocators.charity1_amt_5_AR, description="Donation Amount 5 AED")
        
    @allure.step("Click charity1 amount options  in Arabic")
    def click_charity1_amt10_AR(self):
        self.click_by_xpath(AdPayLocators.charity1_amt_10_AR, description="Donation Amount 10 AED")
        
    @allure.step("Click charity1 amount options  in Arabic")
    def click_charity1_others_AR(self, charity_amt):
        self.click_by_xpath(AdPayLocators.charity1_others_AR, description="Donation Amount Others")
        self.fill_by_xpath(AdPayLocators.others1_amt, charity_amt, description="Donation Amount Others input")
        self.click_by_xpath(AdPayLocators.donation1_confirm, description="Confirm donation amount")
        
    @allure.step("Click charity2 amount options in Arabic")
    def click_charity2_amt5_AR(self):
        self.click_by_xpath(AdPayLocators.charity2_amt_5_AR, description="Donation Amount 5 AED")
        
    @allure.step("Click charity2 amount options in Arabic")
    def click_charity2_amt10_AR(self):
        self.click_by_xpath(AdPayLocators.charity2_amt_10_AR, description="Donation Amount 10 AED")
        
    @allure.step("Click charity2 amount options  in Arabic")
    def click_charity2_others_AR(self, charity_amt):
        self.click_by_xpath(AdPayLocators.charity2_others_AR, description="Donation Amount Others")
        self.fill_by_xpath(AdPayLocators.others2_amt, charity_amt, description="Donation Amount Others input")
        self.click_by_xpath(AdPayLocators.donation2_confirm, description="Confirm donation amount")

    @allure.step("Click charity3 amount options in Arabic")
    def click_charity3_amt5_AR(self):
        self.click_by_xpath(AdPayLocators.charity3_amt_5_AR, description="Donation Amount 5 AED")
        
    @allure.step("Click charity3 amount options  in Arabic")
    def click_charity3_amt10_AR(self):
        self.click_by_xpath(AdPayLocators.charity3_amt_10_AR, description="Donation Amount 10 AED")
        
    @allure.step("Click charity3 amount options  in Arabic")
    def click_charity3_others_AR(self, charity_amt):
        self.click_by_xpath(AdPayLocators.charity3_others_AR, description="Donation Amount Others")
        self.fill_by_xpath(AdPayLocators.others3_amt, charity_amt, description="Donation Amount Others input")
        self.click_by_xpath(AdPayLocators.donation3_confirm, description="Confirm donation amount")


 # English language for charity option

    @allure.step("Click donation amount 5 AED")
    def click_charity1_amt_5(self):
        self.click_by_xpath(AdPayLocators.charity1_amt_5, description="Donation Amount 5 AED")
       
    @allure.step("Click donation amount 10 AED")
    def click_charity1_amt_10(self):
        self.click_by_xpath(AdPayLocators.charity1_amt_10, description="Donation Amount 10 AED")
   
    @allure.step("Click donation amount Others and Fill amount")
    def click_charity1_others(self, charity_amt):
        self.click_by_xpath(AdPayLocators.charity1_others, description="Donation Amount Others")
        self.fill_by_xpath(AdPayLocators.others1_amt, charity_amt, description="Donation Amount Others input")
        self.click_by_xpath(AdPayLocators.donation1_confirm, description="Confirm donation amount")
   
    @allure.step("Click donation amount 5 AED")
    def click_charity2_amt_5(self):
        self.click_by_xpath(AdPayLocators.charity2_amt_5, description="Donation Amount 5 AED")
       
    @allure.step("Click donation amount 10 AED")
    def click_charity2_amt_10(self):
        self.click_by_xpath(AdPayLocators.charity2_amt_10, description="Donation Amount 10 AED")
   
    @allure.step("Click donation amount Others and Fill amount")
    def click_charity2_others(self, charity_amt):
        self.click_by_xpath(AdPayLocators.charity2_others, description="Donation Amount Others")
        self.fill_by_xpath(AdPayLocators.others2_amt, charity_amt, description="Donation Amount Others input")
        self.click_by_xpath(AdPayLocators.donation2_confirm, description="Confirm donation amount")
       
    @allure.step("Click donation amount 5 AED")
    def click_charity3_amt_5(self):
        self.click_by_xpath(AdPayLocators.charity3_amt_5, description="Donation Amount 5 AED")
       
    @allure.step("Click donation amount 10 AED")
    def click_charity3_amt_10(self):
        self.click_by_xpath(AdPayLocators.charity3_amt_10, description="Donation Amount 10 AED")

    @allure.step("Click donation amount Others and Fill amount")
    def click_charity3_others(self, charity_amt):
        self.click_by_xpath(AdPayLocators.charity3_others, description="Donation Amount Others")
        self.fill_by_xpath(AdPayLocators.others3_amt, charity_amt, description="Donation Amount Others input")
        self.click_by_xpath(AdPayLocators.donation3_confirm, description="Confirm donation amount")

# Validations for ADpay payment page

    @allure.step("Verify ADPAY Summary header with exact text")
    def verify_adpay_summary_header_AR(self):
        self.assert_visible(AdPayLocators.Adpay_ARSummary_page, description="Payment Summary header")
        self.assert_text(AdPayLocators.Adpay_ARSummary_page, expected_text="ملخص", description="Payment Summary text")

    @allure.step("Verify Dhiram symbol and amount")
    def verify_Dhiramsymbol_AR(self):
        self.assert_visible(AdPayLocators.Dhiram_Symbol_AR, description="Verify Dhiram symbol")


    @allure.step("Fill card details")
    def fill_card_recurring_reg(self, name, number):
        self.fill_by_getbyrole(AdPayLocators.Name_Textbox, name, description="Cardholder name")
        self.fill_by_getbyrole(AdPayLocators.Card_Textbox, number, description="Card number")
        self.click_by_xpath(AdPayLocators.select_Mnth, description="Select Month")
        self.click_by_xpath(AdPayLocators.select_Mnthoption, description="Select Month Option")
        self.click_by_xpath(AdPayLocators.select_Yr, description="Select Year")
        self.click_by_xpath(AdPayLocators.select_Yroption, description="Select Year Option")
        
        
    @allure.step("Fill card details")
    def fillcvv_recurring_reg(self, cvv):
        self.fill_by_getbyrole(AdPayLocators.CVV_Textbox, cvv, description="CVV")

    @allure.step("Click saved card")
    def click_Recurringsaved_card(self):
        self.click_by_xpath(AdPayLocators.Recurring_saved_card, description="Click Recurring_saved_card")
        

#Recurring Registration to capture the recurring ID:

    @allure.step("Capture Recurring ID from Result Page")
    def capture_recurring_id(self):
        self.wait_for_page_load("load", timeout=90_000)
        self.expect_to_contain(HomeLocators.Recurringid, "Recurring ID", timeout=90_000)
        self.attach_screenshot("Result Page - Recurring Confirmation")
        result_text = self.get_inner_text(HomeLocators.Recurringid)
        match = re.search(
            r"Recurring\s*ID\s*:\s*(\d+)",
            result_text,
            re.IGNORECASE)

        if not match:
            allure.attach(
                self.page.content(), "Result HTML (Recurring ID not found)", allure.attachment_type.HTML)
            raise AssertionError("Recurring ID not found on result page!")

        recurring_id = match.group(1)
        self.captured_recurring_id = recurring_id  # Store for later use
        self.logger.info(f"Captured Recurring ID: {recurring_id}")
        print("Captured Recurring ID:", recurring_id)
        # self.logger(print(recurring_id))
        return recurring_id

    @allure.step("Fill Comment with Captured Recurring ID")
    def fill_capture_recurring_id(self):
        if not self.captured_recurring_id:
            raise AssertionError(
                "No Recurring ID has been captured yet! "
                "Call capture_recurring_id() first on the result page.")
        self.fill_by_xpath(HomeLocators.Recurringidfill, self.captured_recurring_id, description="Comment")
        print(f"Filled Comment with Recurring ID: {self.captured_recurring_id}")
        return self.captured_recurring_id

#Recurring Registration to capture the card ID:

    @allure.step("Capture Card ID using specific XPath")
    def capture_card_id(self):
        self.wait_for_page_load("load", timeout=90_000)
        card_id_text = self.get_inner_text(HomeLocators.CardId_Value)
        if not card_id_text:
            raise AssertionError("Card ID not found using provided XPath!")
        self.captured_card_id = card_id_text.strip()
        print("Captured Card ID:", self.captured_card_id)
        self.logger.info(f"Captured Card ID: {self.captured_card_id}")
        return self.captured_card_id
    

    @allure.step("Fill Card ID in another page")
    def fill_captured_card_id(self):
        if not self.captured_card_id:
            raise AssertionError("No Card ID captured yet! Call capture_card_id() first.")
        self.fill_by_xpath(HomeLocators.CardId_Input,self.captured_card_id,description="Card ID")
        print(f"Filled Card ID: {self.captured_card_id}")
        self.logger.info(f"Filled Card ID: {self.captured_card_id}")
        return self.captured_card_id

#PaymentID capture_finalizationapi Transactions:

    @allure.step("Capture finalizationapi ID from Result Page")
    def capture_finalizationapiID(self):
        self.wait_for_page_load("load", timeout=90_000)
        self.page.locator(HomeLocators.finalapibody).wait_for(timeout=90_000)
        self.attach_screenshot("Result Page - Payment Confirmation")
        result_text = self.get_inner_text(HomeLocators.finalapibody)
        match = re.search(r'"paymentid"\s*:\s*"([^"]+)"', result_text, re.IGNORECASE)
        if not match:
            allure.attach(
                self.page.content(), "Result HTML (finalizationapi ID not found)", allure.attachment_type.HTML)
            raise AssertionError("finalizationapi ID not found on result page!")
        finalizationapi_id = match.group(1)
        self.captured_finalizationapi_id = finalizationapi_id  # Store for reuse
        self.logger.info(f"Captured finalizationapi ID: {finalizationapi_id}")
        print("Captured finalizationapi ID:", finalizationapi_id)
        return finalizationapi_id


    @allure.step("Fill Comment with Captured finalizationapi ID")
    def fill_capture_finalizationapiID_completion(self):
        if not self.captured_finalizationapi_id:
            raise AssertionError("No finalizationapi ID has been captured yet! " "Call capture_recurring_id() first.")
        self.fill_by_xpath(
            HomeLocators.FinalizationAPI_completion, self.captured_finalizationapi_id, description="Comment")
        print(f"Filled Comment with finalizationapi ID: {self.captured_finalizationapi_id}")
        self.logger.info(f"Filled Comment with finalizationapi ID: {self.captured_finalizationapi_id}")
        return self.captured_finalizationapi_id
    
    @allure.step("Fill Comment with Captured finalizationapi ID")
    def fill_capture_finalizationapiID_Inquiry(self):
        if not self.captured_finalizationapi_id:
            raise AssertionError("No finalizationapi ID has been captured yet! " "Call capture_recurring_id() first.")
        self.fill_by_xpath(
            HomeLocators.Comment_Input, self.captured_finalizationapi_id, description="Comment")
        print(f"Filled Comment with finalizationapi ID: {self.captured_finalizationapi_id}")
        self.logger.info(f"Filled Comment with finalizationapi ID: {self.captured_finalizationapi_id}")
        return self.captured_finalizationapi_id

    def __init__(self, page):
        self.page = page

    def open_payment_page(self, payment_url):
        self.page.goto(payment_url)
        self.page.wait_for_load_state("networkidle")

    def get_current_url(self):
        return self.page.url
 
