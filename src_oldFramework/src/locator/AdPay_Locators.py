# src/locators/payment_locators.py
import re
class AdPayLocators:

    Change_Text   = ("text", "Change")
    
    # Payment change option
    changepayment= '//a[@id="Change"]'
    selectpayment = '//div[@id="addNewCardOffcanvas"]'


# Add card modal
    Add_Heading   = ("role", "heading", {"name": "Add"})
    Name_Textbox  = ("role", "textbox", {"name": "Enter name"})
    Card_Textbox  = ("role", "textbox", {"name": "Enter card number"})
    CVV_Textbox   = ("role", "textbox", {"name": "***"})
    Month_Text    = ("text", "MM")
    Year_Text     = ("text", "YYYY")
    Email_Textbox = ("role", "textbox", {"name": "Enter Email Address"})
    Receipt='//*[@id="paymentoptionbody"]'
    select_Month='//*[@id="add-creditcard"]/div[4]/div[1]/div[1]/div[1]'
    select_Monthoption= '//*[@id="add-creditcard"]/div[4]/div[1]/div[1]/div[2]/div[12]'
    select_Year='//*[@id="add-creditcard"]/div[4]/div[2]/div[1]/div[1]'
    select_Yearoption='//*[@id="add-creditcard"]/div[4]/div[2]/div[1]/div[2]/div[4]'
    Buy_Button    = "payment"

# Payment confirmation for Card purchase 
    Payment_Pay_Button = '//*[@id="ConfirmPay"]'
    Payment_Change_Pay_Button='//*[@id="payment"]'
    Payment_Yes_Button =  '//*[@id="yesclick1"]/button'

    Confirm_Yes_Button = '//*[@id="yesclick2"]/button'
    Confirm_No_Button  = ("role", "button", {"name": re.compile(r"^no$",  re.IGNORECASE)})
    Receipt_Empty_Text = ("text", "Receipt email is empty")

# Comera Pay 
    comerapayselect    = '//div[@id="comerapayFav"]'
    Comerapay_Registered_Number = '//input[@id="comeraMobileNumber"]'
    Comerapay_RequestOTP = '//button[@id="comeraWalletSubmit"]'
    Comerapay_OTP = ("role", "textbox", {"button": "Request OTP"})
    Comerapay_OTP_validate="comeraotpffailed"
    Comerapay_OTP_validate = ("text", "Verification code sent") 
    Comerapay_OTP_Enter = ("role", "textbox", {"name": "Enter OTP"})
    Comerapay_Confirm_Button = '//button[@id="comeraPayAuth"]'

# Direct Debit option (UAEPGS)
    DirectDebit = '//div[text()="Direct Debit"]'
    click_direct_debit = '//div[text()="Direct Debit"]'
    select_banklist = '//select[@id="ddl_BanksList"]'
    select_banklist_option = "//select[@id='ddl_BanksList']/option[text()='{}']"
    select_productlist='//select[@id="ddl_ProductList"]'
    select_productlist_option='//select[@id="ddl_ProductList"]/option[text()="{}"]'
    click_submit = '//*[@name="btn_Submit"]'
    click_checkbox = '//*[@id="CheckBoxTerms"]'
    click_submit = '//*[@value="Submit"]'
   
# Fill details in simulator page
    ResponseCode = '//input[@name="pp_ResponseCode"]'
    ResponseMessage = '//input[@id="pp_ResponseMessage"]'
    AuthCode = '//input[@id="pp_AuthCode"]'
    BankID = '//input[@id="pp_BankID"]'
   
#Generate hash & Return to PG
    click_GenerateHash = '//*[@value="Generate Hash"]'
    click_ReturnToPG = '//*[@value="Return to PG"]'

# Locators for validating Dhiram symbol and amount 
    Dhiram_Symbol = "#symbolar"
    Dhiram_Symbol_AR="#symbolen"
    Adpay_ENSummary_page= "#SummaryEN"
    Adpay_ARSummary_page= "#SummaryAR"

# Negative Scenarios for Card validations:

    CardValidations="cardCaptchaMsg"
    cardnameValidations="cardNameMsg"
    CardExpValidations="cardExpMsg"
    CardYearValidations="cardYrMsg"
    CardCvvValidations="cardCvvMsg"

  #Assert validation:
    Inquiry_response='font[color="grey"]'
    Payment_response='td[style="word-break: break-word;"]'

#charity
    charity1_amt_5='//button[@id="charity5_1"]'
    charity1_amt_10='//button[@id="charity10_1"]'
    charity1_others='//div[@id="other_1"]'
    others1_amt='//input[@id="charityAmountCards_row_1"]'
    donation1_confirm='//input[@id="donationconfirm_1"]'
    charity2_amt_5='//button[@id="charity5_2"]'
    charity2_amt_10='//button[@id="charity10_2"]'
    charity2_others='//div[@id="other_2"]'
    others2_amt='//input[@id="charityAmountCards_row_2"]'
    donation2_confirm='//input[@id="donationconfirm_2"]'
    charity3_amt_5='//button[@id="charity5_3"]'
    charity3_amt_10='//button[@id="charity10_3"]'
    charity3_others='//div[@id="other_3"]'
    others3_amt='//input[@id="charityAmountCards_row_3"]'
    donation3_confirm='//input[@id="donationconfirm_3"]'

# Arabic Language locators in ADpay card
  
    Change_AR='//a[@id="ChangeAR"]'
    Add_newcard_AR='//h5[@id="add-new-card"]'
    Cardholdername_AR='//input[@id="cardholderName"]'
    Cardno_AR='//input[@name="cardNumber"]'
    Cardcvv_AR='//input[@id="cardCvv"]'

 # Locators for comerapay in Arabic language

    comerapayselect_AR='//div[text()="Comera Wallet"]'
    
# Locators for charity in Arabic language

    charity1_amt_5_AR='//button[@id="charity5AR_1"]'
    charity1_amt_10_AR='//button[@id="charity10AR_1"]'
    charity1_others_AR='//div[@id="otherAR_1"]'
    charity2_amt_5_AR='//button[@id="charity5AR_2"]'
    charity2_amt_10_AR='//button[@id="charity10AR_2"]'
    charity2_others_AR='//div[@id="otherAR_2"]'
    charity3_amt_5_AR='//button[@id="charity5AR_3"]'
    charity3_amt_10_AR='//button[@id="charity10AR_3"]'
    charity3_others_AR='//div[@id="otherAR_3"]'

 # Recurring Registration: 

    Recurring_saved_card='//input[@id="proceed"]'
    cancel_button='//input[@id="cancel"]'
    select_Mnth='//div[@id="ExpDate"]/div/div[1]/div/div[1]'
    select_Mnthoption= '//div[@id="ExpDate"]/div/div[1]/div/div[2]/div[8]'
    select_Yr='//div[@id="ExpDate"]/div/div[2]/div/div[1]'
    select_Yroption='//div[@id="ExpDate"]/div/div[2]/div/div[2]/div[3]'

# Saved Cards :

    saved_card_MC='//div[@cardkey="202417322764593"]'
    saved_card_MCcvv='//input[@id="savedcardCVV_5204-74**-****-1002"]'
    saved_card_amex='//div[@cardkey="202607686057208"]'
    saved_card_amexcvv='//input[@id="savedcardCVV_3791-87**-***-4105"]'
    saved_card_visa='//div[@cardkey="202504166662198"]'
    saved_card_visacvv='//input[@id="savedcardCVV_4012-00**-****-1112"]'
    saved_card_Jaywan='//div[@cardkey="202608488163239"]'
    saved_card_Jaywancvv='//input[@id="savedcardCVV_6690-09**-****-6376"]'
    Viewmore='//p[@id="viewmore"]'