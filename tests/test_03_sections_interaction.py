"""
Smoke tests TC-11 a TC-16: secciones de la homepage e interacción (Módulo 3).

Cubre los bloques principales documentados en `test_cases_steps.md`:
dropdown 'Services', H2 de cada sección, strip de clientes, cards de
success stories, acordeón del FAQ y CTA del footer.
"""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

from pages.home_page import HomePage

DEFAULT_TIMEOUT_MS: int = 10_000

SERVICES_DROPDOWN_HREFS: tuple[str, ...] = (
    "/services/ai-systems-framework",
    "/services/custom-ai-solutions-factory",
    "/services/talent-as-a-service",
)
EXPECTED_H2_FRAGMENTS: tuple[str, ...] = (
    "The future waits for no one",
    "Evolve and optimize your operations",
    "Success stories",
    "FAQs",
)


@pytest.fixture
def home(page: Page) -> HomePage:
    """`HomePage` cargada con cookies aceptadas — necesario para clicks."""
    home_page = HomePage(page)
    home_page.goto()
    home_page.dismiss_cookie_banner()
    return home_page


@pytest.mark.smoke
def test_tc11_services_dropdown_exposes_three_items(home: HomePage) -> None:
    """
    TC-11: abrir el dropdown 'Services' expone los 3 sub-items esperados y son
    visibles para el usuario.

    `to_have_count` solo valida presencia en DOM; añadimos `to_be_visible` sobre
    el primer item para detectar regresiones donde el panel se marca `.w--open`
    pero el CSS deja los items con `opacity:0` / `display:none` (mismo patrón de
    bug que TC-34 sobre 'Latest insights').
    """
    items = home.open_services_dropdown()
    expect(items).to_have_count(3, timeout=DEFAULT_TIMEOUT_MS)
    expect(items.first).to_be_visible(timeout=DEFAULT_TIMEOUT_MS)
    open_panel = home.page.locator(".w-dropdown-list.w--open")
    for href in SERVICES_DROPDOWN_HREFS:
        expect(open_panel.locator(f"a[href='{href}']")).to_have_count(
            1, timeout=DEFAULT_TIMEOUT_MS
        )


@pytest.mark.smoke
def test_tc12_homepage_h2_sections_are_visible(home: HomePage) -> None:
    """
    TC-12: la home muestra los H2 de las secciones documentadas.

    Filtra a `h2:visible` porque algunos H2 tienen una variante duplicada en
    DOM para responsive — `.first` sobre todos los H2 podría caer en la oculta.
    `selector_map.md` también lista 'Latest insights', pero el deploy actual
    aplica `display:none` a esa sección (ver TC-34 en extras).
    """
    for fragment in EXPECTED_H2_FRAGMENTS:
        h2 = home.page.locator("h2:visible").filter(has_text=fragment).first
        expect(h2).to_be_visible(timeout=DEFAULT_TIMEOUT_MS)


@pytest.mark.smoke
def test_tc13_client_logos_strip_is_visible(home: HomePage) -> None:
    """
    TC-13: el strip/carousel de logos de clientes está visible y al menos un
    logo se renderiza correctamente (imagen cargada, no broken src).

    `selector_map.md` describe `div.clients_component`. El DOM real tiene dos
    zonas: `div.clients-wrapper` (height:0, vacía en este deploy) y
    `div.logo3_component` cerca del hero (visible). Usamos esta última.

    Adicional al conteo, validamos `to_be_visible` sobre el primer `<img>` y
    su `naturalWidth > 0` para detectar imágenes con `src` roto o ocultas por
    CSS (mismo patrón de bug que TC-34).
    """
    strip = home.get_client_logos().first
    expect(strip).to_be_visible(timeout=DEFAULT_TIMEOUT_MS)
    logos = strip.locator("img")
    assert logos.count() >= 1, "El strip de clientes debe tener al menos 1 logo"
    expect(logos.first).to_be_visible(timeout=DEFAULT_TIMEOUT_MS)
    first_logo_loaded = logos.first.evaluate("img => img.naturalWidth > 0")
    assert first_logo_loaded, "El primer logo del strip tiene src roto (naturalWidth == 0)"


@pytest.mark.smoke
def test_tc14_success_story_cards_are_rendered(home: HomePage) -> None:
    """
    TC-14: la sección 'Success stories' renderiza cards con CTA 'Read more'.

    `selector_map.md` describe `div.success-stories_card`, pero el sitio fue
    rediseñado: los cards ahora son enlaces 'Read more' dentro de un Swiper
    apuntando a `/success-stories/<slug>`.
    """
    cards = home.get_success_story_cards()
    expect(cards.first).to_be_visible(timeout=DEFAULT_TIMEOUT_MS)
    assert cards.count() >= 1, "Se esperaba al menos 1 success story card"


@pytest.mark.smoke
def test_tc15_clicking_faq_item_expands_it(home: HomePage) -> None:
    """
    TC-15: hacer click en la primera pregunta del FAQ expande su respuesta.

    El componente `faq6_*` de Webflow no usa `aria-expanded` y el
    `div.faq6_answer` queda en DOM con height ~8px (colapsado). Comparamos
    la altura antes/después del click.
    """
    home.page.locator(HomePage.FAQ_CONTAINER).first.scroll_into_view_if_needed()
    height_before = home.page.evaluate(
        "() => document.querySelector('.faq6_answer').getBoundingClientRect().height"
    )
    home.click_faq_item(0)
    home.page.wait_for_function(
        f"() => document.querySelector('.faq6_answer').getBoundingClientRect().height > {height_before + 30}",
        timeout=DEFAULT_TIMEOUT_MS,
    )


@pytest.mark.smoke
def test_tc16_footer_cta_points_to_contact(home: HomePage) -> None:
    """TC-16: el CTA 'Contact us' del banner inferior apunta a /contact."""
    cta = home.get_footer_cta().first
    expect(cta).to_be_visible(timeout=DEFAULT_TIMEOUT_MS)
    expect(cta).to_have_attribute("href", "/contact")
