from __future__ import annotations

from datetime import datetime
from pathlib import Path
import pytest


def _save_screenshot(driver, item_name: str) -> str | None:
    try:
        outdir = Path("tests/ui/screenshots")
        outdir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        fname = outdir / f"{item_name}-{ts}.png"
        driver.save_screenshot(str(fname))
        return str(fname)
    except Exception:
        return None


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    if report.failed:
        drv = item.funcargs.get("driver")
        if drv is None:
            return
        saved = _save_screenshot(drv, item.name)
        if saved:
            report.longrepr = f"{report.longrepr}\n[screenshot saved to] {saved}"
