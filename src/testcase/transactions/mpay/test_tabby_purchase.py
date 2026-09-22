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
        def test_mpay_tabby(self, page, data):
            transactions = TransactionsPage(page)
            transactions.open_transaction_portal(BANK_NAME)
            transactions.go_to_transaction(BANK_NAME, "purchase")
            transactions.fill_transaction_form(BANK_NAME, data)
            transactions.select_mpay_project(BANK_NAME)
            transactions.select_mpay_endpoint(BANK_NAME)
            transactions.fill_mpay_request_fields(BANK_NAME, data)
            transactions.click_buy(BANK_NAME)
            transactions.select_tabby(BANK_NAME)
            transactions.click_mpay_pay(BANK_NAME)
            transactions.fill_tabby_details(BANK_NAME, data, arabic=data.get("Language") == "AR")
            transactions.select_tabby_installment(BANK_NAME)
            transactions.assert_mpay_payment_status(BANK_NAME)

