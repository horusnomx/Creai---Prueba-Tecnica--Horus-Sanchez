"""
Smoke tests TC-30 a TC-42: cobertura adicional (Módulo 7 — extras).

Extiende la batería del `test_cases_steps.md` (TC-01..29) con casos
complementarios:
- TC-30..33: clicks individuales en cada nav link + retorno por logo.
- TC-34: blog posts en sección 'Latest insights' (DOM, sección oculta por CMS).
- TC-35: layout tablet sin overflow horizontal.
- TC-36..41: metadata y SEO (title, description, og:image, twitter:image,
  html lang, canonical).
- TC-42: contrato HTTP del botón 'Get started' — actualmente responde 204
  pero se espera 200; este test está diseñado para fallar hasta que el
  backend devuelva 200.
"""

from __future__ import annotations

import re

import pytest
from playwright.sync_api import Page, expect

from pages.home_page import HomePage

DEFAULT_TIMEOUT_MS: int = 10_000
HOME_URL_PATTERN = re.compile(r"^https://www\.creai\.mx/?$")
MIN_TITLE_LENGTH: int = 10
MIN_DESCRIPTION_LENGTH: int = 30


@pytest.fixture
def home(page: Page) -> HomePage:
    """`HomePage` cargada con cookies aceptadas — necesario para clicks."""
    home_page = HomePage(page)
    home_page.goto()
    home_page.dismiss_cookie_banner()
    return home_page


# ---------- Nav clicks individuales (TC-30..33) ----------


@pytest.mark.functional
def test_tc30_success_stories_link_navigates(home: HomePage) -> None:
    """TC-30: click en 'Success stories' del nav navega a /success-stories."""
    home.click_nav_link("/success-stories")
    expect(home.page).to_have_url(
        re.compile(r"/success-stories/?$"), timeout=DEFAULT_TIMEOUT_MS
    )


@pytest.mark.functional
def test_tc31_about_us_link_navigates(home: HomePage) -> None:
    """TC-31: click en 'About us' del nav navega a /about-us."""
    home.click_nav_link("/about-us")
    expect(home.page).to_have_url(
        re.compile(r"/about-us/?$"), timeout=DEFAULT_TIMEOUT_MS
    )


@pytest.mark.functional
def test_tc32_knowledge_hub_link_navigates(home: HomePage) -> None:
    """TC-32: click en 'Knowledge hub' del nav navega a /knowledge-hub."""
    home.click_nav_link("/knowledge-hub")
    expect(home.page).to_have_url(
        re.compile(r"/knowledge-hub/?$"), timeout=DEFAULT_TIMEOUT_MS
    )


@pytest.mark.regression
def test_tc33_logo_click_returns_to_home(home: HomePage) -> None:
    """TC-33: desde una sub-página, click en el logo regresa a la homepage."""
    home.click_nav_link("/about-us")
    expect(home.page).to_have_url(
        re.compile(r"/about-us/?$"), timeout=DEFAULT_TIMEOUT_MS
    )
    home.click_logo()
    expect(home.page).to_have_url(HOME_URL_PATTERN, timeout=DEFAULT_TIMEOUT_MS)


# ---------- Sección 'Latest insights' (TC-34) ----------


@pytest.mark.regression
def test_tc34_latest_insights_has_blog_posts_in_dom(home: HomePage) -> None:
    """
    TC-34: la sección 'Latest insights' muestra al menos un blog post visible.

    FALLO ESPERADO (bug conocido): los cards `a.latest_posts-card` existen
    en el DOM, pero la sección padre `section_latest_posts` tiene
    `display:none` (clase `hide`) en el deploy actual — el contenido es
    invisible para usuarios. La aserción usa `to_be_visible()` (no
    `to_be_attached()`) para exponer activamente este defecto. Permanece
    en rojo hasta que la sección se vuelva visible en producción.
    """
    posts = home.get_blog_posts()
    expect(posts.first).to_be_visible(timeout=DEFAULT_TIMEOUT_MS)
    assert posts.count() >= 1, "Se esperaba al menos 1 blog post en 'Latest insights'"


# ---------- Responsive tablet (TC-35) ----------


@pytest.mark.regression
@pytest.mark.mobile
def test_tc35_no_horizontal_overflow_at_tablet(tablet_page: Page) -> None:
    """TC-35: en viewport tablet (768x1024) la home no introduce overflow horizontal."""
    home = HomePage(tablet_page)
    home.goto()
    home.dismiss_cookie_banner()
    metrics = tablet_page.evaluate(
        """() => ({
            scrollWidth: document.documentElement.scrollWidth,
            clientWidth: document.documentElement.clientWidth
        })"""
    )
    assert metrics["scrollWidth"] <= metrics["clientWidth"], (
        f"Overflow horizontal detectado en tablet: "
        f"scrollWidth={metrics['scrollWidth']}px > "
        f"clientWidth={metrics['clientWidth']}px"
    )


# ---------- Metadata / SEO (TC-36..41) ----------


@pytest.mark.regression
def test_tc36_title_tag_is_present_and_meaningful(home: HomePage) -> None:
    """TC-36: la home tiene <title> con contenido razonable (>=10 chars)."""
    title = home.page.title().strip()
    assert title, "El <title> está vacío"
    assert len(title) >= MIN_TITLE_LENGTH, (
        f"Title sospechosamente corto ({len(title)} chars): {title!r}"
    )


@pytest.mark.regression
def test_tc37_meta_description_is_present(home: HomePage) -> None:
    """TC-37: existe meta description con contenido (>=30 chars)."""
    description = home.page.locator("meta[name='description']").first
    expect(description).to_be_attached(timeout=DEFAULT_TIMEOUT_MS)
    content = (description.get_attribute("content") or "").strip()
    assert len(content) >= MIN_DESCRIPTION_LENGTH, (
        f"Meta description vacía o muy corta ({len(content)} chars): {content!r}"
    )


@pytest.mark.regression
def test_tc38_twitter_image_is_absolute_url(home: HomePage) -> None:
    """
    TC-38: existe meta property='twitter:image' con URL absoluta.

    Nota: la home actualmente no expone og:title ni og:description — solo
    og:image y twitter:image. Este TC valida la card de Twitter.
    """
    twitter_image = home.page.locator("meta[property='twitter:image']").first
    expect(twitter_image).to_be_attached(timeout=DEFAULT_TIMEOUT_MS)
    content = (twitter_image.get_attribute("content") or "").strip()
    assert content.startswith(("http://", "https://")), (
        f"twitter:image debe ser URL absoluta: {content!r}"
    )


@pytest.mark.regression
def test_tc39_open_graph_image_is_absolute_url(home: HomePage) -> None:
    """TC-39: existe meta property='og:image' con URL absoluta."""
    og_image = home.page.locator("meta[property='og:image']").first
    expect(og_image).to_be_attached(timeout=DEFAULT_TIMEOUT_MS)
    content = (og_image.get_attribute("content") or "").strip()
    assert content.startswith(("http://", "https://")), (
        f"og:image debe ser URL absoluta: {content!r}"
    )


@pytest.mark.regression
def test_tc40_html_lang_attribute_is_set(home: HomePage) -> None:
    """TC-40: el <html> declara atributo `lang` (accesibilidad + SEO)."""
    lang = home.page.evaluate("() => document.documentElement.lang") or ""
    assert lang.strip(), "<html> sin atributo lang declarado"
    assert lang.lower().startswith("en"), (
        f"Lang esperado 'en*' en la home en inglés; obtenido: {lang!r}"
    )


@pytest.mark.regression
def test_tc41_canonical_link_points_to_creai_domain(home: HomePage) -> None:
    """TC-41: existe <link rel='canonical'> apuntando al dominio canónico."""
    canonical = home.page.locator("link[rel='canonical']").first
    expect(canonical).to_be_attached(timeout=DEFAULT_TIMEOUT_MS)
    href = (canonical.get_attribute("href") or "").strip()
    assert href.startswith("https://www.creai.mx"), (
        f"Canonical debe apuntar a https://www.creai.mx; obtenido: {href!r}"
    )


# ---------- Contrato HTTP del CTA (TC-42) ----------


@pytest.mark.regression
def test_tc42_get_started_button_returns_200_ok(home: HomePage) -> None:
    """
    TC-42: el click en 'Get started' del header debe responder HTTP 200 en
    todas las responses dinámicas que dispara.

    FALLO CONOCIDO (verificado manualmente): al menos un endpoint asociado
    al click responde HTTP 204 No Content. Este test queda intencionalmente
    en rojo como red flag de tracking hasta que el backend devuelva 200.

    Estrategia:
      1. Suscribir un listener al evento `response` del browser context.
      2. Capturar todas las responses (incluyendo third-party tracking).
      3. Disparar el click en el CTA (navbar clonado, `.last`).
      4. Esperar a que la red entre en idle.
      5. Filtrar a responses dinámicas (excluyendo assets estáticos y
         preflights OPTIONS).
      6. Asegurar que TODAS tienen status 200. Cualquier 204 hace fallar
         el test con un mensaje diagnóstico que incluye la URL infractora.
    """
    captured: list = []
    home.page.on("response", lambda r: captured.append(r))

    home.page.locator("a.button_link").last.click()
    home.page.wait_for_load_state("networkidle", timeout=15_000)

    static_exts = (
        ".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".svg",
        ".ico", ".woff", ".woff2", ".ttf", ".mp4", ".webp", ".m4v",
    )
    dynamic_responses = [
        r for r in captured
        if not r.url.lower().split("?")[0].endswith(static_exts)
        and r.request.method != "OPTIONS"
    ]
    assert dynamic_responses, (
        "No se capturó ninguna response dinámica tras el click en 'Get started'"
    )

    # El user reportó manualmente status 204. Filtramos específicamente para
    # ese caso (excluimos 3xx redirects que son normales en pipelines de
    # tracking — el problema reportado es la respuesta final sin contenido).
    no_content = [r for r in dynamic_responses if r.status == 204]
    assert not no_content, (
        f"'Get started' generó {len(no_content)} response(s) con status 204 "
        f"No Content; se esperaba 200 OK. URL(s) afectada(s): "
        f"{[r.url[:100] for r in no_content][:3]}"
    )
