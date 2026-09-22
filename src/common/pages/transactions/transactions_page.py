"""Reusable transaction page object.

Transaction behaviour is common; bank-specific selectors are supplied through
small locator classes in ``src/banks/<bank>/locators``. Adding another bank
means adding its locator implementation to the dispatch maps instead of
copying this page object.
"""
from __future__ import annotations

import re
from typing import Any

import allure

from src.banks.fab.locators.transaction_locators import (
    FabAdpayLocators,
    FabHomeLocators,
    FabMpayLocators,
)
from src.common.base.base_page import BasePage
from src.common.utilities.config_loader import ConfigManager


class TransactionsPage(BasePage):
    def __init__(self, page, module_name="Transactions"):
        super().__init__(page, module_name=module_name)
        self._home_dispatch = {
            "fab": (self._standard_home_flow, FabHomeLocators),
        }
        self._adpay_dispatch = {
            "fab": (self._standard_adpay_flow, FabAdpayLocators),
        }
        self._mpay_dispatch = {
            "fab": (self._standard_mpay_flow, FabMpayLocators),
        }
        self.captured_payment_id: str | None = None
        self.captured_recurring_id: str | None = None
        self.captured_card_id: str | None = None
        self.captured_finalization_api_id: str | None = None

    # ------------------------------------------------------------------
    # Dispatch helpers - same reusable pattern used elsewhere in the
    # framework. Bank-specific code stays in the banks/<bank>/ package.
    # ------------------------------------------------------------------
    def _home(self, bank: str):
        return self._home_dispatch[bank.lower()][1]

    def _adpay(self, bank: str):
        return self._adpay_dispatch[bank.lower()][1]

    def _mpay(self, bank: str):
        return self._mpay_dispatch[bank.lower()][1]

    @staticmethod
    def _value(data: dict[str, Any], *keys: str, default: Any = None) -> Any:
        for key in keys:
            if key in data and data[key] not in (None, ""):
                return data[key]
        return default

    def _fill_if_present(self, locator, data: dict[str, Any], keys: tuple[str, ...], description: str) -> None:
        value = self._value(data, *keys)
        if value is not None:
            self.fill_by_locator(locator, str(value), description)

    def _fill_by_role_if_present(self, role: str, name: str, data: dict[str, Any], keys: tuple[str, ...], description: str) -> None:
        value = self._value(data, *keys)
        if value is not None:
            self.fill_by_role(role, name, str(value))

    def _standard_home_flow(self, data: dict[str, Any], loc) -> None:
        """Common hook for banks that share the standard transaction form."""
        self._fill_if_present(loc.tid, data, ("TID", "tid"), "TID")
        self._fill_if_present(loc.version, data, ("Version", "version"), "Version")
        self._fill_if_present(loc.adgeid1, data, ("ADGEID1", "adgeid1"), "ADGEID1")
        self._fill_if_present(loc.service11, data, ("Service11", "service11", "Service1"), "Service")
        self._fill_if_present(loc.password, data, ("Password", "pwd"), "Password")
        self._fill_if_present(loc.corid, data, ("CORID", "corid"), "CORID")
        self._fill_if_present(loc.amount, data, ("Amount", "amount"), "Amount")
        self._fill_if_present(loc.quantity, data, ("Quantity", "qty"), "Quantity")
        self._fill_if_present(loc.udf1, data, ("UDF1", "udf1"), "UDF1")

    def _standard_adpay_flow(self, data: dict[str, Any], loc) -> None:
        """Common hook for banks that share the ADPAY hosted payment form."""
        return None

    def _standard_mpay_flow(self, data: dict[str, Any], loc) -> None:
        """Common hook for banks that share the MPAY hosted payment form."""
        return None

    # ------------------------------------------------------------------
    # Navigation / demo transaction form
    # ------------------------------------------------------------------
    @allure.step("Open transaction portal")
    def open_transaction_portal(self, bank: str) -> None:
        # FAB transactions are hosted on a dedicated portal. The URL is
        # resolved from the bank credentials file when available.
        try:
            config = ConfigManager.load_portal_config("transaction_tranportal")
            url = config["url"]
        except Exception:
            url = self._home(bank).demo_url
        self.navigate(url)

    @allure.step("Go to transaction page: {transaction}")
    def go_to_transaction(self, bank: str, transaction: str) -> None:
        loc = self._home(bank)
        links = {
            "purchase": loc.purchase_link,
            "refund": loc.refund_link,
            "void": loc.void_link,
            "authorization": loc.authorization_link,
            "capture": loc.capture_link,
            "inquiry": loc.inquiry_link,
            "recurring_list_cards": loc.recurring_list_cards_link,
            "recurring_registration": loc.recurring_registration_link,
            "recurring_payment": loc.recurring_payment_link,
            "finalization_api": loc.finalization_api_link,
        }
        key = transaction.lower()
        if key not in links:
            raise ValueError(f"Unsupported transaction page: {transaction}")
        self.click_by_locator(links[key], f"Open {transaction} transaction page")

    @allure.step("Return to transaction home page")
    def go_back_home(self, bank: str) -> None:
        self.click_by_locator(self._home(bank).home_link, "Home Page")

    @allure.step("Fill transaction form")
    def fill_transaction_form(self, bank: str, data: dict[str, Any]) -> None:
        _, loc = self._home_dispatch[bank.lower()]
        self._standard_home_flow(data, loc)

    @allure.step("Fill inquiry form")
    def fill_inquiry_form(self, bank: str, data: dict[str, Any]) -> None:
        loc = self._home(bank)
        self._fill_if_present(loc.tid, data, ("TID", "tid"), "TID")
        self._fill_if_present(loc.version, data, ("Version", "version"), "Version")
        self._fill_if_present(loc.password, data, ("Password", "pwd"), "Password")
        self._fill_if_present(loc.inquiry_type, data, ("Inquiry Type", "InqType"), "Inquiry Type")

    @allure.step("Fill void form")
    def fill_void_form(self, bank: str, data: dict[str, Any]) -> None:
        loc = self._home(bank)
        self._fill_if_present(loc.tid, data, ("TID", "tid"), "TID")
        self._fill_if_present(loc.version, data, ("Version", "version"), "Version")
        self._fill_if_present(loc.password, data, ("Password", "pwd"), "Password")
        self._fill_if_present(loc.corid, data, ("CORID", "corid"), "CORID")

    @allure.step("Fill refund form")
    def fill_refund_form(self, bank: str, data: dict[str, Any]) -> None:
        self.fill_transaction_form(bank, data)

    @allure.step("Fill capture form")
    def fill_capture_form(self, bank: str, data: dict[str, Any]) -> None:
        self.fill_transaction_form(bank, data)

    @allure.step("Fill finalization API form")
    def fill_finalization_api_form(self, bank: str, data: dict[str, Any]) -> None:
        loc = self._home(bank)
        for selector, keys, description in (
            (loc.tid, ("TID", "tid"), "TID"),
            (loc.version, ("Version", "version"), "Version"),
            (loc.password, ("Password", "pwd"), "Password"),
        ):
            self._fill_if_present(selector, data, keys, description)

    @allure.step("Fill recurring list-cards form")
    def fill_recurring_list_cards_form(self, bank: str, data: dict[str, Any]) -> None:
        loc = self._home(bank)
        self._fill_if_present(loc.tid, data, ("TID", "tid"), "TID")
        self._fill_if_present(loc.password, data, ("Password", "pwd"), "Password")
        self._fill_if_present(loc.udf1, data, ("UDF1", "udf1"), "UDF1")

    @allure.step("Fill recurring registration form")
    def fill_recurring_registration_form(self, bank: str, data: dict[str, Any]) -> None:
        loc = self._home(bank)
        for selector, keys, description in (
            (loc.tid, ("TID", "tid"), "TID"),
            (loc.version, ("Version", "version"), "Version"),
            (loc.adgeid1, ("ADGEID1", "adgeid1"), "ADGEID1"),
            (loc.service11, ("Service11", "service11"), "Service11"),
            (loc.password, ("Password", "pwd"), "Password"),
            (loc.udf1, ("UDF1", "udf1"), "UDF1"),
        ):
            self._fill_if_present(selector, data, keys, description)

    @allure.step("Fill recurring payment form")
    def fill_recurring_payment_form(self, bank: str, data: dict[str, Any]) -> None:
        loc = self._home(bank)
        for selector, keys, description in (
            (loc.tid, ("TID", "tid"), "TID"),
            (loc.version, ("Version", "version"), "Version"),
            (loc.password, ("Password", "pwd"), "Password"),
            (loc.corid, ("CORID", "corid"), "CORID"),
        ):
            self._fill_if_present(selector, data, keys, description)
        self._fill_if_present(loc.amount, data, ("Amount", "amount"), "Amount")
        self._fill_if_present(loc.udf1, data, ("UDF1", "udf1"), "UDF1")

    @allure.step("Fill MPAY additional request fields")
    def fill_mpay_request_fields(self, bank: str, data: dict[str, Any]) -> None:
        loc = self._home(bank)
        self._fill_if_present(loc.udf11, data, ("UDF11", "udf11"), "UDF11")
        self._fill_if_present(loc.udf12, data, ("UDF12", "udf12"), "UDF12")
        self._fill_if_present(loc.entity_id, data, ("Entity ID", "ENTITYID", "EntityId"), "Entity ID")

    @allure.step("Fill additional amounts")
    def fill_additional_amounts(self, bank: str, data: dict[str, Any]) -> None:
        loc = self._home(bank)
        self._fill_if_present(loc.dynamic_amount1, data, ("Dynamic Amount1", "DynamicAmount1", "DynamicAmount"), "Dynamic Amount 1")
        self._fill_if_present(loc.dynamic_amount2, data, ("Dynamic Amount2", "DynamicAmount2", "DynamicAmount"), "Dynamic Amount 2")
        self._fill_if_present(loc.dynamic_amount3, data, ("Dynamic Amount3", "DynamicAmount3"), "Dynamic Amount 3")

    @allure.step("Fill header version")
    def fill_header_version(self, bank: str, data: dict[str, Any]) -> None:
        self._fill_if_present(self._home(bank).header_version, data, ("Header Version", "HeaderVersion"), "Header Version")

    @allure.step("Select language")
    def select_language(self, bank: str, value: str) -> None:
        loc = self._home(bank)
        self.select_by_locator(loc.language, str(value), "Language")

    @allure.step("Select MPAY endpoint")
    def select_mpay_endpoint(self, bank: str) -> None:
        self.click_by_xpath(self._home(bank).endpoint_option, "MPAY endpoint")

    @allure.step("Select MPAY project")
    def select_mpay_project(self, bank: str) -> None:
        self.click_by_xpath(self._home(bank).project_option_mpay, "MPAY project")

    @allure.step("Select merchant portal project")
    def select_merchant_portal_project(self, bank: str) -> None:
        self.click_by_xpath(self._home(bank).project_option_merchant_portal, "Merchant portal project")

    @allure.step("Select recurring project")
    def select_recurring_project(self, bank: str) -> None:
        self.click_by_xpath(self._home(bank).project_option_recurring, "Recurring project")

    @allure.step("Click Buy")
    def click_buy(self, bank: str) -> None:
        self.click_by_xpath(self._home(bank).buy_button, "Buy button")

    # ------------------------------------------------------------------
    # ADPAY card / wallet / direct-debit actions
    # ------------------------------------------------------------------
    @allure.step("Select ADPAY payment method")
    def click_change_payment(self, bank: str) -> None:
        self.click_by_xpath(self._adpay(bank).change_payment, "Change payment")

    @allure.step("Select ADPAY card payment")
    def click_select_payment(self, bank: str) -> None:
        self.click_by_xpath(self._adpay(bank).select_payment, "Select payment")

    @allure.step("Add card details")
    def add_card(self, bank: str, data: dict[str, Any]) -> None:
        loc = self._adpay(bank)
        self.click_by_role("heading", "Add", exact=True)
        self._fill_by_role_if_present("textbox", "Enter name", data, ("Card Name", "card_name"), "Cardholder name")
        self._fill_by_role_if_present("textbox", "Enter card number", data, ("Card Number", "card_number"), "Card number")
        self._fill_by_role_if_present("textbox", "***", data, ("CVV", "cvv"), "CVV")

    @allure.step("Select card expiry month")
    def select_card_month(self, bank: str) -> None:
        loc = self._adpay(bank)
        self.click_by_xpath(loc.select_month, "Select Month")
        self.click_by_xpath(loc.select_month_option, "Select Month Option")

    @allure.step("Select card expiry year")
    def select_card_year(self, bank: str) -> None:
        loc = self._adpay(bank)
        self.click_by_xpath(loc.select_year, "Select Year")
        self.click_by_xpath(loc.select_year_option, "Select Year Option")

    @allure.step("Pay by ADPAY card")
    def pay_card(self, bank: str) -> None:
        self.click_by_xpath(self._adpay(bank).payment_pay_button, "Pay button")

    @allure.step("Select ADPAY ComeraPay")
    def select_comerapay(self, bank: str) -> None:
        self.click_by_xpath(self._adpay(bank).comerapay, "Select ComeraPay")

    @allure.step("Complete ComeraPay validation")
    def complete_comerapay(self, bank: str, data: dict[str, Any]) -> None:
        loc = self._adpay(bank)
        number = self._value(data, "ComeraPay Number", "ComerapayNumber")
        otp = self._value(data, "ComeraPay OTP", "ComerapayOTP")
        if number is not None:
            self.fill_by_locator(loc.comerapay_registered_number, str(number), "ComeraPay Registered Number")
        self.click_by_xpath(loc.comerapay_request_otp, "Request OTP")
        if otp is not None:
            self.fill_by_getbyrole(loc.comerapay_otp, str(otp), "Enter OTP")
        self.click_by_xpath(loc.comerapay_confirm_button, "ComeraPay Confirm")

    @allure.step("Select direct debit")
    def select_direct_debit(self, bank: str) -> None:
        self.click_by_xpath(self._adpay(bank).direct_debit, "Direct Debit")

    @allure.step("Select direct debit bank and product")
    def select_direct_debit_details(self, bank: str, data: dict[str, Any]) -> None:
        loc = self._adpay(bank)
        bank_value = self._value(data, "Bank")
        product_value = self._value(data, "Product")
        if bank_value is not None:
            self.select_by_locator(loc.bank_list, str(bank_value), "Bank")
        if product_value is not None:
            self.select_by_locator(loc.product_list, str(product_value), "Product")

    @allure.step("Submit direct debit")
    def submit_direct_debit(self, bank: str) -> None:
        loc = self._adpay(bank)
        self.click_by_xpath(loc.submit_button, "Submit button")
        self.click_by_xpath(loc.terms_checkbox, "Accept terms checkbox")
        self.click_by_xpath(loc.submit_button, "Final Submit button")

    @allure.step("Fill direct debit simulator response")
    def fill_direct_debit_response(self, bank: str, data: dict[str, Any]) -> None:
        loc = self._adpay(bank)
        for selector, keys, description in (
            (loc.response_code, ("Response Code", "ResponseCode"), "Response Code"),
            (loc.response_message, ("Response Message", "ResponseMessage"), "Response Message"),
            (loc.auth_code, ("Auth Code", "AuthCode"), "Auth Code"),
            (loc.bank_id, ("Bank ID", "BankID"), "Bank ID"),
        ):
            self._fill_if_present(selector, data, keys, description)

    @allure.step("Generate hash and return to payment gateway")
    def generate_hash_and_return_to_pg(self, bank: str) -> None:
        loc = self._adpay(bank)
        self.click_by_locator(loc.generate_hash, "Generate Hash")
        self.click_by_locator(loc.return_to_pg, "Return to PG")

    @allure.step("Verify ADPAY payment summary")
    def assert_adpay_summary(self, bank: str, arabic: bool = False) -> None:
        loc = self._adpay(bank)
        selector = loc.summary_header_ar if arabic else loc.summary_header
        expected = "Summary"
        self.assert_visible(self.locator(selector), "Payment Summary header")
        self.assert_text(self.locator(selector), expected, "Payment Summary text")

    @allure.step("Verify ADPAY currency symbol")
    def assert_adpay_currency_symbol(self, bank: str, arabic: bool = False) -> None:
        loc = self._adpay(bank)
        selector = loc.dirham_symbol_ar if arabic else loc.dirham_symbol
        self.assert_visible(self.locator(selector), "Dirham symbol")

    @allure.step("Verify ADPAY payment status")
    def assert_adpay_payment_status(self, bank: str, expected_message: str | None = None) -> None:
        loc = self._adpay(bank)
        if expected_message:
            self.assert_text(self.locator(loc.payment_response), expected_message, "ADPAY payment status")
        else:
            self.assert_visible(self.locator(loc.payment_response), "ADPAY payment response")

    # ------------------------------------------------------------------
    # MPAY actions
    # ------------------------------------------------------------------
    @allure.step("Select MPAY new card")
    def click_mpay_new_card(self, bank: str) -> None:
        self.click_by_xpath(self._mpay(bank).new_card, "New card")

    @allure.step("Fill MPAY card details")
    def fill_mpay_card_details(self, bank: str, data: dict[str, Any]) -> None:
        loc = self._mpay(bank)
        self._fill_if_present(loc.cardholder_name, data, ("Card Name", "card_name"), "Cardholder name")
        self._fill_if_present(loc.card_number, data, ("Card Number", "card_number"), "Card number")
        self._fill_if_present(loc.cvv, data, ("CVV", "cvv"), "CVV")
        month = self._value(data, "Expiry Month", "Exp_Month", "exp_month")
        year = self._value(data, "Expiry Year", "Exp_Year", "exp_year")
        if month is not None:
            self.select_by_locator(loc.expiry_month, str(month), "Expiry Month")
        if year is not None:
            self.select_by_locator(loc.expiry_year, str(year), "Expiry Year")

    @allure.step("Fill MPAY receipt email")
    def fill_mpay_receipt_email(self, bank: str, data: dict[str, Any]) -> None:
        self._fill_if_present(self._mpay(bank).receipt_email, data, ("Receipt Email", "Receipt_email"), "Receipt Email")

    @allure.step("Complete MPAY payment")
    def click_mpay_pay(self, bank: str) -> None:
        self.click_by_xpath(self._mpay(bank).click_pay, "MPAY Pay button")

    @allure.step("Select MPAY saved card")
    def click_mpay_saved_card(self, bank: str) -> None:
        loc = self._mpay(bank)
        self.click_by_xpath(loc.saved_card, "MPAY saved card")
        self._record("Selected MPAY saved card")

    @allure.step("Fill MPAY saved card CVV")
    def fill_mpay_saved_card_cvv(self, bank: str, data: dict[str, Any]) -> None:
        self._fill_if_present(self._mpay(bank).saved_card_cvv, data, ("CVV", "cvv"), "Saved card CVV")

    @allure.step("Select MPAY Tabby")
    def select_tabby(self, bank: str) -> None:
        self.click_by_xpath(self._mpay(bank).click_tabby, "Tabby")

    @allure.step("Fill Tabby details")
    def fill_tabby_details(self, bank: str, data: dict[str, Any], arabic: bool = False) -> None:
        loc = self._mpay(bank)
        self._fill_if_present(loc.tabby_email, data, ("Tabby Email", "email_tabby"), "Tabby Email")
        self.click_by_xpath(loc.tabby_continue_ar if arabic else loc.tabby_continue, "Tabby Continue")
        self._fill_if_present(loc.tabby_otp, data, ("Tabby OTP", "otp_tabby"), "Tabby OTP")
        self.click_by_xpath(loc.tabby_otp_continue_ar if arabic else loc.tabby_continue, "Tabby OTP Continue")
        if arabic:
            self.click_by_xpath(loc.tabby_final_continue_ar, "Tabby final Continue")

    @allure.step("Select Tabby installment")
    def select_tabby_installment(self, bank: str) -> None:
        loc = self._mpay(bank)
        self.click_by_xpath(loc.tabby_check_box, "Tabby checkbox")
        self.click_by_xpath(loc.tabby_installment, "Tabby installment")
        self.click_by_xpath(loc.tabby_installment_continue, "Tabby Continue")

    @allure.step("Select MPAY charity")
    def select_mpay_charity(self, bank: str, amount: Any) -> None:
        loc = self._mpay(bank)
        self.click_by_xpath(loc.charity1, "Charity 1")
        self.fill_by_locator(loc.charity1_amount, str(amount), "Charity 1 Amount")

    @allure.step("Select MPAY Arabic charities")
    def select_mpay_arabic_charities(self, bank: str, amount: Any) -> None:
        loc = self._mpay(bank)
        for checkbox, field, number in (
            (loc.charity1_ar, loc.charity1_amount_ar, 1),
            (loc.charity2_ar, loc.charity2_amount_ar, 2),
            (loc.charity3_ar, loc.charity3_amount_ar, 3),
        ):
            self.click_by_xpath(checkbox, f"Charity {number} Arabic")
            self.fill_by_locator(field, str(amount), f"Charity {number} Amount Arabic")

    @allure.step("Verify MPAY payment status")
    def assert_mpay_payment_status(self, bank: str, expected_message: str | None = None) -> None:
        loc = self._mpay(bank)
        if expected_message:
            self.assert_text(self.locator(loc.payment_response), expected_message, "MPAY payment status")
        else:
            self.assert_visible(self.locator(loc.payment_response), "MPAY payment response")

    @allure.step("Verify MPAY inquiry status")
    def assert_mpay_inquiry_status(self, bank: str, expected_message: str | None = None) -> None:
        loc = self._mpay(bank)
        if expected_message:
            self.assert_text(self.locator(loc.inquiry_response), expected_message, "MPAY inquiry status")
        else:
            self.assert_visible(self.locator(loc.inquiry_response), "MPAY inquiry response")


    @allure.step("Select ADPAY saved card")
    def select_adpay_saved_card(self, bank: str, card_type: str, data: dict[str, Any]) -> None:
        loc = self._adpay(bank)
        card_map = {
            "mastercard": (loc.saved_card_mastercard, loc.saved_card_mastercard_cvv),
            "amex": (loc.saved_card_amex, loc.saved_card_amex_cvv),
            "visa": (loc.saved_card_visa, loc.saved_card_visa_cvv),
            "jaywan": (loc.saved_card_jaywan, loc.saved_card_jaywan_cvv),
        }
        key = card_type.lower()
        if key not in card_map:
            raise ValueError(f"Unsupported ADPAY saved card type: {card_type}")
        card_locator, cvv_locator = card_map[key]
        self.click_by_xpath(card_locator, f"Select {card_type} saved card")
        self._fill_if_present(cvv_locator, data, ("CVV", "cvv"), "Saved card CVV")

    @allure.step("Select ADPAY recurring saved card")
    def select_adpay_recurring_saved_card(self, bank: str) -> None:
        self.click_by_xpath(self._adpay(bank).recurring_saved_card, "Recurring saved card")

    @allure.step("Fill MPAY recurring card details")
    def fill_mpay_recurring_card(self, bank: str, data: dict[str, Any]) -> None:
        loc = self._mpay(bank)
        self._fill_if_present(loc.recurring_cardholder_name, data, ("Card Name", "card_name"), "Recurring Cardholder Name")
        self._fill_if_present(loc.recurring_card_number, data, ("Card Number", "card_number"), "Recurring Card Number")
        self._fill_if_present(loc.recurring_cvv, data, ("CVV", "cvv"), "Recurring CVV")
        month = self._value(data, "Expiry Month", "Exp_Month", "exp_month")
        year = self._value(data, "Expiry Year", "Exp_Year", "exp_year")
        if month is not None:
            self.select_by_locator(loc.recurring_expiry_month, str(month), "Recurring Expiry Month")
        if year is not None:
            self.select_by_locator(loc.recurring_expiry_year, str(year), "Recurring Expiry Year")

    @allure.step("Select MPAY recurring saved card")
    def select_mpay_recurring_saved_card(self, bank: str) -> None:
        self.click_by_xpath(self._mpay(bank).recurring_saved_card, "Recurring saved card")

    # ------------------------------------------------------------------
    # Common result / supporting transaction actions
    # ------------------------------------------------------------------
    @allure.step("Capture payment ID")
    def capture_payment_id(self, bank: str) -> str:
        self.page.wait_for_load_state("load", timeout=90_000)
        body_text = self.get_text(self.locator(self._home(bank).body), "Result page")
        match = re.search(r'"paymentid"\s*:\s*"([^"]+)"', body_text, re.IGNORECASE)
        if not match:
            allure.attach(self.page.content(), "Result HTML (PaymentID not found)", allure.attachment_type.HTML)
            raise AssertionError("Payment ID not found on result page")
        self.captured_payment_id = match.group(1)
        self.logger.info("Captured Payment ID: %s", self.captured_payment_id)
        return self.captured_payment_id

    @allure.step("Fill captured payment ID")
    def fill_captured_payment_id(self, bank: str) -> str:
        if not self.captured_payment_id:
            raise AssertionError("No payment ID has been captured yet")
        self.fill_by_locator(self._home(bank).comment, self.captured_payment_id, "Comment")
        return self.captured_payment_id

    @allure.step("Select UDF5")
    def select_udf5(self, bank: str, value: Any) -> None:
        self.select_by_locator(self._home(bank).udf5, str(value), "UDF5")

    @allure.step("Capture recurring ID")
    def capture_recurring_id(self, bank: str) -> str:
        self.page.wait_for_load_state("load", timeout=90_000)
        result_text = self.get_text(self.locator(self._home(bank).final_api_body), "Recurring result")
        match = re.search(r'"recurringID"\s*:\s*"([^"]+)"', result_text, re.IGNORECASE)
        if not match:
            raise AssertionError("Recurring ID not found on result page")
        self.captured_recurring_id = match.group(1)
        return self.captured_recurring_id

    @allure.step("Fill captured recurring ID")
    def fill_captured_recurring_id(self, bank: str) -> str:
        if not self.captured_recurring_id:
            raise AssertionError("No recurring ID has been captured yet")
        self.fill_by_locator(self._home(bank).recurring_id_input, self.captured_recurring_id, "Recurring ID")
        return self.captured_recurring_id

    @allure.step("Capture card ID")
    def capture_card_id(self, bank: str) -> str:
        self.page.wait_for_load_state("load", timeout=90_000)
        card_id = self.get_text(self.locator(self._home(bank).card_id_value), "Card ID")
        if not card_id:
            raise AssertionError("Card ID not found")
        self.captured_card_id = card_id.strip()
        return self.captured_card_id

    @allure.step("Fill captured card ID")
    def fill_captured_card_id(self, bank: str) -> str:
        if not self.captured_card_id:
            raise AssertionError("No card ID has been captured yet")
        self.fill_by_locator(self._home(bank).card_id_input, self.captured_card_id, "Card ID")
        return self.captured_card_id

    @allure.step("Fill captured finalization API payment ID")
    def fill_captured_finalization_api_id(self, bank: str) -> str:
        if not self.captured_finalization_api_id:
            raise AssertionError("No finalization API payment ID has been captured yet")
        self.fill_by_locator(
            self._home(bank).finalization_api_payment_id,
            self.captured_finalization_api_id,
            "Finalization API payment ID",
        )
        return self.captured_finalization_api_id

    @allure.step("Capture finalization API payment ID")
    def capture_finalization_api_id(self, bank: str) -> str:
        value = self.get_attribute(self.locator(self._home(bank).finalization_api_payment_id), "value", "Finalization API payment ID")
        if not value:
            raise AssertionError("Finalization API payment ID not found")
        self.captured_finalization_api_id = value.strip()
        return self.captured_finalization_api_id

    @allure.step("Click refund")
    def click_refund(self, bank: str) -> None:
        self.click_by_locator(self._home(bank).refund_link, "Refund")

    @allure.step("Click void")
    def click_void(self, bank: str) -> None:
        self.click_by_locator(self._home(bank).void_link, "Void")

    @allure.step("Verify transaction result")
    def assert_transaction_result(self, bank: str, expected_message: str | None) -> None:
        if not expected_message:
            return
        self.assert_text(self.locator(self._home(bank).result_message), expected_message, "Transaction result")

    @allure.step("Click back to merchant")
    def click_back_to_merchant(self, bank: str) -> None:
        self.click_by_xpath(self._home(bank).back_to_merchant, "Back to Merchant")

    @allure.step("Download receipt")
    def click_download_receipt(self, bank: str) -> None:
        self.click_by_xpath(self._home(bank).download_receipt, "Download Receipt")

    # ------------------------------------------------------------------
    # ICP transaction fields
    # ------------------------------------------------------------------
    @allure.step("Fill ICP transaction form")
    def fill_icp_form(self, bank: str, data: dict[str, Any]) -> None:
        loc = self._home(bank)
        mapping = (
            (loc.tid, ("TID", "tid"), "TID"),
            (loc.version, ("Version", "version"), "Version"),
            (loc.adgeid1, ("ADGEID1", "adgeid1"), "ADGEID1"),
            (loc.service11, ("Service1", "service1", "Service11", "service11"), "Service1"),
            (loc.password, ("Password", "pwd"), "Password"),
            (loc.corid, ("CORID", "corid"), "CORID"),
            (loc.amount, ("Amount", "amount"), "Amount"),
            (loc.quantity, ("Quantity", "qty"), "Quantity"),
            (loc.dynamic_amount1, ("Dynamic Amount1", "DynamicAmount1"), "Dynamic Amount 1"),
            (loc.dynamic_amount2, ("Dynamic Amount2", "DynamicAmount2"), "Dynamic Amount 2"),
            (loc.dynamic_amount3, ("Dynamic Amount3", "DynamicAmount3"), "Dynamic Amount 3"),
            (loc.udf1, ("UDF1", "udf1"), "UDF1"),
        )
        for selector, keys, description in mapping:
            self._fill_if_present(selector, data, keys, description)

    @allure.step("Fill ICP additional service")
    def fill_icp_additional_service(self, bank: str, data: dict[str, Any]) -> None:
        loc = self._home(bank)
        self._fill_if_present(loc.service2, data, ("Service2", "service2"), "Service 2")
        self._fill_if_present(loc.service_amount2, data, ("Service2 Amount", "Service2Amount", "serviceAmount2"), "Service 2 Amount")

    @allure.step("Fill ICP vendor merchant 1")
    def fill_icp_vendor_one(self, bank: str, data: dict[str, Any]) -> None:
        loc = self._home(bank)
        for selector, keys, description in (
            (loc.vendor_adgeid1, ("Vendor ADGEID1", "VendorADGEID1"), "Vendor ADGEID1"),
            (loc.vendor_service1, ("Vendor Service1", "VendorService1"), "Vendor Service1"),
            (loc.vendor_service1_amount, ("Vendor Service1 Amount", "VendorService1Amount"), "Vendor Service1 Amount"),
            (loc.vendor_dynamic_amount1, ("Vendor Dynamic Amount1", "VendorDynamicAmount1"), "Vendor Dynamic Amount 1"),
            (loc.vendor_dynamic_amount2, ("Vendor Dynamic Amount2", "VendorDynamicAmount2"), "Vendor Dynamic Amount 2"),
            (loc.vendor_dynamic_amount3, ("Vendor Dynamic Amount3", "VendorDynamicAmount3"), "Vendor Dynamic Amount 3"),
        ):
            self._fill_if_present(selector, data, keys, description)

    @allure.step("Fill ICP vendor merchant 2")
    def fill_icp_vendor_two(self, bank: str, data: dict[str, Any]) -> None:
        loc = self._home(bank)
        for selector, keys, description in (
            (loc.vendor_adgeid2, ("Vendor ADGEID2", "VendorADGEID2"), "Vendor ADGEID2"),
            (loc.vendor_service2, ("Vendor Service2", "VendorService2"), "Vendor Service2"),
            (loc.vendor_service2_amount, ("Vendor Service2 Amount", "VendorService2Amount"), "Vendor Service2 Amount"),
        ):
            self._fill_if_present(selector, data, keys, description)
