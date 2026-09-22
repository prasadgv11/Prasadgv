"""
Skeleton test for the ecentric_specific module - establishes the naming/marker
convention only. No demo backend exists yet, so this intentionally fails
with a clear NotImplementedError via EcentricSpecificPage._todo_action()
until real locators/steps are filled in (see that file's TODOs).
"""
import pytest

from src.common.pages.ecentric_specific.ecentric_specific_page import EcentricSpecificPage


@pytest.mark.wio
@pytest.mark.neoleap
@pytest.mark.ecentric
@pytest.mark.fab
@pytest.mark.oab
@pytest.mark.pinelabs
@pytest.mark.sanity
@pytest.mark.regression
class TestEcentricSpecific:
    def test_ecentric_specific_placeholder(self, page):
        """TODO: replace with real Excel-driven test data + assertions,
        following the same ExcelUtil.get_sheet(...) + parametrize
        convention used in src/testcase/login/."""
        ecentric_specific_page = EcentricSpecificPage(page)
        with pytest.raises(NotImplementedError):
            ecentric_specific_page._todo_action(data={}, loc=None)
