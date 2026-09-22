# src/pages/adpay/purchase_page.py
import re

import allure
from locator.Home_locators import HomeLocators
from pages.base_page import BasePage
from locator.MPay_Locators import MPayLocators

class PurchasePage(BasePage):

    def __init__(self, page, module_name="Payments"):
        super().__init__(page, module_name=module_name)
        self.captured_payment_id = None  # Store payment ID for reuse

    def __init__(self, page, module_name="Payments"):
        super().__init__(page, module_name=module_name)
        self.captured_recurring_id = None  # Store recurring_id for reuse

    
    # click new card option in MPAY flow
    @allure.step("Click New Card in MPAY flow")
    def click_newcard(self):
        self.click_by_xpath(MPayLocators.click_newcard, description="Click New Card in MPAY flow")

    
      # fill card details in MPAY flow
    @allure.step("Fill card details in MPAY flow")
    def fill_card_details(self, name, number, cvv):
        self.fill_by_xpath(MPayLocators.cardholder_name, name, description="Cardholder Name")
        self.fill_by_xpath(MPayLocators.card_number, number, description="Card Number")
        self.fill_by_xpath(MPayLocators.cvv, cvv, description="CVV")

      # add month & year for card purchase in MPAY flow
    @allure.step("Select month option: {value}")
    def select_MM(self, value: str) -> None:
       self.select_by_xpath(MPayLocators.select_MM, description="select month option", option=value)

    @allure.step("Select year option: {value}")
    def select_YYYY(self, value: str) -> None:
       self.select_by_xpath(MPayLocators.select_YYYY, description="select year option", option=value)

    # MPAY locators-->UAEPGS purchase   
    # click direct debit option in MPAY flow
    @allure.step("Click Direct Debit option in MPAY flow")
    def click_uaepgs(self):
        self.click_by_xpath(MPayLocators.click_uaepgs, description="Direct Debit option in MPAY flow")

    @allure.step("Click tabby button")
    def select_uaepgspayment(self):
        self.select_radio_button(MPayLocators.click_uaepgs, description="select UAEPGS")

    # MPAY locators-->Tabby purchase   
    # click Tabby option in MPAY flow
    @allure.step("Click tabby button")
    def select_tabby(self):
        self.click_by_xpath(MPayLocators.click_tabby, description="click Tabby")

    @allure.step("Click tabby button")
    def select_tabbypayment(self):
        self.select_radio_button(MPayLocators.Radio_tabby, description="click Tabby")

    @allure.step("Fill receipt email")    
    def fill_receipt_email(self, receipt_email):
        self.fill_by_locator(MPayLocators.receipt_email, receipt_email, description="receipt email")
   
    @allure.step("Click pay button")
    def click_Mpay(self):
        self.click_by_xpath(MPayLocators.click_pay, description="Pay button")
       
    @allure.step("Fill tabby email")
    def fill_tabby_email(self, email, otp):
      
        # self.click_by_xpath(MPayLocators.email, description="Click Tabby email")
        self.fill_by_xpath(MPayLocators.email, email, description="Tabby email")
        self.click_by_xpath(MPayLocators.click_continue, description="Continue button")
        self.fill_by_xpath(MPayLocators.otp, otp, description="OTP")
       
    @allure.step("continue button")
    def accept_continue_button(self):

        self.check_checkbox(MPayLocators.check_box, description="Accept terms checkbox")
        self.click_by_xpath(MPayLocators.click_continue, description="Continue button")
   
    @allure.step("click no of payments options")
    def no_of_emi_payments(self):
        self.click_by_xpath(MPayLocators.no_of_payments, description="No of payments")
        self.click_by_xpath(MPayLocators.click_continue_emi, description="Continue EMI button")

    @allure.step("Click charity checkbox")
    def click_charity_checkbox(self, charity_amt):
        self.click_by_xpath(MPayLocators.Mpaycharity1, description="Click Charity Checkbox")
        self.fill_by_xpath(MPayLocators.Mpaycharity1_amt, charity_amt, description="Charity Amount")
        
    # saved card mpay
    @allure.step("Click saved card option in MPAY flow")
    def click_saved_Mastercard(self, sc_cvv):
        self.click_by_xpath(MPayLocators.click_savedcard, description="Click saved card in MPAY")
        self.fill_by_xpath(MPayLocators.saved_card_cvv, sc_cvv, description="CVV for saved card")


    @allure.step("Select Bank option: {value}")
    def select_bank(self, value: str) -> None:
       self.select_by_xpath(MPayLocators.select_banklist, description="select bank option", option=value)    
       
    @allure.step("Select Product option: {value}")
    def select_product(self, value: str) -> None:
       self.select_by_xpath(MPayLocators.select_productlist, description="select product option", option=value)    
   
    @allure.step("click Submit button in UGEPGS flow")
    def submit(self):
        self.click_by_xpath(MPayLocators.click_submit, description="Submit button")
        self.click_by_xpath(MPayLocators.click_checkbox, description="Accept terms checkbox")
        self.click_by_xpath(MPayLocators.click_submit, description="Final Submit button")
       
    @allure.step("Fill Parameters in simulator page for Direct Debit")
    def add_parameters(self, response_code, response_message, auth_code, bank_id):
        # Fill the required parameters for direct debit
        self.click_by_xpath(MPayLocators.ResponseCode, description="Response Code")
        self.fill_by_xpath(MPayLocators.ResponseCode, response_code, description="Response Code")
        self.fill_by_xpath(MPayLocators.ResponseMessage, response_message, description="Response Message")
        self.fill_by_xpath(MPayLocators.AuthCode, auth_code, description="Auth Code")
        self.fill_by_xpath(MPayLocators.BankID, bank_id, description="Bank ID")
 
    @allure.step("Click Generate Hash and Return to PG")
    def generate_hash_and_return_to_PG(self):
        self.click_by_locator(MPayLocators.click_GenerateHash, description="Generate Hash")
        self.click_by_locator(MPayLocators.click_ReturnToPG, description="Return to PG")
        

    @allure.step("Click Back to Merchant button on response page") 
    def click_back_to_merchant(self):
        self.click_by_xpath(HomeLocators.backtomerchat, description="Back to Merchant")

    # Demo Response page actions Download Receipt
    @allure.step("Click Download Receipt button on response page")
    def click_download_receipt(self):
        self.click_by_xpath(HomeLocators.downloadreceipt, description="Download Receipt")


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


    @allure.step("Verify payment status")
    def verify_payment_Mpay(self):
        self.assert_status_in(MPayLocators.Payment_response, description="Payment status check in After completing the transactions")

    @allure.step("Verify payment status")
    def verify_payment_status_Mpay(self):
            self.assert_status_in(MPayLocators.Inquiry_response, description="Payment status check")

 # Arabic Language charity options in MPAY flow
    @allure.step("Click charity1 checkbox & fill amount in Arabic language")
    def click_charity1_checkbox_AR(self, charity_amt):
        self.click_by_xpath(MPayLocators.charity1_checkbox_AR, description="Click Charity1 Checkbox in Arabic language")
        self.fill_by_xpath(MPayLocators.charity1_amt_AR, charity_amt, description="Charity1 Amount in Arabic language")
        
    @allure.step("Click charity2 checkbox & fill amount in Arabic language")
    def click_charity2_checkbox_AR(self, charity_amt):
        self.click_by_xpath(MPayLocators.charity2_checkbox_AR, description="Click Charity2 Checkbox in Arabic language")
        self.fill_by_xpath(MPayLocators.charity2_amt_AR, charity_amt, description="Charity2 Amount in Arabic language")
        
    @allure.step("Click charity3 checkbox & fill amount in Arabic language")
    def click_charity3_checkbox_AR(self, charity_amt):
        self.click_by_xpath(MPayLocators.charity3_checkbox_AR, description="Click Charity3 Checkbox in Arabic language")
        self.fill_by_xpath(MPayLocators.charity3_amt_AR, charity_amt, description="Charity3 Amount in Arabic language")
        
    # Arabic language locators for Tabby in MPAY flow
    @allure.step("Fill tabby email")
    def fill_tabby_emailcontinue_AR(self, Tabbyemail, otp):
        self.fill_by_xpath(MPayLocators.email, Tabbyemail, description="Tabby email")
        self.click_by_xpath(MPayLocators.tabby_continue_AR, description="Continue button")
        self.fill_by_xpath(MPayLocators.otp, otp, description="OTP")
        self.click_by_xpath(MPayLocators.otp_continue_AR, description="Continue button after entering OTP")
    
    @allure.step("click no of payments options")
    def no_of_emi_payments_AR(self):
        self.click_by_xpath(MPayLocators.no_of_payments, description="No of payments")
        self.click_by_xpath(MPayLocators.final_continue_AR, description="Continue EMI button")
    
#Recurring Registration Transactions:

    @allure.step("Fill card details in MPAY flow")
    def fill_recurringcard_details(self, name, number):
        self.fill_by_xpath(MPayLocators.recurring_cardname, name, description="Cardholder Name")
        self.fill_by_xpath(MPayLocators.recurring_number, number, description="Card Number")

    @allure.step("Select month option: {value}")
    def select_Month_recurring(self, value: str) -> None:
       self.select_by_xpath(MPayLocators.recurring_select_MM, description="select Recurring month option", option=value)

    @allure.step("Select year option: {value}")
    def select_Year_recurring(self, value: str) -> None:
       self.select_by_xpath(MPayLocators.recurring_select_YYYY, description="select Recurring year option", option=value)


    @allure.step("Fill card details")
    def fillcvv_recurring_reg(self, cvv):
        self.fill_by_xpath(MPayLocators.recurring_cvv, cvv, description="cvv")

    @allure.step("Click saved card")
    def click_recurringsaved_card(self):
        self.click_by_xpath(MPayLocators.Recurring_saved_card, description="Click Recurring_saved_card")

#Recurring Registration to capture the recurring ID:

    
    @allure.step("Capture Recurring ID from Result Page")
    def capture_recurring_id(self):
        self.wait_for_page_load("load", timeout=90_000)
        self.page.locator(HomeLocators.finalapibody).wait_for(timeout=90_000)
        self.attach_screenshot("Result Page - Payment Confirmation")
        result_text = self.get_inner_text(HomeLocators.finalapibody)
        match = re.search(r'"recurringID"\s*:\s*"([^"]+)"', result_text, re.IGNORECASE)
        if not match:
            allure.attach(
                self.page.content(), "Result HTML (Recurring ID not found)", allure.attachment_type.HTML)
            raise AssertionError("Recurring ID not found on result page!")
        recurring_id = match.group(1)
        self.captured_recurring_id = recurring_id  # Store for reuse
        self.logger.info(f"Captured Recurring ID: {recurring_id}")
        print("Captured Recurring ID:", recurring_id)
        return recurring_id


    @allure.step("Fill Comment with Captured Recurring ID")
    def fill_capture_recurring_id(self):
        if not self.captured_recurring_id:
            raise AssertionError("No Recurring ID has been captured yet! " "Call capture_recurring_id() first.")
        self.fill_by_xpath(
            HomeLocators.Recurringidfill, self.captured_recurring_id, description="Comment")
        print(f"Filled Comment with Recurring ID: {self.captured_recurring_id}")
        self.logger.info(f"Filled Comment with Recurring ID: {self.captured_recurring_id}")
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