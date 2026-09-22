from __future__ import annotations

from typing import Any

import allure
import pytest

from src.common.pages.transactions.transactions_page import TransactionsPage
from src.common.utilities.config_loader import ConfigManager
from src.common.utilities.excel_utils import ExcelUtil

BANK_NAME = ConfigManager.get("bank")

def _rows(sheet: str) -> list[dict[str, Any]]:
    rows = ExcelUtil.get_sheet("Transactions", sheet)
    return [row for row in rows if str(row.get("Execution Status", "yes")).lower() == "yes"]

def _ids(rows: list[dict[str, Any]]) -> list[str]:
    return [f'{row["ScenarioID"]} - {row["TestcaseID"]} - {row["Description"]}' for row in rows]

def _prepare_adpay(page, data: dict[str, Any], transaction: str) -> TransactionsPage:
    transactions = TransactionsPage(page)
    transactions.open_transaction_portal(BANK_NAME)
    transactions.go_to_transaction(BANK_NAME, transaction)
    transactions.fill_transaction_form(BANK_NAME, data)
    transactions.fill_additional_amounts(BANK_NAME, data)
    transactions.fill_header_version(BANK_NAME, data)
    transactions.click_buy(BANK_NAME)
    return transactions

def _complete_adpay_card(page, data: dict[str, Any], transaction: str = "purchase") -> TransactionsPage:
    transactions = _prepare_adpay(page, data, transaction)
    transactions.assert_adpay_summary(BANK_NAME)
    transactions.assert_adpay_currency_symbol(BANK_NAME)
    transactions.click_change_payment(BANK_NAME)
    transactions.add_card(BANK_NAME, data)
    transactions.select_card_month(BANK_NAME)
    transactions.select_card_year(BANK_NAME)
    transactions.pay_card(BANK_NAME)
    transactions.assert_adpay_payment_status(BANK_NAME)
    return transactions

def _mpay_card_payment(page, data: dict[str, Any], transaction: str = "purchase") -> TransactionsPage:
    tx = TransactionsPage(page)
    tx.open_transaction_portal(BANK_NAME)
    tx.go_to_transaction(BANK_NAME, transaction)
    tx.fill_transaction_form(BANK_NAME, data)
    tx.select_mpay_project(BANK_NAME)
    tx.select_mpay_endpoint(BANK_NAME)
    tx.fill_mpay_request_fields(BANK_NAME, data)
    tx.click_buy(BANK_NAME)
    tx.click_mpay_new_card(BANK_NAME)
    tx.fill_mpay_card_details(BANK_NAME, data)
    if data.get("Language") == "AR":
        tx.select_mpay_arabic_charities(BANK_NAME, data.get("Charity Amount"))
    tx.fill_mpay_receipt_email(BANK_NAME, data)
    tx.click_mpay_pay(BANK_NAME)
    tx.assert_mpay_payment_status(BANK_NAME)
    return tx

def _mpay_tabby_payment(page, data: dict[str, Any], transaction: str = "purchase") -> TransactionsPage:
    tx = TransactionsPage(page)
    tx.open_transaction_portal(BANK_NAME)
    tx.go_to_transaction(BANK_NAME, transaction)
    tx.fill_transaction_form(BANK_NAME, data)
    tx.select_mpay_project(BANK_NAME)
    tx.select_mpay_endpoint(BANK_NAME)
    tx.fill_mpay_request_fields(BANK_NAME, data)
    tx.click_buy(BANK_NAME)
    tx.select_tabby(BANK_NAME)
    tx.click_mpay_pay(BANK_NAME)
    tx.fill_tabby_details(BANK_NAME, data, arabic=data.get("Language") == "AR")
    tx.select_tabby_installment(BANK_NAME)
    tx.assert_mpay_payment_status(BANK_NAME)
    return tx

def _merchant_card_purchase(page, data: dict[str, Any]) -> TransactionsPage:
    tx = TransactionsPage(page)
    tx.open_transaction_portal(BANK_NAME)
    tx.go_to_transaction(BANK_NAME, "purchase")
    tx.fill_transaction_form(BANK_NAME, data)
    tx.select_merchant_portal_project(BANK_NAME)
    tx.fill_additional_amounts(BANK_NAME, data)
    tx.fill_header_version(BANK_NAME, data)
    tx.click_buy(BANK_NAME)
    tx.assert_adpay_summary(BANK_NAME)
    tx.assert_adpay_currency_symbol(BANK_NAME)
    tx.click_change_payment(BANK_NAME)
    tx.add_card(BANK_NAME, data)
    tx.select_card_month(BANK_NAME)
    tx.select_card_year(BANK_NAME)
    tx.pay_card(BANK_NAME)
    tx.assert_adpay_payment_status(BANK_NAME)
    return tx
