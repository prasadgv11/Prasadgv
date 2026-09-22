"""
ExtentReporter - a custom report generator styled after ExtentReports
(dashboard + expandable per-test step tree + inline screenshots), since
there is no official ExtentReports package for Python. Fully self-contained
single HTML file - no CLI tool needed to view it, unlike Allure.
"""
from __future__ import annotations

import base64
import contextvars
import html
import re
import time
from pathlib import Path

_current_test = contextvars.ContextVar("current_test", default=None)


class StepRecord:
    def __init__(self, message: str, level: str = "info", screenshot_path: str | None = None):
        self.timestamp = time.strftime("%H:%M:%S")
        self.message = message
        self.level = level
        self.screenshot_path = screenshot_path


class TestRecord:
    def __init__(self, name: str, tcid: str, suite: str = "General"):
        self.name = name
        self.tcid = tcid
        self.suite = suite
        self.steps: list[StepRecord] = []
        self.status = "pending"
        self._start = time.time()
        self.duration = 0.0

    def add_step(self, message: str, level: str = "info", screenshot_path: str | None = None) -> None:
        self.steps.append(StepRecord(message, level, screenshot_path))

    def finish(self, status: str) -> None:
        self.status = status
        self.duration = round(time.time() - self._start, 2)


class ExtentReporter:
    def __init__(self):
        self.tests: list[TestRecord] = []

    def start_test(self, name: str, tcid: str, suite: str = "General") -> TestRecord:
        """Starts a new test record. If a record for this exact TCID already
        exists (pytest-rerunfailures re-executing the same test after a
        failure), the earlier attempt's record is discarded first - only the
        FINAL attempt's outcome and steps are kept, matching what pytest's
        own terminal summary reports as the real result."""
        self.tests = [t for t in self.tests if t.tcid != tcid]
        record = TestRecord(name, tcid, suite)
        self.tests.append(record)
        _current_test.set(record)
        return record

    def log(self, message: str, level: str = "info", screenshot_path: str | None = None) -> None:
        record = _current_test.get()
        if record is not None:
            record.add_step(message, level, screenshot_path)

    def end_test(self, status: str) -> None:
        record = _current_test.get()
        if record is not None:
            record.finish(status)
        _current_test.set(None)

    # ------------------------------------------------------------------ #
    def generate_html(self, output_path: str, bank: str, env: str, tests: list["TestRecord"] | None = None,
                       title_suffix: str = "", screenshots_for_failed_only: bool = False) -> None:
        """Renders tests (defaults to everything recorded) into a self-contained
        Allure-style HTML report. Pass tests=<subset> to render a filtered
        report, or screenshots_for_failed_only=True to keep every test in the
        list but only embed screenshots for the ones that actually failed."""
        test_list = tests if tests is not None else self.tests
        total = len(test_list)
        passed = sum(1 for t in test_list if t.status == "passed")
        failed = sum(1 for t in test_list if t.status == "failed")
        skipped = sum(1 for t in test_list if t.status == "skipped")
        pass_pct = round((passed / total * 100) if total else 0, 1)

        STATUS_COLOR = {"passed": "#2e7d32", "failed": "#c62828", "skipped": "#f9a825"}
        LEVEL_COLOR = {"pass": "#2e7d32", "fail": "#c62828", "error": "#c62828", "info": "#444"}

        # Group tests by suite (class name) for the sidebar, Allure-style
        suites: dict[str, list[TestRecord]] = {}
        for t in test_list:
            suites.setdefault(t.suite, []).append(t)

        # CSS conic-gradient donut - no chart library needed, still self-contained
        segments = []
        angle = 0.0
        for status, count, color in (("passed", passed, STATUS_COLOR["passed"]),
                                      ("failed", failed, STATUS_COLOR["failed"]),
                                      ("skipped", skipped, STATUS_COLOR["skipped"])):
            if count == 0:
                continue
            frac = count / total if total else 0
            start_deg = angle * 360
            end_deg = (angle + frac) * 360
            segments.append(f"{color} {start_deg:.1f}deg {end_deg:.1f}deg")
            angle += frac
        donut_css = ", ".join(segments) if segments else "#ddd 0deg 360deg"

        sidebar_items = []
        content_sections = []
        for suite_name, tests in suites.items():
            suite_id = re.sub(r"[^a-zA-Z0-9]", "_", suite_name)
            suite_passed = sum(1 for t in tests if t.status == "passed")
            sidebar_items.append(
                f'<div class="suite-link" onclick="scrollToSuite(\'{suite_id}\')">'
                f'<span>{html.escape(suite_name)}</span>'
                f'<span class="suite-count">{suite_passed}/{len(tests)}</span>'
                f'</div>'
            )

            test_cards = []
            for t in tests:
                status_color = STATUS_COLOR.get(t.status, "#555")
                steps_html = []
                for s in t.steps:
                    level_color = LEVEL_COLOR.get(s.level, "#444")
                    img_html = ""
                    include_shot = s.screenshot_path and (not screenshots_for_failed_only or t.status == "failed")
                    if include_shot and Path(s.screenshot_path).exists():
                        try:
                            data = base64.b64encode(Path(s.screenshot_path).read_bytes()).decode("ascii")
                            img_html = (f'<br><img src="data:image/png;base64,{data}" '
                                        f'class="step-shot" onclick="event.stopPropagation();this.classList.toggle(\'zoomed\')">')
                        except Exception:
                            img_html = ""
                    steps_html.append(
                        f'<div class="step" style="color:{level_color};">'
                        f'<span class="step-ts">[{s.timestamp}]</span> {html.escape(s.message)}{img_html}'
                        f'</div>'
                    )
                test_cards.append(f"""
                <div class="test-card" data-status="{t.status}" data-search="{html.escape((t.tcid + ' ' + t.name).lower())}" style="border-left-color:{status_color};">
                  <div class="test-header" onclick="this.nextElementSibling.classList.toggle('open')">
                    <span class="status-badge" style="background:{status_color};">{t.status.upper()}</span>
                    <span class="tcid">{html.escape(t.tcid)}</span>
                    <span class="meta">{t.duration}s &middot; {len(t.steps)} steps</span>
                  </div>
                  <div class="steps">
                    {''.join(steps_html)}
                  </div>
                </div>
                """)
            content_sections.append(f"""
            <div class="suite-section" id="suite_{suite_id}">
              <h2 class="suite-title">{html.escape(suite_name)}</h2>
              {''.join(test_cards)}
            </div>
            """)

        html_doc = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Test Execution Report{html.escape(title_suffix)} - {html.escape(bank.upper())}</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{ font-family: 'Segoe UI', Roboto, Arial, sans-serif; background:#f0f2f5; margin:0; color:#1a1a1a; }}
  .layout {{ display:flex; min-height:100vh; }}

  /* Sidebar */
  .sidebar {{ width:240px; background:#1e2530; color:#cfd8e3; flex-shrink:0; padding:20px 0; }}
  .sidebar h3 {{ padding:0 20px; font-size:12px; text-transform:uppercase; letter-spacing:1px; color:#8b96a5; margin:20px 0 8px; }}
  .suite-link {{ padding:10px 20px; cursor:pointer; display:flex; justify-content:space-between; font-size:14px; }}
  .suite-link:hover {{ background:#2a3242; }}
  .suite-count {{ color:#8b96a5; font-size:12px; }}
  .brand {{ padding:0 20px 20px; font-size:18px; font-weight:700; color:#fff; border-bottom:1px solid #2a3242; margin-bottom:10px; }}

  /* Main */
  .main {{ flex:1; padding:24px 32px; }}
  .top-bar {{ display:flex; justify-content:space-between; align-items:center; margin-bottom:20px; }}
  .top-bar .meta-line {{ color:#666; font-size:13px; }}

  /* Dashboard widgets */
  .widgets {{ display:flex; gap:20px; margin-bottom:24px; }}
  .widget {{ background:#fff; border-radius:8px; padding:20px; box-shadow:0 1px 4px rgba(0,0,0,.08); }}
  .donut-widget {{ display:flex; align-items:center; gap:20px; }}
  .donut {{ width:110px; height:110px; border-radius:50%; background: conic-gradient({donut_css}); position:relative; flex-shrink:0; }}
  .donut::after {{ content:''; position:absolute; top:15px; left:15px; right:15px; bottom:15px; background:#fff; border-radius:50%; }}
  .donut-center {{ position:absolute; top:0; left:0; width:100%; height:100%; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:18px; z-index:2; }}
  .stats-widget {{ display:flex; gap:28px; align-items:center; }}
  .stat .num {{ font-size:26px; font-weight:700; }}
  .stat .label {{ color:#777; font-size:12px; text-transform:uppercase; letter-spacing:.5px; }}
  .passed-num {{ color:#2e7d32; }}
  .failed-num {{ color:#c62828; }}
  .skipped-num {{ color:#f9a825; }}

  /* Filters */
  .toolbar {{ display:flex; gap:10px; margin-bottom:16px; align-items:center; }}
  .filter-btn {{ border:1px solid #ddd; background:#fff; padding:6px 14px; border-radius:16px; cursor:pointer; font-size:13px; }}
  .filter-btn.active {{ background:#1e2530; color:#fff; border-color:#1e2530; }}
  .search-box {{ flex:1; max-width:280px; padding:7px 12px; border:1px solid #ddd; border-radius:16px; font-size:13px; }}

  /* Suite sections & test cards */
  .suite-title {{ font-size:16px; margin:24px 0 10px; color:#333; }}
  .test-card {{ background:#fff; border-left:4px solid #ccc; border-radius:6px; margin:8px 0; box-shadow:0 1px 3px rgba(0,0,0,.08); overflow:hidden; }}
  .test-header {{ display:flex; align-items:center; gap:12px; padding:12px 16px; cursor:pointer; }}
  .status-badge {{ color:#fff; font-size:11px; font-weight:700; padding:2px 8px; border-radius:4px; letter-spacing:.5px; }}
  .tcid {{ font-weight:700; color:#1e2530; }}
  .test-name {{ color:#555; flex:1; }}
  .meta {{ color:#999; font-size:12px; }}
  .steps {{ display:none; padding:0 16px 14px 16px; border-top:1px solid #f0f0f0; }}
  .steps.open {{ display:block; }}
  .step {{ padding:5px 0; font-size:13px; }}
  .step-ts {{ color:#999; margin-right:6px; }}
  .step-shot {{ max-width:340px; border:1px solid #ddd; border-radius:4px; margin-top:6px; cursor:zoom-in; display:block; }}
  .step-shot.zoomed {{ max-width:90%; cursor:zoom-out; }}
</style>
</head>
<body>
  <div class="layout">
    <div class="sidebar">
      <div class="brand">Hybrid Playwright Python Framework</div>
      <h3>Suites</h3>
      {''.join(sidebar_items)}
    </div>
    <div class="main">
      <div class="top-bar">
        <div>
          <h1 style="margin:0;">Test Execution Report{html.escape(title_suffix)}</h1>
          <div class="meta-line">Bank: <b>{html.escape(bank.upper())}</b> &nbsp;|&nbsp; Env: <b>{html.escape(env)}</b> &nbsp;|&nbsp; Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>
      </div>

      <div class="widgets">
        <div class="widget donut-widget">
          <div style="position:relative;">
            <div class="donut"></div>
            <div class="donut-center">{pass_pct}%</div>
          </div>
          <div class="stats-widget">
            <div class="stat"><div class="num">{total}</div><div class="label">Total</div></div>
            <div class="stat"><div class="num passed-num">{passed}</div><div class="label">Passed</div></div>
            <div class="stat"><div class="num failed-num">{failed}</div><div class="label">Failed</div></div>
            <div class="stat"><div class="num skipped-num">{skipped}</div><div class="label">Skipped</div></div>
          </div>
        </div>
      </div>

      <div class="toolbar">
        <div class="filter-btn active" data-filter="all" onclick="setFilter('all', this)">All</div>
        <div class="filter-btn" data-filter="passed" onclick="setFilter('passed', this)">Passed</div>
        <div class="filter-btn" data-filter="failed" onclick="setFilter('failed', this)">Failed</div>
        <div class="filter-btn" data-filter="skipped" onclick="setFilter('skipped', this)">Skipped</div>
        <input class="search-box" placeholder="Search TCID or test name..." oninput="applySearch(this.value)">
      </div>

      <div id="content">
        {''.join(content_sections) if content_sections else '<p style="color:#888;padding:20px;">No tests match this report.</p>'}
      </div>
    </div>
  </div>

<script>
  let currentFilter = 'all';
  let currentSearch = '';

  function setFilter(filter, el) {{
    currentFilter = filter;
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    el.classList.add('active');
    applyFilters();
  }}

  function applySearch(value) {{
    currentSearch = value.toLowerCase();
    applyFilters();
  }}

  function applyFilters() {{
    document.querySelectorAll('.test-card').forEach(card => {{
      const statusOk = currentFilter === 'all' || card.getAttribute('data-status') === currentFilter;
      const searchOk = !currentSearch || card.getAttribute('data-search').includes(currentSearch);
      card.style.display = (statusOk && searchOk) ? '' : 'none';
    }});
  }}

  function scrollToSuite(suiteId) {{
    const el = document.getElementById('suite_' + suiteId);
    if (el) el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
  }}
</script>
</body>
</html>"""
        Path(output_path).write_text(html_doc, encoding="utf-8")

    def generate_failure_screenshots_report(self, output_path: str, bank: str, env: str) -> None:
        """
        Second report, SAME layout as the full report and containing every
        test (pass/fail/skip) - but only the failed tests' steps carry
        embedded screenshots. Passed/skipped steps show text only, so the
        file stays focused on what actually needs investigating without
        losing the full pass/fail picture.
        """
        self.generate_html(
            output_path, bank, env,
            tests=self.tests,
            title_suffix=" - Failure Screenshots Only",
            screenshots_for_failed_only=True,
        )


# Module-level singleton used across the whole test session
reporter = ExtentReporter()
