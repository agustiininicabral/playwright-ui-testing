import pytest


@pytest.mark.integration
def test_valid_credentials_log_in_successfully(page, base_url: str) -> None:
    from playwright.sync_api import expect

    page.goto(f"{base_url}/practice-test-login/", wait_until="domcontentloaded")
    page.get_by_label("Username").fill("student")
    page.get_by_label("Password").fill("Password123")
    page.get_by_role("button", name="Submit").click()

    expect(page).to_have_url(f"{base_url}/logged-in-successfully/")
    expect(page.get_by_role("heading", name="Logged In Successfully")).to_be_visible()
    expect(page.get_by_role("link", name="Log out")).to_be_visible()
