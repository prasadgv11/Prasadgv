class PinelabsLoginLocators:
    class Admin:
        username_field = "#adminUsername"
        password_field = "#adminPassword"
        login_button = "#adminLoginBtn"
        error_message = "#adminLoginError"
        dashboard_marker = "#adminDashboard"

    class Bank:
        institution_field = "input[name='instId']"
        username_field = "input[name='userId']"
        password_field = "input[name='password']"
        login_button = "button#login"
        error_message = "#bankLoginError"
        dashboard_marker = "#bankDashboard"

    class Merchant:
        institution_name_field = "input[name='instId']"
        merchant_id_field = "input[name='merchantId']"
        username_field = "input[name='userId']"
        password_field = "input[name='password']"
        login_button = "button#login"
        error_message = "#merchantLoginError"
        dashboard_marker = "#merchantDashboard"
