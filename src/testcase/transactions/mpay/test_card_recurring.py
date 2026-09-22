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

@pytest.mark.sanity
@pytest.mark.regression
@pytest.mark.fab
class TestFabMpayTransactions(object):
        def test_mpay_recurring(self, page, data):
            transactions = TransactionsPage(page)
            transactions.open_transaction_portal(BANK_NAME)
            transactions.go_to_transaction(BANK_NAME, "recurring_registration")
            transactions.fill_recurring_registration_form(BANK_NAME, data)
            transactions.select_recurring_project(BANK_NAME)
            transactions.click_buy(BANK_NAME)
            transactions.fill_mpay_recurring_card(BANK_NAME, data)
            transactions.select_mpay_recurring_saved_card(BANK_NAME)
            transactions.capture_recurring_id(BANK_NAME)
            transactions.go_back_home(BANK_NAME)
            transactions.open_transaction_portal(BANK_NAME)
            transactions.go_to_transaction(BANK_NAME, "recurring_payment")
            transactions.fill_recurring_payment_form(BANK_NAME, data)
            transactions.fill_captured_recurring_id(BANK_NAME)
            transactions.click_buy(BANK_NAME)

