"""
Skeleton test for the system_logs module - establishes the naming/marker
convention only. No demo backend exists yet, so this intentionally fails
with a clear NotImplementedError via SystemLogsPage._todo_action()
until real locators/steps are filled in (see that file's TODOs).
"""
import pytest

from src.common.pages.system_logs.system_logs_page import SystemLogsPage


@pytest.mark.wio
@pytest.mark.neoleap
@pytest.mark.ecentric
@pytest.mark.fab
@pytest.mark.oab
@pytest.mark.pinelabs
@pytest.mark.sanity
@pytest.mark.regression
class TestSystemLogs:
    def test_system_logs_placeholder(self, page):
        """TODO: replace with real Excel-driven test data + assertions,
        following the same ExcelUtil.get_sheet(...) + parametrize
        convention used in src/testcase/login/."""
        system_logs_page = SystemLogsPage(page)
        with pytest.raises(NotImplementedError):
            system_logs_page._todo_action(data={}, loc=None)
