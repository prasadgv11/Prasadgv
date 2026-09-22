class EcentricLoginLocators:
    class Bank:
        username_field = "//span[text()='User Name']"     # TODO: confirm real selector
        password_field = "//span[normalize-space()='Password']"      # TODO: confirm real selector
        captcha_field = "//mat-form-field[@id='captcha']//input"
        captcha_image = "//cl-captcha-input[@id='captcha']//span[contains(@class,'font-bold')]"
        captcha_error = "//mat-error[contains(text(),'CAPTCHA does not match')]"
        captcha_refresh = "//button[.//mat-icon[@data-mat-icon-name='arrow-path']]"
        login_button = "//button[normalize-space()='Login']"
        dashboard_marker = "#dashboard"                 # TODO: confirm real selector
        welcome_message = "#welcome-msg"                # TODO: confirm real selector
        error_message = "#error-msg"                    # TODO: confirm real selector
        locked_message = "#locked-msg"                  # TODO: confirm real selector
        login_msg="//mat-label[normalize-space(text())='User logged in successfully']"  

    class Merchant:
        username_field = "//input[@type='text']"     # TODO: confirm real selector
        password_field = "//input[@type='password']"      # TODO: confirm real selector
        captcha_field = "//mat-form-field[@id='captcha']//input"
        captcha_image = "//cl-captcha-input[@id='captcha']//span[contains(@class,'font-bold')]"
        captcha_error = "//mat-error[contains(text(),'CAPTCHA does not match')]"
        captcha_refresh = "//button[.//mat-icon[@data-mat-icon-name='arrow-path']]"
        login_button = "//button[normalize-space()='Login']"
        dashboard_marker = "#dashboard"                 # TODO: confirm real selector
        welcome_message = "#welcome-msg"                # TODO: confirm real selector
        error_message = "#error-msg"                    # TODO: confirm real selector
        locked_message = "#locked-msg"                  # TODO: confirm real selector
