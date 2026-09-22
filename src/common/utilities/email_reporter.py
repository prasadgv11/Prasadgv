"""
EmailReporter - sends the test execution report (and failures-only report)
via email once a run completes, by automating the local Outlook desktop
application (pywin32 COM) instead of connecting to an SMTP server directly.

This means: no SMTP host/port/credentials needed at all - it reuses
whichever account is already signed into Outlook on the machine running the
tests. Requires `pip install pywin32` AND a working Outlook desktop
installation - Windows-only, will not work on Linux/macOS or in a headless
CI runner without Outlook installed and configured.

A failed email send NEVER raises or fails the test run - it's a best-effort
notification, logged if it doesn't work, nothing more.
"""
from __future__ import annotations

from pathlib import Path

from src.common.utilities.logger import get_logger

logger = get_logger("EmailReporter")


def send_report_email(
    recipients: list[str],
    subject: str,
    body_html: str,
    attachments: list[str],
) -> bool:
    """
    Sends an email with the given HTML report(s) attached, by driving the
    local Outlook desktop application via COM automation (pywin32).
    Returns True/False - never raises, so a missing/misconfigured Outlook
    install can never take down the test run itself.
    """
    if not recipients:
        logger.warn("No email recipients configured - skipping report email")
        return False

    try:
        import win32com.client
    except ImportError:
        logger.error(
            "Failed to send report email: pywin32 not installed "
            "(pip install pywin32) - Outlook COM automation requires it"
        )
        return False

    try:
        outlook = win32com.client.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)  # 0 = olMailItem
        mail.Subject = subject
        mail.HTMLBody = body_html
        mail.To = "; ".join(recipients)

        attached_count = 0
        for path_str in attachments:
            path = Path(path_str)
            if not path.exists():
                logger.warn(f"Attachment not found, skipping: {path}")
                continue
            mail.Attachments.Add(str(path.resolve()))
            attached_count += 1

        mail.Send()
        logger.info(f"Report email sent via Outlook to: {', '.join(recipients)} ({attached_count} attachment(s))")
        return True
    except Exception as e:
        logger.error(f"Failed to send report email via Outlook: {e}")
        return False


def build_summary_body(bank: str, env: str, total: int, passed: int, failed: int, skipped: int) -> str:
    """Small HTML summary used as the email body - reports themselves are attached."""
    pass_pct = round((passed / total * 100) if total else 0, 1)
    return f"""
    <html><body style="font-family:Segoe UI,Arial,sans-serif;">
      <h2>Test Execution Summary</h2>
      <p><b>Bank:</b> {bank.upper()} &nbsp; <b>Env:</b> {env}</p>
      <table style="border-collapse:collapse;">
        <tr><td style="padding:4px 12px;">Total</td><td style="padding:4px 12px;"><b>{total}</b></td></tr>
        <tr><td style="padding:4px 12px;color:#2e7d32;">Passed</td><td style="padding:4px 12px;"><b>{passed}</b></td></tr>
        <tr><td style="padding:4px 12px;color:#c62828;">Failed</td><td style="padding:4px 12px;"><b>{failed}</b></td></tr>
        <tr><td style="padding:4px 12px;color:#f9a825;">Skipped</td><td style="padding:4px 12px;"><b>{skipped}</b></td></tr>
        <tr><td style="padding:4px 12px;">Pass %</td><td style="padding:4px 12px;"><b>{pass_pct}%</b></td></tr>
      </table>
      <p>Full report and failures-only report are attached.</p>
    </body></html>
    """
