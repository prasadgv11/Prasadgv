"""
SystemLogsPage - lightweight skeleton for the system_logs module.

Mirrors LoginPage's conventions (BasePage subclass, module_name passed to
super().__init__(), bank-aware via self.bank) so real locators/steps can
be filled in per bank the same way LoginPage's _bank_config()/
_portal_config() dispatch does. No demo backend exists for this module
yet - every action method below is a TODO placeholder, not verified
against a live page. Follow LoginPage's pattern-method convention: one
method per distinct field/flow layout, reused across any bank that
shares it, rather than one method per bank.
"""
from src.common.base.base_page import BasePage


class SystemLogsPage(BasePage):
    def __init__(self, page):
        super().__init__(page, module_name="SystemLogs")

    def _bank_config(self):
        """TODO: map each bank (and portal, if this module needs one -
        see LoginPage._portal_config()) to its (handler, locator_class).
        Add an entry per bank once real locators exist for this module:
        {
        #     "wio": (self._todo_action, ...),
        #     "neoleap": (self._todo_action, ...),
        #     "ecentric": (self._todo_action, ...),
        #     "fab": (self._todo_action, ...),
        #     "oab": (self._todo_action, ...),
        #     "pinelabs": (self._todo_action, ...),
        }
        """
        return {}

    def _todo_action(self, data: dict, loc) -> None:
        """TODO: replace with the real steps for this module."""
        raise NotImplementedError(
            f"{self.__class__.__name__} has no steps implemented yet for bank '{self.bank}'"
        )
