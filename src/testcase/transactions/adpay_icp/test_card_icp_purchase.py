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
class TestFabAdpayTransactions(object):
        def test_adpay_icp_card_purchase(self, page, data):
            transactions = TransactionsPage(page)
            transactions.open_transaction_portal(BANK_NAME)
            transactions.go_to_transaction(BANK_NAME, "purchase")
            transactions.fill_icp_form(BANK_NAME, data)
            transactions.fill_icp_additional_service(BANK_NAME, data)
            transactions.fill_icp_vendor_one(BANK_NAME, data)
            transactions.fill_icp_vendor_two(BANK_NAME, data)
            transactions.click_buy(BANK_NAME)
            transactions.assert_adpay_summary(BANK_NAME)
            transactions.assert_adpay_currency_symbol(BANK_NAME)
            transactions.click_select_payment(BANK_NAME)
            transactions.add_card(BANK_NAME, data)
            transactions.select_card_month(BANK_NAME)
            transactions.select_card_year(BANK_NAME)
            transactions.pay_card(BANK_NAME)
            transactions.assert_adpay_payment_status(BANK_NAME)

