"""
Smoke tests TC-05 a TC-10: elementos clave del header y hero (Módulo 2).

Verifica que los locators críticos del navbar y hero documentados en
`selector_map.md` y `test_cases_steps.md` estén presentes y con el
contenido esperado al cargar la homepage.
"""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.home_page import HomePage

EXPECTED_H1: str = "AI-powered solutions for human-centered operations"
EXPECTED_NAV_HREFS: tuple[str, ...] = (
    "/success-stories",
    "/about-us",
    "/knowledge-hub",
)
DEFAULT_TIMEOUT_MS: int = 10_000


@pytest.fixture
def home(page: Page) -> HomePage:
    """`HomePage` ya navegado a la home con base_url del context."""
    home_page = HomePage(page)
    home_page.goto()
    return home_page


@pytest.mark.smoke
def test_tc05_logo_is_visible(home: HomePage) -> None:
    """TC-05: el logo del navbar es visible al cargar la home."""
    expect(home.get_logo()).to_be_visible(timeout=DEFAULT_TIMEOUT_MS)


@pytest.mark.regression
def test_tc06_nav_contains_four_main_entries(home: HomePage) -> None:
    """TC-06: el nav muestra el dropdown 'Services' y los 3 links principales."""
    expect(home.get_services_dropdown()).to_be_visible(timeout=DEFAULT_TIMEOUT_MS)
    for href in EXPECTED_NAV_HREFS:
        link = home.page.locator(f"a[href='{href}']").first
        expect(link).to_be_visible(timeout=DEFAULT_TIMEOUT_MS)


@pytest.mark.smoke
def test_tc07_get_started_cta_is_visible(home: HomePage) -> None:
    """TC-07: el CTA 'Get started' del header está visible."""
    expect(home.get_cta_button()).to_be_visible(timeout=DEFAULT_TIMEOUT_MS)


@pytest.mark.smoke
def test_tc08_contact_link_points_to_contact_page(home: HomePage) -> None:
    """TC-08: el botón 'Contact' del header es visible y apunta a /contact."""
    contact = home.get_contact_link()
    expect(contact).to_be_visible(timeout=DEFAULT_TIMEOUT_MS)
    expect(contact).to_have_attribute("href", "/contact")


@pytest.mark.smoke
def test_tc09_hero_h1_has_expected_text(home: HomePage) -> None:
    """TC-09: el H1 del hero tiene el texto exacto definido en selector_map."""
    h1 = home.page.locator("h1").first
    expect(h1).to_be_visible(timeout=DEFAULT_TIMEOUT_MS)
    expect(h1).to_have_text(EXPECTED_H1)


@pytest.mark.regression
def test_tc10_language_switcher_is_visible(home: HomePage) -> None:
    """TC-10: el language switcher (en / es-MX) está visible."""
    expect(home.get_language_switcher().first).to_be_visible(
        timeout=DEFAULT_TIMEOUT_MS
    )
