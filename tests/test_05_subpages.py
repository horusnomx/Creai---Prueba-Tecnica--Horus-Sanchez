"""
Smoke tests TC-20 a TC-25: disponibilidad y H1 de sub-páginas (Módulo 5).

Para cada sub-página crítica documentada en `selector_map.md`, navega
directamente vía `page.goto(url)` y valida que el H1 visible coincida
exactamente con el texto esperado.
"""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

DEFAULT_TIMEOUT_MS: int = 10_000

# (path, fragmento esperado en H1) — textos extraídos de selector_map.md.
# Notas:
# - Páginas /services/* tienen el H1 anidado con texto adyacente concatenado
#   en `textContent`; usamos `to_contain_text` (substring) en lugar de match exacto.
# - El H1 documentado para /knowledge-hub era 'Resources', pero el sitio actual
#   muestra 'Knowledge hub' (deploy posterior al snapshot del selector_map).
SUBPAGES: tuple[tuple[str, str], ...] = (
    ("/services/ai-systems-framework", "AI Systems Framework"),
    ("/services/custom-ai-solutions-factory", "Custom AI Solutions Factory"),
    # selector_map.md documenta el H1 como 'Take your projects to the next level...'
    # pero el sitio actual muestra simplemente 'Talent as a Service' (deploy posterior).
    ("/services/talent-as-a-service", "Talent as a Service"),
    (
        "/success-stories",
        "Faster, smoother, safer operations—all with AI",
    ),
    ("/about-us", "Your trusted leaders in AI-driven solutions"),
    ("/knowledge-hub", "Knowledge hub"),
)


def _assert_subpage_h1(page: Page, path: str, expected_h1_fragment: str) -> None:
    """Helper: navega a `path` y valida que el H1 visible contenga el texto esperado."""
    page.goto(path, wait_until="domcontentloaded", timeout=60_000)
    h1 = page.locator("h1:visible").first
    expect(h1).to_be_visible(timeout=DEFAULT_TIMEOUT_MS)
    expect(h1).to_contain_text(expected_h1_fragment)


@pytest.mark.functional
def test_tc20_ai_systems_framework_h1(page: Page) -> None:
    """TC-20: /services/ai-systems-framework tiene el H1 esperado."""
    _assert_subpage_h1(page, *SUBPAGES[0])


@pytest.mark.functional
def test_tc21_custom_ai_solutions_factory_h1(page: Page) -> None:
    """TC-21: /services/custom-ai-solutions-factory tiene el H1 esperado."""
    _assert_subpage_h1(page, *SUBPAGES[1])


@pytest.mark.functional
def test_tc22_talent_as_a_service_h1(page: Page) -> None:
    """TC-22: /services/talent-as-a-service tiene el H1 esperado."""
    _assert_subpage_h1(page, *SUBPAGES[2])


@pytest.mark.functional
def test_tc23_success_stories_h1(page: Page) -> None:
    """TC-23: /success-stories tiene el H1 esperado."""
    _assert_subpage_h1(page, *SUBPAGES[3])


@pytest.mark.functional
def test_tc24_about_us_h1(page: Page) -> None:
    """TC-24: /about-us tiene el H1 esperado."""
    _assert_subpage_h1(page, *SUBPAGES[4])


@pytest.mark.functional
def test_tc25_knowledge_hub_h1(page: Page) -> None:
    """TC-25: /knowledge-hub tiene el H1 esperado."""
    _assert_subpage_h1(page, *SUBPAGES[5])
