"""
Skeleton test for the transactions_configurations module - establishes the naming/marker
convention only. No demo backend exists yet, so this intentionally fails
with a clear NotImplementedError via TransactionsConfigurationsPage._todo_action()
until real locators/steps are filled in (see that file's TODOs).
"""
import pytest

from src.common.pages.transactions_configurations.transactions_configurations_page import TransactionsConfigurationsPage


@pytest.mark.wio
@pytest.mark.neoleap
@pytest.mark.ecentric
@pytest.mark.fab
@pytest.mark.oab
@pytest.mark.pinelabs
@pytest.mark.sanity
@pytest.mark.regression
class TestTransactionsConfigurations:
    def test_transactions_configurations_placeholder(self, page):
        """TODO: replace with real Excel-driven test data + assertions,
        following the same ExcelUtil.get_sheet(...) + parametrize
        convention used in src/testcase/login/."""
        transactions_configurations_page = TransactionsConfigurationsPage(page)
        with pytest.raises(NotImplementedError):
            transactions_configurations_page._todo_action(data={}, loc=None)
