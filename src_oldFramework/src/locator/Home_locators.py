class HomeLocators:

# URL
    Demo_URL = "https://adapayuat.bankfab.com/PGRPTG/"

#Links for Payments instruments
    # Purchase_Link = ("role", "link", {"name": "Purchase", "exact": True})
    Purchase_Link = ("role", "link", {"name": "Purchase"})
    Refund_Link   = ("role", "link", {"name": "Refund", "exact": True})
    Void_Link     = ("role", "link", {"name": "Refund", "exact": True})
    Home_Link     = ("role", "link", {"name": "Home Page", "exact": True})
    Body = "body" 
    finalapibody="xpath=/html/body/table[2]/tbody/tr[1]/td/i"
   
                  

# Demo Page Locators  
    TID        = "#tid"
    Version    = "#version"
    ADGEID1    = "#adgeid1"
    Service11  = "#service11"
    Password   = "#pwd"
    CORID      = "#corid"
    InqType   = "#inqtype"
    Amount     = "#serAmnt11"
    Quantity   = "input[name='serQty11']"
    UDF1       = "input[name='UDF1']"
    Buy_Button = '//input[@type="Submit"]'
    UDF5_Select   = '//select[@name="udf5"]'
    UDF5_Select_Option = '//select[@name="udf5"]/option[text()="{}"]'
    Comment_Input = '//input[@name="comment"]' 
    Refund_Button = ("role", "button", {"name": "Refund"})
    Void_Button = ("role", "button", {"name": "Void"})
    udf11='//*[@id="UDF11"]'
    UDF12 = "input[name='UDF12']"
    select_endpoint='//select[@name="endpoint"]'
    select_project='//select[@name="path"]'
    select_project_option='//select[@name="path"]/option[5]'
    select_endpoint_option='//select[@name="endpoint"]/option[3]'
    Language = '//select[@id="langEnAr"]'
    Language_option = '//select[@id="langEnAr"]/option[text()="{}"]'
    HeaderVersion='//input[@id="headerVersion"]'
    refundId='//*[@id="text"]/input'
    EntityId='//input[@id="entityId"]'

### ICP Changes 

    
    dynamicamount1='//input[@id="amount11"]'
    dynamicamount2='//input[@id="amount12"]'
    dynamicamount3='//input[@id="amount13"]'
    service2='//input[@id="service12"]'
    serviceAmount2='//input[@id="serAmnt12"]'
    venADGEID1='//input[@id="adgeid2"]'
    venADGEID2='//input[@id="adgeid3"]'
    venserv1='//input[@id="service21"]'
    venserv1Amount='//input[@id="serAmnt21"]'
    venserv2='//input[@id="service31"]'
    venserv2Amount='//input[@id="serAmnt31"]'
    vendynamicamount1='//input[@id="amount21"]'
    vendynamicamount2='//input[@id="amount22"]'
    vendynamicamount3='//input[@id="amount23"]'




# Buy_Button = ("role", "button", {"name": "Buy"})

     # validation for demo page
    demopagevalidation="body"

#Demo resposne page locators:

    backtomerchat='/html/body/div/div/div[5]/button[1]'
    downloadreceipt='/html/body/div/div/div[5]/button[2]'


# Recurring ListCards:
    # Links for Recurring ListCards
    RecurringListCards_Link = ("role", "link", {"name": "Recurring ListCards"})
    
    
# Recurring Payment: 
    # Links for Recurring Payment
    RecurringPayment_Link = ("role", "link", {"name": "Recurring Payment"})
    RP_amount='//input[@id="amt"]'
    RP_udf1='//input[@name="UDF1"]'
    Recurringid="//label[contains(text(),'Recurring ID')]"
    Recurringidfill='//input[@id="recurringId"]'
    CardId_Value='/html/body/h4[1]/font[2]'
    CardId_Input='//input[@id="cardId"]'
    
# Finalization API:
    FinalizationAPI_Link = ("role", "link", {"name": "Finalization API"})
    FinalizationAPI_completion='//input[@id="paymentID"]'

# Supporting Transactions Assertion:

    Refund_Assert="xpath=/html/body/h4[1]/font[2]"
    Resultvisible = "#Result: "
    Inquiry_response='font[color="grey"]'