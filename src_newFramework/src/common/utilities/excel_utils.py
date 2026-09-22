"""
ExcelUtil.get_sheet(fileName, sheetName) - matches the real convention:
opens src/banks/<current-bank>/testdata/<fileName>.xlsx, reads sheetName,
returns the raw rows as a list of dicts. No TestCase-column filtering here
- the sheet IS the scenario (e.g. sheet "ValidLogin" holds only valid-login
rows). Bank is resolved automatically from config.yaml, never passed in.
"""
from __future__ import annotations

import pathlib
from typing import Any

import openpyxl

from src.common.utilities.config_loader import ConfigManager

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[3]
BANKS_DIR = PROJECT_ROOT / "src" / "banks"


class ExcelDataError(Exception):
    pass


class ExcelUtil:
    @staticmethod
    def _current_bank() -> str:
        return ConfigManager.load_bank_config()["bank"]

    @staticmethod
    def _workbook_path(file_name: str, bank: str | None = None) -> pathlib.Path:
        bank = bank or ExcelUtil._current_bank()
        path = BANKS_DIR / bank / "testdata" / f"{file_name}.xlsx"
        if not path.exists():
            raise ExcelDataError(f"Test data file not found: {path}")
        return path

    @staticmethod
    def get_sheet(file_name: str, sheet_name: str) -> list[dict[str, Any]]:
        """Returns one dict per row (column headers as keys) for the
        current bank's <file_name>.xlsx / sheet_name."""
        path = ExcelUtil._workbook_path(file_name)
        wb = openpyxl.load_workbook(path, data_only=True)
        if sheet_name not in wb.sheetnames:
            raise ExcelDataError(f"Sheet '{sheet_name}' not found in {path}. Available: {wb.sheetnames}")
        ws = wb[sheet_name]
        rows = list(ws.iter_rows(values_only=True))
        if not rows:
            return []
        headers = [str(h).strip() if h is not None else "" for h in rows[0]]
        data = []
        for row in rows[1:]:
            if all(cell is None for cell in row):
                continue
            data.append({headers[i]: row[i] for i in range(len(headers))})
        return data

    # ------------------------------------------------------------------ #
    # Coverage / uniqueness helpers - scan every .xlsx file for the bank
    # ------------------------------------------------------------------ #
    @staticmethod
    def all_tcids_for_bank(bank: str | None = None) -> dict[str, list[str]]:
        """Returns {"<file>::<sheet>": [tcid, ...]} across every workbook
        under that bank's testdata/ folder."""
        bank = bank or ExcelUtil._current_bank()
        testdata_dir = BANKS_DIR / bank / "testdata"
        result: dict[str, list[str]] = {}
        if not testdata_dir.exists():
            return result
        for xlsx_path in sorted(testdata_dir.glob("*.xlsx")):
            if xlsx_path.name.startswith("~$"):
                continue
            file_name = xlsx_path.stem
            wb = openpyxl.load_workbook(xlsx_path, read_only=True)
            for sheet in wb.sheetnames:
                rows = ExcelUtil.get_sheet(file_name, sheet)
                key = f"{file_name}::{sheet}"
                result[key] = [str(r.get("TCID")) for r in rows if r.get("TCID")]
        return result

    @staticmethod
    def check_tcid_uniqueness(bank: str | None = None) -> None:
        """Raises ExcelDataError if any TCID is duplicated across every
        sheet in every workbook for this bank."""
        seen: dict[str, str] = {}
        for key, tcids in ExcelUtil.all_tcids_for_bank(bank).items():
            for tcid in tcids:
                if tcid in seen:
                    raise ExcelDataError(
                        f"Duplicate TCID '{tcid}' found in '{key}' "
                        f"(already used in '{seen[tcid]}')"
                    )
                seen[tcid] = key
