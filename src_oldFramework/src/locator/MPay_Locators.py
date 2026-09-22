class MPayLocators:

    # Payment options group:

    click_tabby='//label[@id="PaymentpageTranoptions"][@for="tabby_inst"]'
    Radio_tabby='//label[@id="PaymentpageTranoptions"][@for="tabby_inst"]'
    click_uaepgs='//label[text()="Direct Debit"]'
    click_pay= '//input[@id="proceed"]'
    receipt_email='//*[@id="email"]'

     # Mpay locators-->Card purchase
    click_newcard='//div[@id="RegNewCard"]'
    cardholder_name='//input[@name="cardholderName"]'
    card_number='//input[@name="cardNumber"]'
    cvv='//input[@id="cardCvv"]'
    select_MM='//select[@id="ExpMonthSelect"]'
    select_MM_option='//select[@id="ExpMonthSelect"]/option[text()="{}"]'
    select_YYYY='//select[@id="ExpYearSelect"]'
    select_YYYY_option='//select[@id="ExpYearSelect"]/option[text()="{}"]'
    Mpaycharity1='//*[@id="charity_pay"]/div[1]/div[1]/div/label/div'
    Mpaycharity2='//*[@id="charity_pay"]/div[2]/div[1]/div/label/div'
    Mpaycharity3 ='//*[@id="charity_pay"]/div[3]/div[1]/div/label/div'
    Mpaycharity1_amt='//input[@id="charityAmountCards_row_1"]'
    
    # saved card locators Mpay

    click_savedcard='//div[@cardkey="202417370959348"][@id="EN_2_5204-74**-****-1002"]'
    saved_card_cvv='//input[@id="EN_savedcardCVV_5204-74**-****-1002"]'

    # Tabby locators:

    email='//input[@name="email"]'
    click_continue='//span[text()="Continue"]'
    otp='//*[@name="otp-code"]'
    check_box='//input[@id="checkAll"]'
    no_of_payments='//div[@data-test="payment-plans.installments-item"][4]'
    click_continue_emi='//span[text()="Continue"]'

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
    ResponseCode = '//input[@name="pp_ResponseCode"]'
    ResponseMessage = '//input[@id="pp_ResponseMessage"]'
    AuthCode = '//input[@id="pp_AuthCode"]'
    BankID = '//input[@id="pp_BankID"]'
    click_GenerateHash = '//*[@value="Generate Hash"]'
    click_ReturnToPG = '//*[@value="Return to PG"]'


      #Assert validation:
    Inquiry_response='font[color="grey"]'
    Payment_response='td[style="word-break: break-word;"]'


    # Arabic Language charity locators in MPAY 
    charity1_checkbox_AR='//div[@id="charity_pay_AR"]/div[1]/div[1]/label/div/div'
    charity1_amt_AR='//input[@id="charityAmountCards_AR_row_1"]'
    charity2_checkbox_AR='//div[@id="charity_pay_AR"]/div[2]/div[1]/label/div/div'
    charity2_amt_AR='//input[@id="charityAmountCards_AR_row_2"]'
    charity3_checkbox_AR='//div[@id="charity_pay_AR"]/div[3]/div[1]/label/div/div'
    charity3_amt_AR='//input[@id="charityAmountCards_AR_row_3"]'
    
    # Arabic language locators for Tabby in MPAY flow
    tabby_continue_AR='//button[@data-test="loginForm.continue"]'
    otp_continue_AR='//button[@data-test="button"]'
    final_continue_AR='//button[@data-test="payment-plans.continue"]'


  # Recurring Registration Card Details:
    recurring_cardname='//input[@id="EN_cardholderName"]'
    recurring_number='//input[@id="EN_cardNumber"]'
    recurring_cvv='//input[@id="EN_cardCvv"]'
    recurring_select_MM='//select[@id="EN_ExpMonthSelect"]'
    recurring_select_MM_option='//select[@id="EN_ExpMonthSelect"]/option[text()="{}"]'
    recurring_select_YYYY='//select[@id="EN_ExpYearSelect"]'
    recurring_select_YYYY_option='//select[@id="EN_ExpYearSelect"]/option[text()="{}"]'

    Recurring_saved_card='//input[@id="proceed"]'
    
