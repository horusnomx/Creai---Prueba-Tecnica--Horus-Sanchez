"""
Smoke tests TC-26 a TC-29: internacionalización ES-MX (Módulo 6).

Valida la versión en español de la home y de una sub-página:
- Switcher de idioma redirige a /es-mx.
- Nav traducido a español.
- H1 de la home en español.
- H1 de una sub-página crítica en español.
"""

from __future__ import annotations

import re

import pytest
from playwright.sync_api import Page, expect

from pages.home_page import HomePage

DEFAULT_TIMEOUT_MS: int = 10_000

# Textos del nav traducido (selector_map.md → sección Español).
ES_NAV_TEXTS: tuple[str, ...] = (
    "Servicios",
    "Casos de éxito",
    "Sobre nosotros",
    "Recursos",
)
ES_HOME_H1: str = "Soluciones de IA centradas en las personas"
ES_ABOUT_PATH: str = "/es-mx/about-us"
ES_ABOUT_H1: str = "Tus líderes de confianza en soluciones impulsadas por IA"


@pytest.mark.functional
def test_tc26_language_switcher_redirects_to_spanish(page: Page) -> None:
    """TC-26: el switcher de idioma redirige de la versión EN a /es-mx."""
    home = HomePage(page)
    home.goto()
    home.dismiss_cookie_banner()
    es_link = home.page.locator("a.locale_link[href*='/es-mx']").last
    es_link.click()
    expect(home.page).to_have_url(
        re.compile(r"/es-mx/?"), timeout=DEFAULT_TIMEOUT_MS
    )


@pytest.mark.functional
def test_tc27_spanish_nav_menu_is_translated(page: Page) -> None:
    """TC-27: en /es-mx, los links del nav muestran las etiquetas en español."""
    page.goto("/es-mx")
    for label in ES_NAV_TEXTS:
        # Buscamos un link visible cuyo texto contenga la etiqueta esperada.
        link = page.locator("a:visible, div:visible").filter(has_text=label).first
        expect(link).to_be_visible(timeout=DEFAULT_TIMEOUT_MS)


@pytest.mark.functional
def test_tc28_spanish_homepage_h1(page: Page) -> None:
    """TC-28: la home en español tiene el H1 traducido esperado."""
    page.goto("/es-mx")
    h1 = page.locator("h1:visible").first
    expect(h1).to_be_visible(timeout=DEFAULT_TIMEOUT_MS)
    expect(h1).to_have_text(ES_HOME_H1)


@pytest.mark.functional
def test_tc29_spanish_subpage_about_us_h1(page: Page) -> None:
    """TC-29: la sub-página /es-mx/about-us tiene el H1 traducido."""
    page.goto(ES_ABOUT_PATH)
    h1 = page.locator("h1:visible").first
    expect(h1).to_be_visible(timeout=DEFAULT_TIMEOUT_MS)
    expect(h1).to_have_text(ES_ABOUT_H1)
