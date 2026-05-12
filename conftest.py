"""
Configuración global de pytest para el suite de smoke tests de creai.mx.

Define fixtures compartidas:
- page: navegador Chromium headless con base_url = https://www.creai.mx.
- console_errors: captura mensajes console.error emitidos durante el test.
- mobile_page: viewport iPhone X (375x812).
- tablet_page: viewport iPad (768x1024).
"""

from __future__ import annotations

import base64
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


# --- Evidence capture on failure ------------------------------------------
#
# Hook que adjunta evidencia al reporte HTML cuando un test falla:
#   - Screenshot full-page embebido en base64 (capa A — sigue siendo un único
#     archivo HTML portátil con `--self-contained-html`).
#   - URL final de la página al momento del fallo (capa C).
#   - Mensajes `console.error` capturados durante el test, si la fixture
#     `console_errors` estaba activa.
#
# Si el test no usó ningún fixture de página (p. ej. TC-01 que solo usa
# `APIRequestContext`), no hay nada que capturar y el hook salta sin error.


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Adjuntar screenshot + URL + console errors al reporte HTML en fallos."""
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    extras_list = getattr(report, "extras", [])

    page = (
        item.funcargs.get("page")
        or item.funcargs.get("mobile_page")
        or item.funcargs.get("tablet_page")
    )

    try:
        from pytest_html import extras as html_extras
    except ImportError:
        return

    if page is not None:
        # Capa A — screenshot embebido en base64 (full page).
        # pytest-html 4.x requiere que el contenido sea un *string* ya
        # codificado en base64 (no bytes crudos); de lo contrario falla
        # internamente con `'bytes' object has no attribute 'encode'`.
        try:
            screenshot_bytes = page.screenshot(full_page=True)
            screenshot_b64 = base64.b64encode(screenshot_bytes).decode("ascii")
            extras_list.append(
                html_extras.png(screenshot_b64, name="screenshot at failure")
            )
        except Exception as exc:
            extras_list.append(
                html_extras.text(
                    f"Screenshot capture failed: {exc}",
                    name="screenshot error",
                )
            )

        # Capa C — URL final + tamaño del viewport al momento del fallo.
        try:
            viewport = page.viewport_size or {}
            context_line = (
                f"URL: {page.url}\n"
                f"Viewport: {viewport.get('width', '?')}x{viewport.get('height', '?')}"
            )
            extras_list.append(
                html_extras.text(context_line, name="page context")
            )
        except Exception:
            pass

    # Capa C — console errors capturados por la fixture, si estaba en uso.
    console_errors = item.funcargs.get("console_errors")
    if console_errors:
        extras_list.append(
            html_extras.text(
                "\n".join(console_errors),
                name=f"console.error log ({len(console_errors)} entries)",
            )
        )

    report.extras = extras_list
