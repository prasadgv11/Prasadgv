class WioCurrencyLocators:
    # Navigation
    menu_configuration = "//span[text()='Configuration']"
    menu_currency = "//span[text()='Currency']"
    
    # Currency list page
    add_button = "//button[text()='Add']"
    
    # Add Currency form
    currency_code_input = "//input[@placeholder='Currency Code']"
    currency_description_input = "//input[@placeholder='Currency Description']"
    minor_digits_input = "//input[@placeholder='Minor Digits']"
    currency_symbol_input = "//input[@placeholder='Currency Symbol']"
    save_button = "//button[text()='Save']"
    cancel_button = "//button[text()='Cancel']"
    message_container = "//div[contains(@class, 'alert')]"
    add_currency_page_title = "//h1[text()='Add Currency']"
    
    # Currency list page for View/Edit/ChangeStatus
    # Dynamic row locator template (to be formatted with currency_code)
    row_template = "//tr[td[contains(normalize-space(text()),'{currency_code}')]]"
    view_button = row_template + "//a[text()='View']"
    edit_button = row_template + "//a[text()='Edit']"
    checkbox = row_template + "//input[@type='checkbox']"
    change_status_button = "//button[text()='Change Status']"
    
    # View Currency page
    view_currency_code = "//span[@data-testid='view-currency-code']"
    view_currency_description = "//span[@data-testid='view-currency-description']"
    view_minor_digits = "//span[@data-testid='view-minor-digits']"
    view_currency_symbol = "//span[@data-testid='view-currency-symbol']"
    view_status = "//span[@data-testid='view-status']"
    back_button = "//button[text()='Back']"
    
    # Edit Currency page (same fields as Add, but Currency Code may be read-only)
    # We reuse the same input locators from Add form
    # Note: Currency Code field might be read-only, so we avoid filling it in edit action
