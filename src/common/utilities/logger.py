"""
Shared colorized console logger. get_logger(name) mirrors the pattern of
get_logger(self.__class__.__name__) used throughout BasePage.
"""
import logging
import time

try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init(autoreset=True)
    _COLOR = True
except ImportError:
    _COLOR = False

    class _NoColor:
        def __getattr__(self, item):
            return ""

    Fore = _NoColor()
    Style = _NoColor()


class FrameworkLogger:
    def __init__(self, name: str):
        self._logger = logging.getLogger(name)
        if not self._logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("%(message)s"))
            self._logger.addHandler(handler)
        self._logger.setLevel(logging.INFO)
        self._logger.propagate = False

    def _ts(self) -> str:
        return time.strftime("%H:%M:%S")

    def info(self, message: str) -> None:
        self._logger.info(f"[{self._ts()}] [INFO] {message}")

    def pass_(self, message: str) -> None:
        c, r = (Fore.GREEN, Style.RESET_ALL) if _COLOR else ("", "")
        self._logger.info(f"{c}[{self._ts()}] [PASS] {message}{r}")

    def error(self, message: str) -> None:
        c, r = (Fore.RED, Style.RESET_ALL) if _COLOR else ("", "")
        self._logger.error(f"{c}[{self._ts()}] [ERROR] {message}{r}")

    def warn(self, message: str) -> None:
        c, r = (Fore.YELLOW, Style.RESET_ALL) if _COLOR else ("", "")
        self._logger.warning(f"{c}[{self._ts()}] [WARN] {message}{r}")


_loggers: dict[str, FrameworkLogger] = {}


def get_logger(name: str) -> FrameworkLogger:
    if name not in _loggers:
        _loggers[name] = FrameworkLogger(name)
    return _loggers[name]
