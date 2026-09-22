"""
UserAdministrationPage - real, working demo implementation for demobank,
covering text fields, dropdowns, radio buttons, a native date picker, and
native alert/confirm dialogs, so the framework's handling of every one of
those UI field types can be verified end-to-end (not just login form
fields). Other banks still need their own locators/steps added to
_bank_config() before this page will work against them - demobank is the
only bank wired up so far, purely to prove the framework itself works.
"""
from src.common.base.base_page import BasePage
from src.banks.demobank.locators.user_creation_locators import DemobankUserCreationLocators


class UserAdministrationPage(BasePage):
    def __init__(self, page):
        super().__init__(page, module_name="UserAdministration")

    def _bank_config(self):
        """TODO: add an entry per real bank once its user-creation
        locators/steps exist - same pattern as LoginPage._bank_config().
        {
            "wio": (self._create_user_standard, ...),
            "neoleap": (self._create_user_standard, ...),
            "ecentric": (self._create_user_standard, ...),
            "fab": (self._create_user_standard, ...),
            "oab": (self._create_user_standard, ...),
            "pinelabs": (self._create_user_standard, ...),
        }
        """
        return {
            "demobank": (self._create_user_standard, DemobankUserCreationLocators),
        }

    def create_user(self, data: dict) -> None:
        handler, loc_cls = self._bank_config().get(self.bank, (None, None))
        if handler is None:
            raise NotImplementedError(
                f"UserAdministrationPage.create_user() has no steps implemented yet for bank '{self.bank}'"
            )
        handler(data, loc_cls)

    # ------------------------------------------------------------------ #
    # Field pattern - demonstrates every requested UI element type:
    # text fields, dropdowns, radio buttons, a native date picker, and
    # native alert/confirm dialogs.
    # ------------------------------------------------------------------ #
    def _create_user_standard(self, data: dict, loc) -> None:
        self.fill_by_locator(loc.first_name_field, data["FirstName"], "First Name")
        self.fill_by_locator(loc.last_name_field, data["LastName"], "Last Name")
        self.fill_by_locator(loc.email_field, data["Email"], "Email")
        self.fill_by_locator(loc.phone_field, data["Phone"], "Phone")
        self.fill_by_locator(loc.employee_id_field, data["EmployeeId"], "Employee ID")
        self.fill_by_locator(loc.address_field, data["Address"], "Address")
        self.fill_by_locator(loc.city_field, data["City"], "City")
        self.fill_by_locator(loc.postal_code_field, data["PostalCode"], "Postal Code")

        self.select_by_locator(loc.department_dropdown, data["Department"], "Department")
        self.select_by_locator(loc.role_dropdown, data["Role"], "Role")
        self.select_by_locator(loc.country_dropdown, data["Country"], "Country")

        # Radio buttons - dynamic dict lookup rather than hardcoding one
        # option, so the value actually comes from the Excel row.
        gender_radios = {
            "Male": loc.gender_male_radio,
            "Female": loc.gender_female_radio,
        }
        self.select_radio_by_locator(gender_radios[data["Gender"]], "Gender")

        account_type_radios = {
            "Savings": loc.account_type_savings_radio,
            "Current": loc.account_type_current_radio,
        }
        self.select_radio_by_locator(account_type_radios[data["AccountType"]], "Account Type")

        self.select_date_native(loc.date_of_joining_field, data["DateOfJoining"], "Date of Joining")

        # The demo form fires alert() if a required field is empty, or
        # confirm() on a valid submit - accept_dialog() registers a
        # ONE-TIME handler for whichever native dialog fires next, and
        # must be called BEFORE the click that can trigger it.
        self.accept_dialog()
        self.click_by_locator(loc.submit_button, "Submit button")

    # ------------------------------------------------------------------ #
    # Assertions
    # ------------------------------------------------------------------ #
    def _locators(self):
        _, loc_cls = self._bank_config().get(self.bank, (None, None))
        if loc_cls is None:
            raise ValueError(f"No locators defined for bank '{self.bank}'")
        return loc_cls

    def assert_user_created_message(self, expected_message: str) -> None:
        loc_cls = self._locators()
        self.assert_text(self.locator(loc_cls.success_message), expected_message, "User created message")
