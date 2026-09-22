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

from src.testcase.transactions._transaction_helpers import (_mpay_card_payment)

@pytest.mark.sanity
@pytest.mark.regression
@pytest.mark.fab
class TestFabMpayCardSupportingTransactions(object):
        def test_mpay_card_authorization(self, page, data):
            tx = _mpay_card_payment(page, data, "authorization")
            tx.capture_payment_id(BANK_NAME)

