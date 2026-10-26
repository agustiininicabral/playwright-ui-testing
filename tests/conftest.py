from __future__ import annotations

import logging
import re
from collections.abc import Iterator
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from playwright.sync_api import Browser, Page


BASE_URL = "https://practicetestautomation.com"
LOGGER = logging.getLogger(__name__)


@pytest.fixture
def base_url() -> str:
    return BASE_URL


@pytest.fixture
def browser() -> Iterator[Browser]:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture
def page(browser: Browser) -> Iterator[Page]:
    page = browser.new_page()
    page.set_default_timeout(10_000)
    yield page
    page.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[object]) -> Iterator[None]:
    outcome = yield
    report = outcome.get_result()

    if report.when not in {"setup", "call", "teardown"} or not report.failed:
        return

    page = item.funcargs.get("page")
    if page is None:
        return

    try:
        if page.is_closed():
            LOGGER.warning(
                "Skipping screenshot for %s after %s failure: page is closed",
                item.nodeid,
                report.when,
            )
            return

        screenshots_dir = item.config.rootpath / "screenshots"
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        file_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", item.nodeid) + f"-{report.when}.png"
        page.screenshot(path=str(screenshots_dir / file_name), full_page=True)
    except Exception:
        LOGGER.warning(
            "Failed to capture screenshot for %s after %s failure",
            item.nodeid,
            report.when,
            exc_info=True,
        )
