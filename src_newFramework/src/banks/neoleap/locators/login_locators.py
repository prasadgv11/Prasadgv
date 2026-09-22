class NeoleapLoginLocators:
    class Admin:
        login_button = "//span[contains(text(),'Login')]"
        institution_field = "//input[@id='instId']"
        username_field = "input[name='userId']"
        password_field = "input[name='password']"
        submit_button = "input[name='sbutton']"
        otp_field = "#otpvalue"   # TODO: confirm real selector

    class Bank:
        institution_field = "input[name='instId']"
        username_field = "input[name='userId']"
        password_field = "input[name='password']"
        login_button = "button#login"
        otp_field = "#otpvalue"   # TODO: confirm real selector

    class Merchant:
        institution_name_field = "input[name='instId']"
        merchant_id_field = "input[name='merchantId']"
        username_field = "input[name='userId']"
        password_field = "input[name='password']"
        login_button = "button#login"
        otp_field = "#otpvalue"   # TODO: confirm real selector

    class SuperAdmin:
        username_field = "input[name='userId']"
        password_field = "input[name='password']"
        login_button = "button#login"
        otp_field = "#otpvalue"   # TODO: confirm real selector
