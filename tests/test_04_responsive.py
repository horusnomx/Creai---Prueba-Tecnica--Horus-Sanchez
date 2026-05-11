"""
Smoke tests TC-17 a TC-19: comportamiento responsive en móvil (Módulo 4).

Verifica los cambios del navbar al redimensionar a 375x812 (móvil):
- Nav links y CTA 'Get started' se ocultan vía media queries CSS.
- Logo se mantiene visible.
- Botón hamburger es visible y, al clickearlo, expone los nav links.
"""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.home_page import HomePage

DEFAULT_TIMEOUT_MS: int = 10_000
NAV_LINK_HREFS: tuple[str, ...] = (
    "/success-stories",
    "/about-us",
    "/knowledge-hub",
)


@pytest.fixture
def home_mobile(mobile_page: Page) -> HomePage:
    """`HomePage` cargado en viewport móvil (375x812), con cookies aceptadas."""
    home = HomePage(mobile_page)
    home.goto()
    home.dismiss_cookie_banner()
    return home


@pytest.mark.smoke
@pytest.mark.mobile
def test_tc17_nav_links_and_cta_hidden_in_mobile(home_mobile: HomePage) -> None:
    """
    TC-17: en viewport móvil, el nav y el CTA 'Get started' del header
    están ocultos via media queries (el header los reemplaza por hamburger + contact icon).
    """
    expect(home_mobile.get_cta_button()).to_be_hidden(timeout=DEFAULT_TIMEOUT_MS)
    for href in NAV_LINK_HREFS:
        link = home_mobile.page.locator(f"a[href='{href}']").first
        expect(link).to_be_hidden(timeout=DEFAULT_TIMEOUT_MS)


@pytest.mark.smoke
@pytest.mark.mobile
def test_tc18_logo_visible_in_mobile(home_mobile: HomePage) -> None:
    """TC-18: en viewport móvil el logo del navbar sigue visible."""
    expect(home_mobile.get_logo()).to_be_visible(timeout=DEFAULT_TIMEOUT_MS)


@pytest.mark.smoke
@pytest.mark.mobile
def test_tc19_hamburger_opens_mobile_menu(home_mobile: HomePage) -> None:
    """
    TC-19: clickear el botón hamburger expone los links del nav que estaban ocultos.

    Valida la transición de cerrado → abierto: antes del click los nav links
    están oculta; tras click + animación, al menos uno se vuelve visible.
    """
    # `.last` para targetear el clon de Finsweet Smart Nav (el original queda
    # detrás y sus pointer events son interceptados).
    hamburger = home_mobile.get_hamburger_menu().last
    expect(hamburger).to_be_visible(timeout=DEFAULT_TIMEOUT_MS)
    # Estado cerrado: nav links ocultos (verificado también en TC-17)
    first_link = home_mobile.page.locator(
        f"a[href='{NAV_LINK_HREFS[0]}']"
    ).first
    expect(first_link).to_be_hidden(timeout=DEFAULT_TIMEOUT_MS)
    # Abrir el menú
    hamburger.click()
    # Tras click, los nav links deben volverse visibles en al menos una instancia
    visible_link = home_mobile.page.locator(
        f"a[href='{NAV_LINK_HREFS[0]}']:visible"
    ).first
    expect(visible_link).to_be_visible(timeout=DEFAULT_TIMEOUT_MS)
