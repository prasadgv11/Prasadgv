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

from src.testcase.transactions._transaction_helpers import (_complete_adpay_card)

@pytest.mark.sanity
@pytest.mark.regression
@pytest.mark.fab
class TestFabAdpayTransactions(object):
        def test_adpay_card_purchase(self, page, data):
            transactions = _complete_adpay_card(page, data, "purchase")
            transactions.capture_payment_id(BANK_NAME)
            transactions.go_back_home(BANK_NAME)
            transactions.open_transaction_portal(BANK_NAME)
            transactions.go_to_transaction(BANK_NAME, "inquiry")
            transactions.fill_inquiry_form(BANK_NAME, data)
            transactions.select_udf5(BANK_NAME, data.get("UDF5"))
            transactions.fill_captured_payment_id(BANK_NAME)
            transactions.click_buy(BANK_NAME)
            transactions.assert_transaction_result(BANK_NAME, data.get("ExpectedMessage"))

