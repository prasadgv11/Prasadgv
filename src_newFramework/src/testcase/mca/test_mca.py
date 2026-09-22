"""
Skeleton test for the mca module - establishes the naming/marker
convention only. No demo backend exists yet, so this intentionally fails
with a clear NotImplementedError via McaPage._todo_action()
until real locators/steps are filled in (see that file's TODOs).
"""
import pytest

from src.common.pages.mca.mca_page import McaPage


@pytest.mark.wio
@pytest.mark.neoleap
@pytest.mark.ecentric
@pytest.mark.fab
@pytest.mark.oab
@pytest.mark.pinelabs
@pytest.mark.sanity
@pytest.mark.regression
class TestMca:
    def test_mca_placeholder(self, page):
        """TODO: replace with real Excel-driven test data + assertions,
        following the same ExcelUtil.get_sheet(...) + parametrize
        convention used in src/testcase/login/."""
        mca_page = McaPage(page)
        with pytest.raises(NotImplementedError):
            mca_page._todo_action(data={}, loc=None)
