import pytest


@pytest.mark.integration
@pytest.mark.parametrize(
    ("username", "password", "expected_error"),
    [
        ("incorrectUser", "Password123", "Your username is invalid!"),
        ("student", "incorrectPassword", "Your password is invalid!"),
    ],
    ids=("invalid-username", "invalid-password"),
)
def test_invalid_credentials_show_specific_error(
    page, base_url: str, username: str, password: str, expected_error: str
) -> None:
    from playwright.sync_api import expect

    page.goto(f"{base_url}/practice-test-login/", wait_until="domcontentloaded")
    page.get_by_label("Username").fill(username)
    page.get_by_label("Password").fill(password)
    page.get_by_role("button", name="Submit").click()

    error_message = page.locator("#error")
    expect(error_message).to_be_visible()
    expect(error_message).to_have_text(expected_error)
