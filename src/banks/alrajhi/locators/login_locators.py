class AlrajhiLoginLocators:
    class Admin:
        username_field = "#adminuserId"
        password_field = "#adminpassword"
        login_button = "//li[@class='login']"
        submit_button = "//input[@value='Submit']"
        error_message = "#adminLoginError"
        dashboard_marker = "#adminDashboard"
        otp_field = "#otpvalue"   # TODO: confirm real selector
        verify_button = "#verify"  # TODO: confirm real selector

    class Bank:
        institution_field = "//input[@id='instId']"
        username_field = "//input[@id='instuserId']"
        password_field = "//input[@id='instpassword']"
        login_button = "//li[@class='login']"
        submit_button = "//input[@value='Submit']"
        error_message = "#bankLoginError"
        dashboard_marker = "#bankDashboard"
        otp_field = "#otpvalue"
        verify_button = "#verify"   # TODO: confirm real selector

    class Merchant:
        institution_name_field = "input[name='instId']"
        merchant_id_field = "#mrchId"
        username_field = "input[name='userId']"
        password_field = "input[name='password']"
        login_button = "input[id='sbutton']"
        error_message = "#merchantLoginError"
        dashboard_marker = "#merchantDashboard"
        otp_field = "#otpvalue"   # TODO: confirm real selector
        verify_button = "//button[normalize-space()='Verify']"  # TODO: confirm real selector