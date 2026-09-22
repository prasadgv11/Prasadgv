"""
Skeleton test for the payments module - establishes the naming/marker
convention only. No demo backend exists yet, so this intentionally fails
with a clear NotImplementedError via PaymentsPage._todo_action()
until real locators/steps are filled in.
"""
import pytest

from src.common.pages.payments.payments_page import PaymentsPage


@pytest.mark.wio
@pytest.mark.neoleap
@pytest.mark.ecentric
@pytest.mark.fab
@pytest.mark.oab
@pytest.mark.pinelabs
@pytest.mark.sanity
@pytest.mark.regression
class TestPayments:
    def test_payments_placeholder(self, page):
        """TODO: replace with real Excel-driven test data + assertions."""
        payments_page = PaymentsPage(page)
        with pytest.raises(NotImplementedError):
            payments_page._todo_action(data={}, loc=None)
