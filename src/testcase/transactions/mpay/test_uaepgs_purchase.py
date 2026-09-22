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
        def test_mpay_uaepgs(self, page, data):
            transactions = TransactionsPage(page)
            transactions.open_transaction_portal(BANK_NAME)
            transactions.go_to_transaction(BANK_NAME, "purchase")
            transactions.fill_transaction_form(BANK_NAME, data)
            transactions.select_mpay_project(BANK_NAME)
            transactions.select_mpay_endpoint(BANK_NAME)
            transactions.fill_mpay_request_fields(BANK_NAME, data)
            transactions.click_buy(BANK_NAME)
            transactions.select_direct_debit(BANK_NAME)
            transactions.select_direct_debit_details(BANK_NAME, data)
            transactions.submit_direct_debit(BANK_NAME)
            transactions.fill_direct_debit_response(BANK_NAME, data)
            transactions.generate_hash_and_return_to_pg(BANK_NAME)

