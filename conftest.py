"""
Configuración global de pytest para el suite de smoke tests de creai.mx.

Define fixtures compartidas:
- page: navegador Chromium headless con base_url = https://www.creai.mx.
- console_errors: captura mensajes console.error emitidos durante el test.
- mobile_page: viewport iPhone X (375x812).
- tablet_page: viewport iPad (768x1024).
"""

from __future__ import annotations

from typing import Generator, List

import pytest
from playwright.sync_api import Browser, BrowserContext, ConsoleMessage, Page

BASE_URL = "https://www.creai.mx"
DESKTOP_VIEWPORT = {"width": 1440, "height": 900}
MOBILE_VIEWPORT = {"width": 375, "height": 812}
TABLET_VIEWPORT = {"width": 768, "height": 1024}


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    """Forzar Chromium en modo headless para toda la sesión."""
    return {**browser_type_launch_args, "headless": True}


@pytest.fixture
def browser_context_args(browser_context_args: dict) -> dict:
    """Inyectar base_url y viewport de escritorio en el contexto por defecto."""
    return {
        **browser_context_args,
        "base_url": BASE_URL,
        "viewport": DESKTOP_VIEWPORT,
    }


@pytest.fixture
def console_errors(page: Page) -> Generator[List[str], None, None]:
    """
    Captura todos los mensajes de tipo "error" emitidos por console durante el test.

    El listener se adjunta antes de cualquier navegación para no perder eventos
    tempranos. La lista resultante se expone mutable al test para inspección.
    """
    errors: List[str] = []

    def _on_console(message: ConsoleMessage) -> None:
        if message.type == "error":
            errors.append(message.text)

    page.on("console", _on_console)
    yield errors
    page.remove_listener("console", _on_console)


def _page_with_viewport(
    browser: Browser, viewport: dict
) -> Generator[Page, None, None]:
    """Helper interno: abre un contexto efímero con el viewport indicado."""
    context: BrowserContext = browser.new_context(
        base_url=BASE_URL,
        viewport=viewport,
    )
    page = context.new_page()
    try:
        yield page
    finally:
        context.close()


@pytest.fixture
def mobile_page(browser: Browser) -> Generator[Page, None, None]:
    """Página con viewport móvil (iPhone X — 375x812)."""
    yield from _page_with_viewport(browser, MOBILE_VIEWPORT)


@pytest.fixture
def tablet_page(browser: Browser) -> Generator[Page, None, None]:
    """Página con viewport de tablet (768x1024)."""
    yield from _page_with_viewport(browser, TABLET_VIEWPORT)
