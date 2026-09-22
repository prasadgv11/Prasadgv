class WioLoginLocators:
    class Admin:
        login_button ="//span[text()='Login']"
        username_field ="input[id='adminuserId']"
        password_field ="input[id='adminpassword']"
        submit_button ="input[value='Submit']"
        dashboard_marker ="//li[contains(text(),'Welcome')]"
        logout_button="//span[text()='Logout']"
 
    class Bank:
        login_button="//span[text()='Login']"
        username_field = "input[id='instuserId']"
        password_field = "input[id='instpassword']"
        submit_button = "input[value='Submit']"
        dashboard_marker = "//li[contains(text(),'Welcome')]"
        logout_button="//span[text()='Logout']"
