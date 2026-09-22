"""
PaymentsPage - lightweight skeleton for the payments module.

Mirrors LoginPage's conventions (BasePage subclass, module_name passed to
super().__init__(), bank-aware via self.bank). No demo backend exists for
this module yet - every action method below is a TODO placeholder, not
verified against a live page.
"""
from src.common.base.base_page import BasePage


class PaymentsPage(BasePage):
    def __init__(self, page):
        super().__init__(page, module_name="Payments")

    def _bank_config(self):
        """TODO: map each bank (and portal, if needed - see
        LoginPage._portal_config()) to its (handler, locator_class)."""
        return {}

    def _todo_action(self, data: dict, loc) -> None:
        """TODO: replace with the real steps for this module."""
        raise NotImplementedError(
            f"{self.__class__.__name__} has no steps implemented yet for bank '{self.bank}'"
        )
