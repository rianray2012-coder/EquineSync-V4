from mailer import render


def test_verify_email_renders_live_cta_fallback_and_linked_logo(monkeypatch):
    monkeypatch.setenv("WEBSITE_URL", "https://equine-sync.com")
    monkeypatch.setenv("EMAIL_LOGO_URL", "https://app.equine-sync.com/icon-192.png")
    verify_url = "https://app.equine-sync.com/verify-email?token=test-token"

    html = render(
        "verify_email",
        {
            "full_name": "Test User",
            "verify_url": verify_url,
            "verify_url_html": verify_url,
            "ttl_label": "48 hours",
        },
        base="_base_auth",
    )

    assert 'href="https://app.equine-sync.com/verify-email?token=test-token"' in html
    assert html.count('href="https://app.equine-sync.com/verify-email?token=test-token"') == 2
    assert 'href="https://equine-sync.com"' in html
    assert 'src="https://app.equine-sync.com/icon-192.png"' in html
    assert 'alt="EquineSync"' in html


def test_email_verified_followup_renders_app_download_cta(monkeypatch):
    monkeypatch.setenv("WEBSITE_URL", "https://equine-sync.com")
    monkeypatch.setenv("EMAIL_LOGO_URL", "https://app.equine-sync.com/icon-192.png")
    monkeypatch.setenv("MOBILE_APP_DOWNLOAD_URL", "https://app.equine-sync.com/download")

    html = render(
        "email_verified_app_download",
        {
            "full_name": "Test User",
            "download_url": "https://app.equine-sync.com/download",
        },
        base="_base_auth",
    )

    assert "Your EquineSync account is ready" in html
    assert "Download the EquineSync app" in html
    assert html.count('href="https://app.equine-sync.com/download"') == 2
    assert 'href="https://equine-sync.com"' in html
    assert 'src="https://app.equine-sync.com/icon-192.png"' in html
