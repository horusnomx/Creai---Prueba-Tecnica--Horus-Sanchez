"""
Smoke tests TC-01 a TC-04: carga inicial de la homepage de creai.mx.

Cubre:
- TC-01: status 200 vía APIRequestContext.
- TC-02: ausencia de errores en `console.error` durante el primer load.
- TC-03: redirección de http://creai.mx → https://www.creai.mx.
- TC-04: tiempo total del `goto` por debajo de 5 segundos.
"""

from __future__ import annotations

import time
from typing import List

import pytest
from playwright.sync_api import Page, Playwright, expect

from pages.home_page import HomePage

BASE_URL = "https://www.creai.mx"
LOAD_TIME_LIMIT_SECONDS = 5.0


@pytest.mark.smoke
def test_tc01_homepage_returns_status_200(playwright: Playwright) -> None:
    """TC-01: un GET a la homepage devuelve HTTP 200 vía APIRequestContext."""
    api_context = playwright.request.new_context()
    try:
        response = api_context.get(BASE_URL)
        assert response.status == 200, (
            f"Se esperaba status 200, obtenido: {response.status} "
            f"({response.status_text})"
        )
    finally:
        api_context.dispose()


@pytest.mark.smoke
def test_tc02_no_console_errors_on_initial_load(
    page: Page, console_errors: List[str]
) -> None:
    """TC-02: la carga inicial no produce mensajes de tipo `console.error`."""
    home = HomePage(page)
    home.goto()
    # Asegura que el DOM clave terminó de pintar antes de evaluar consola.
    expect(page.locator("h1")).to_be_visible(timeout=10_000)
    assert console_errors == [], (
        f"Se detectaron errores en consola durante la carga inicial: "
        f"{console_errors}"
    )


@pytest.mark.smoke
def test_tc03_http_redirects_to_https(page: Page) -> None:
    """TC-03: http://creai.mx redirige a https://www.creai.mx."""
    page.goto("http://creai.mx")
    assert page.url.startswith("https://www.creai.mx"), (
        f"URL final inesperada tras la redirección: {page.url}"
    )


@pytest.mark.smoke
def test_tc04_homepage_loads_under_5_seconds(page: Page) -> None:
    """TC-04: el `goto` a la homepage completa en menos de 5 segundos."""
    start = time.time()
    page.goto(BASE_URL)
    elapsed = time.time() - start
    assert elapsed < LOAD_TIME_LIMIT_SECONDS, (
        f"La homepage tardó {elapsed:.2f}s en cargar "
        f"(límite: {LOAD_TIME_LIMIT_SECONDS}s)"
    )
