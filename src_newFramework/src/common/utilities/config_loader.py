"""
Config loader for the framework.
Single source of truth for project paths, config.yaml, and per-bank
credentials.yaml resolution.
"""
from __future__ import annotations

import pathlib
from typing import Any

import yaml

# This file lives at: <project_root>/src/common/utilities/config_loader.py
# parents[0]=utilities, [1]=common, [2]=src  -> lands exactly on the src/ folder
SRC_ROOT = pathlib.Path(__file__).resolve().parents[2]
PROJECT_ROOT = SRC_ROOT.parent

ROOT_CONFIG_PATH = SRC_ROOT / "config.yaml"
BANKS_DIR = SRC_ROOT / "banks"

REQUIRED_ROOT_KEYS = ["bank", "env", "browser", "headless", "test_type"]
REQUIRED_BANK_KEYS = ["url", "username", "password"]


class ConfigError(Exception):
    """Raised when config.yaml or a bank's credentials file is missing/invalid."""


def _load_yaml(path: pathlib.Path) -> dict[str, Any]:
    if not path.exists():
        raise ConfigError(f"Config file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _resolve_url(raw_url: str) -> str:
    """http(s)/file URLs pass through; anything else is treated as a path
    relative to project root (used for the bundled demo pages) and
    converted to a file:// URI."""
    if raw_url.startswith(("http://", "https://", "file://")):
        return raw_url
    local_path = (PROJECT_ROOT / raw_url).resolve()
    if not local_path.exists():
        raise ConfigError(f"Local demo page not found: {local_path}")
    return local_path.as_uri()


def _resolve_env_portal(bank_cfg_env: dict[str, Any], portal: str) -> dict[str, Any]:
    """
    Returns the flat {url, username, password[, payment_url]} dict for the
    requested portal. Supports two credentials.yaml shapes per env:
      - flat (most banks, single login surface): {url, username, password, ...}
        -> returned as-is regardless of `portal` (single-portal bank)
      - nested (a bank with multiple login portals under one bank, e.g.
        admin/bank/merchant): {portals: {admin: {...}, bank: {...},
        merchant: {...}}} -> the sub-dict for the requested portal is
        returned; raises ConfigError if that portal isn't defined
    """
    if "portals" in bank_cfg_env:
        portals = bank_cfg_env["portals"]
        if portal not in portals:
            raise ConfigError(
                f"portal '{portal}' not defined. Available portals: {list(portals.keys())}"
            )
        return portals[portal]
    return bank_cfg_env


def available_banks() -> list[str]:
    """A folder under src/banks/ only counts as a real bank if it has its
    own <name>_credentials.yaml - excludes __pycache__ and similar."""
    if not BANKS_DIR.exists():
        return []
    return sorted(
        p.name for p in BANKS_DIR.iterdir()
        if p.is_dir() and (p / f"{p.name}_credentials.yaml").exists()
    )


class ConfigManager:
    _cached: dict[str, Any] | None = None

    @classmethod
    def load_bank_config(cls, force_reload: bool = False) -> dict[str, Any]:
        """Loads + validates config.yaml, loads the matching bank's
        credentials file, resolves env-specific url/username/password,
        returns one merged dict. Cached after first call in a process."""
        if cls._cached is not None and not force_reload:
            return cls._cached

        root_cfg = _load_yaml(ROOT_CONFIG_PATH)
        missing = [k for k in REQUIRED_ROOT_KEYS if k not in root_cfg]
        if missing:
            raise ConfigError(f"config.yaml is missing required keys: {missing}")

        bank = root_cfg["bank"]
        env = root_cfg["env"]

        banks_found = available_banks()
        if bank not in banks_found:
            raise ConfigError(
                f"bank '{bank}' has no folder under src/banks/. "
                f"Available banks: {banks_found or 'NONE FOUND'}"
            )

        credentials_path = BANKS_DIR / bank / f"{bank}_credentials.yaml"
        bank_cfg_all = _load_yaml(credentials_path)

        if env not in bank_cfg_all:
            raise ConfigError(
                f"env '{env}' not found in {credentials_path}. "
                f"Available envs: {list(bank_cfg_all.keys())}"
            )

        # Default/customer portal ("bank") - used by anything that doesn't
        # care about portal at all (payments, non-portal banks).
        bank_cfg = _resolve_env_portal(bank_cfg_all[env], "bank")
        missing_bank_keys = [k for k in REQUIRED_BANK_KEYS if k not in bank_cfg]
        if missing_bank_keys:
            raise ConfigError(
                f"{credentials_path} [{env}] is missing required keys: {missing_bank_keys}"
            )

        merged = dict(root_cfg)
        merged["url"] = _resolve_url(bank_cfg["url"])
        merged["username"] = bank_cfg["username"]
        merged["password"] = bank_cfg["password"]
        if "payment_url" in bank_cfg:
            merged["payment_url"] = _resolve_url(bank_cfg["payment_url"])

        cls._cached = merged
        return merged

    @classmethod
    def load_portal_config(cls, portal: str) -> dict[str, Any]:
        """
        Resolves url/username/password (+ payment_url if present) for a
        SPECIFIC portal of the currently configured bank/env. Used by
        LoginPage when an Excel row's Portal column names a portal other
        than the default "bank" one - which portal to hit is data-driven
        per test row, not selected in config.yaml, so all portals for a
        bank run together within one sanity/regression execution.
        Safe to call with portal="bank" for single-portal banks too.
        """
        root_cfg = _load_yaml(ROOT_CONFIG_PATH)
        bank = root_cfg["bank"]
        env = root_cfg["env"]

        credentials_path = BANKS_DIR / bank / f"{bank}_credentials.yaml"
        bank_cfg_all = _load_yaml(credentials_path)
        if env not in bank_cfg_all:
            raise ConfigError(f"env '{env}' not found in {credentials_path}")

        portal_cfg = _resolve_env_portal(bank_cfg_all[env], portal)
        missing = [k for k in REQUIRED_BANK_KEYS if k not in portal_cfg]
        if missing:
            raise ConfigError(
                f"{credentials_path} [{env}][{portal}] is missing required keys: {missing}"
            )

        resolved = dict(portal_cfg)
        resolved["url"] = _resolve_url(portal_cfg["url"])
        if "payment_url" in portal_cfg:
            resolved["payment_url"] = _resolve_url(portal_cfg["payment_url"])
        return resolved

    @classmethod
    def get(cls, key: str) -> Any:
        return cls.load_bank_config().get(key)

    @classmethod
    def load_config(cls) -> dict[str, Any]:
        return cls.load_bank_config()
