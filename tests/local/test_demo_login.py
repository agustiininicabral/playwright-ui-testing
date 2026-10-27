from pathlib import Path

import pytest


FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "demo_login.html"


@pytest.fixture
def demo_login_html() -> str:
    return FIXTURE.read_text(encoding="utf-8")


@pytest.mark.local_browser
def test_bundled_login_fixture_has_accessible_form(page, demo_login_html: str) -> None:
    from playwright.sync_api import expect

    page.set_content(demo_login_html)

    expect(page).to_have_title("Demo Login Fixture")
    expect(page.get_by_role("heading", name="Test Login")).to_be_visible()
    expect(page.get_by_label("Username")).to_be_visible()
    expect(page.get_by_label("Password")).to_be_visible()
    expect(page.get_by_role("button", name="Submit")).to_be_visible()


@pytest.mark.local_browser
def test_bundled_login_fixture_accepts_demo_credentials(
    page, demo_login_html: str
) -> None:
    from playwright.sync_api import expect

    page.set_content(demo_login_html)
    page.get_by_label("Username").fill("student")
    page.get_by_label("Password").fill("Password123")
    page.get_by_role("button", name="Submit").click()

    expect(page.get_by_role("heading", name="Logged In Successfully")).to_be_visible()
    expect(page.get_by_role("link", name="Log out")).to_be_visible()


@pytest.mark.local_browser
@pytest.mark.parametrize(
    ("username", "password", "expected_error"),
    [
        ("incorrectUser", "Password123", "Your username is invalid!"),
        ("student", "incorrectPassword", "Your password is invalid!"),
    ],
    ids=("invalid-username", "invalid-password"),
)
def test_bundled_login_fixture_rejects_invalid_credentials(
    page, demo_login_html: str, username: str, password: str, expected_error: str
) -> None:
    from playwright.sync_api import expect

    page.set_content(demo_login_html)
    page.get_by_label("Username").fill(username)
    page.get_by_label("Password").fill(password)
    page.get_by_role("button", name="Submit").click()

    error_message = page.get_by_role("alert")
    expect(error_message).to_be_visible()
    expect(error_message).to_have_text(expected_error)
