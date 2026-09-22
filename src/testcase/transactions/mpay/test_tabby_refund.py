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

from src.testcase.transactions._transaction_helpers import (_mpay_tabby_payment)

@pytest.mark.sanity
@pytest.mark.regression
@pytest.mark.fab
class TestFabMpayTabbySupportingTransactions(object):
        def test_mpay_tabby_refund(self, page, data):
            tx = _mpay_tabby_payment(page, data)
            tx.capture_payment_id(BANK_NAME)
            tx.go_back_home(BANK_NAME)
            tx.open_transaction_portal(BANK_NAME)
            tx.go_to_transaction(BANK_NAME, "refund")
            tx.fill_refund_form(BANK_NAME, data)
            tx.select_mpay_project(BANK_NAME)
            tx.select_mpay_endpoint(BANK_NAME)
            tx.fill_captured_payment_id(BANK_NAME)
            tx.click_buy(BANK_NAME)

