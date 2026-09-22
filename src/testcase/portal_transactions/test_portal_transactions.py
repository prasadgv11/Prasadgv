"""
Skeleton test for the portal_transactions module - establishes the naming/marker
convention only. No demo backend exists yet, so this intentionally fails
with a clear NotImplementedError via PortalTransactionsPage._todo_action()
until real locators/steps are filled in (see that file's TODOs).
"""
import pytest

from src.common.pages.portal_transactions.portal_transactions_page import PortalTransactionsPage


@pytest.mark.wio
@pytest.mark.neoleap
@pytest.mark.ecentric
@pytest.mark.fab
@pytest.mark.oab
@pytest.mark.pinelabs
@pytest.mark.sanity
@pytest.mark.regression
class TestPortalTransactions:
    def test_portal_transactions_placeholder(self, page):
        """TODO: replace with real Excel-driven test data + assertions,
        following the same ExcelUtil.get_sheet(...) + parametrize
        convention used in src/testcase/login/."""
        portal_transactions_page = PortalTransactionsPage(page)
        with pytest.raises(NotImplementedError):
            portal_transactions_page._todo_action(data={}, loc=None)
