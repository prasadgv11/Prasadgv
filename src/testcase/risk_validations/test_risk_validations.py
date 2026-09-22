"""
Skeleton test for the risk_validations module - establishes the naming/marker
convention only. No demo backend exists yet, so this intentionally fails
with a clear NotImplementedError via RiskValidationsPage._todo_action()
until real locators/steps are filled in (see that file's TODOs).
"""
import pytest

from src.common.pages.risk_validations.risk_validations_page import RiskValidationsPage


@pytest.mark.wio
@pytest.mark.neoleap
@pytest.mark.ecentric
@pytest.mark.fab
@pytest.mark.oab
@pytest.mark.pinelabs
@pytest.mark.sanity
@pytest.mark.regression
class TestRiskValidations:
    def test_risk_validations_placeholder(self, page):
        """TODO: replace with real Excel-driven test data + assertions,
        following the same ExcelUtil.get_sheet(...) + parametrize
        convention used in src/testcase/login/."""
        risk_validations_page = RiskValidationsPage(page)
        with pytest.raises(NotImplementedError):
            risk_validations_page._todo_action(data={}, loc=None)
