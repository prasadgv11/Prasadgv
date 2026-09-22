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

from src.testcase.transactions._transaction_helpers import (_prepare_adpay)

@pytest.mark.sanity
@pytest.mark.regression
@pytest.mark.fab
class TestFabAdpayTransactions(object):
        def test_adpay_uaepgs_purchase(self, page, data):
            transactions = _prepare_adpay(page, data, "purchase")
            transactions.assert_adpay_summary(BANK_NAME)
            transactions.select_direct_debit(BANK_NAME)
            transactions.select_direct_debit_details(BANK_NAME, data)
            transactions.submit_direct_debit(BANK_NAME)
            transactions.fill_direct_debit_response(BANK_NAME, data)
            transactions.generate_hash_and_return_to_pg(BANK_NAME)

