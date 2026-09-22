"""
Skeleton test for the reports module - establishes the naming/marker
convention only. No demo backend exists yet, so this intentionally fails
with a clear NotImplementedError via ReportsPage._todo_action()
until real locators/steps are filled in (see that file's TODOs).
"""
import pytest

from src.common.pages.reports.reports_page import ReportsPage


@pytest.mark.wio
@pytest.mark.neoleap
@pytest.mark.ecentric
@pytest.mark.fab
@pytest.mark.oab
@pytest.mark.pinelabs
@pytest.mark.sanity
@pytest.mark.regression
class TestReports:
    def test_reports_placeholder(self, page):
        """TODO: replace with real Excel-driven test data + assertions,
        following the same ExcelUtil.get_sheet(...) + parametrize
        convention used in src/testcase/login/."""
        reports_page = ReportsPage(page)
        with pytest.raises(NotImplementedError):
            reports_page._todo_action(data={}, loc=None)
