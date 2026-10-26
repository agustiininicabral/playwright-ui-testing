import pytest


@pytest.mark.integration
def test_login_page_loads_with_expected_form(page, base_url: str) -> None:
    from playwright.sync_api import expect

    response = page.goto(f"{base_url}/practice-test-login/", wait_until="domcontentloaded")

    assert response is not None
    assert response.status == 200
    expect(page).to_have_title("Test Login | Practice Test Automation")
    expect(page.get_by_role("heading", name="Test Login")).to_be_visible()
    expect(page.get_by_label("Username")).to_be_visible()
    expect(page.get_by_label("Password")).to_be_visible()
    expect(page.get_by_role("button", name="Submit")).to_be_visible()
