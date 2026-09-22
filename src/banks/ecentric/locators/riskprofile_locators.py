class RiskprofileLocators:
    # Menu navigation
    menu_administration = "//span[text()='Administration']"
    menu_risk_setup = "//span[text()='Risk setup']"
    menu_pg = "//span[text()='PG']"
    tab_risk_profile = "//span[text()='Risk profile']"
    
    # Buttons
    button_add = "//button[text()='Add']"
    button_save = "//button[text()='Save']"
    button_search = "//button[text()='Search']"
    
    # Form fields
    input_risk_profile_name = "//input[@placeholder='Enter risk profile name']"
    dropdown_currency_code = "//mat-select[@placeholder='Currency code']"
    
    # Radio groups and toggles
    radio_profile_international_transaction_no = "//mat-radio-button[@value='No']//label[text()='No']"
    toggle_terminal_domestic_daily = "//mat-slide-toggle[@formcontrolname='terminalDomesticDailyToggle']//label"
    toggle_terminal_domestic_weekly = "//mat-slide-toggle[@formcontrolname='terminalDomesticWeeklyToggle']//label"
    toggle_terminal_domestic_monthly = "//mat-slide-toggle[@formcontrolname='terminalDomesticMonthlyToggle']//label"
    input_terminal_domestic_daily_count = "//input[@formcontrolname='terminalDomesticDailyCount']"
    input_terminal_domestic_weekly_count = "//input[@formcontrolname='terminalDomesticWeeklyCount']"
    input_terminal_domestic_monthly_count = "//input[@formcontrolname='terminalDomesticMonthlyCount']"
    toggle_cumulative_transaction_amount_daily = "//mat-slide-toggle[@formcontrolname='cumulativeTransactionAmountDailyToggle']//label"
    toggle_cumulative_refund_amount_daily = "//mat-slide-toggle[@formcontrolname='cumulativeRefundAmountDailyToggle']//label"
    radio_terminal_actions_terminal_blocking = "//mat-radio-button[@value='TerminalBlocking']//label[text()='Terminal blocking']"
    input_transaction_amount_min = "//input[@formcontrolname='transactionAmountMin']"
    input_transaction_amount_max = "//input[@formcontrolname='transactionAmountMax']"
    toggle_user_domestic_daily = "//mat-slide-toggle[@formcontrolname='userDomesticDailyToggle']//label"
    radio_user_actions_card_blocking = "//mat-radio-button[@value='CardBlocking']//label[text()='Card blocking']"
    toggle_ip_domestic_daily = "//mat-slide-toggle[@formcontrolname='ipDomesticDailyToggle']//label"
    radio_ip_actions_ip_blocking = "//mat-radio-button[@value='IPBlocking']//label[text()='IP blocking']"
    
    # Search form fields
    input_search_risk_profile_name_currency = "//input[@placeholder='Enter risk profile name/Currency']"
    dropdown_search_mode = "//mat-select[@placeholder='Mode']"
    
    # Message containers
    message_success = "//div[contains(@class,'success-message')]"
    message_error = "//div[contains(@class,'error-message')]"
    message_no_records = "//div[contains(text(),'No records found')]"
