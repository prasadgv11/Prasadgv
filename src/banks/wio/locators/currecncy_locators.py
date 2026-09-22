class CurrecncyLocators:
    # Navigation locators (using precomputed XPath values)
    configuration_menu = "//span[contains(text(),'Configuration&nbsp;&nbsp;')]"
    currency_submenu = "//span[contains(text(),'Currency')]"
    
    # Currency list page locators
    add_button = "#TODO-verify-add-button-locator"  # Replace with actual locator for Add button
    
    # Add Currency page locators
    currency_code_input = "#TODO-verify-currency-code-input"
    currency_description_input = "#TODO-verify-currency-description-input"
    minor_digits_input = "#TODO-verify-minor-digits-input"
    currency_symbol_input = "#TODO-verify-currency-symbol-input"
    save_button = "#TODO-verify-save-button"
    cancel_button = "#TODO-verify-cancel-button"
    message_container = "#TODO-verify-message-container"  # For success/error messages
    
    # Currency list table locators (for row operations)
    # Template for finding a row by Currency Code (to be formatted with actual value)
    currency_row_template = "//tr[td[normalize-space(text())='{currency_code}']]"
    # Locators within a row for View/Edit buttons
    view_button_in_row = ".//a[contains(text(),'View')]"
    edit_button_in_row = ".//a[contains(text(),'Edit')]"
    # Global buttons (if needed)
    change_status_button = "#TODO-verify-change-status-button"
    # Checkbox in row for selecting records
    row_checkbox_template = ".//input[@type='checkbox']"
    
    # View Currency page locators
    view_currency_code_display = "#TODO-verify-view-currency-code-display"
    view_currency_description_display = "#TODO-verify-view-currency-description-display"
    view_minor_digits_display = "#TODO-verify-view-minor-digits-display"
    view_currency_symbol_display = "#TODO-verify-view-currency-symbol-display"
    view_status_display = "#TODO-verify-view-status-display"
    view_back_button = "#TODO-verify-view-back-button"
    
    # Edit Currency page locators (same as Add page fields but may have different behavior)
    edit_currency_code_display = "#TODO-verify-edit-currency-code-display"  # Likely read-only
    edit_currency_description_input = "#TODO-verify-edit-currency-description-input"
    edit_minor_digits_input = "#TODO-verify-edit-minor-digits-input"
    edit_currency_symbol_input = "#TODO-verify-edit-currency-symbol-input"
    edit_save_button = "#TODO-verify-edit-save-button"
    edit_cancel_button = "#TODO-verify-edit-cancel-button"
    
    # List page locators (to verify we are on the correct page)
    currency_list_page_indicator = "//h1[contains(text(),'Currency List')]"  # Example, adjust as needed
