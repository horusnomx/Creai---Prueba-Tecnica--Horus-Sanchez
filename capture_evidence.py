"""
Captura evidencia visual + DOM del bug de TC-34.

Genera 4 artefactos en ./evidence/:
  - 01_full_page.png      : screenshot completo de la home (lo que ve el usuario)
  - 02_dom_inspection.txt : volcado del DOM mostrando que la sección existe pero está oculta
  - 03_section_isolated.png: screenshot del DIV padre (renderizado forzando display:block)
  - 04_recording.webm     : grabación scrolleando la home para verificar visualmente
"""

from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(__file__).parent / "evidence"
OUT.mkdir(exist_ok=True)


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            record_video_dir=str(OUT),
            record_video_size={"width": 1440, "height": 900},
        )
        page = context.new_page()
        page.goto("https://www.creai.mx", wait_until="networkidle")

        # Aceptar cookies para que no obstruyan
        try:
            page.locator(
                "#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"
            ).click(timeout=5_000)
            page.locator("#CybotCookiebotDialog").wait_for(state="hidden", timeout=5_000)
        except Exception:
            pass

        # Screenshot completo: lo que el usuario realmente ve.
        page.screenshot(path=str(OUT / "01_full_page.png"), full_page=True)

        # Inspección del DOM: probar visibilidad de las cards y su sección padre.
        inspection = page.evaluate(
            """() => {
              const cards = Array.from(document.querySelectorAll('a.latest_posts-card'));
              const section = document.querySelector('.section_latest_posts');

              const desc = (el) => {
                if (!el) return null;
                const r = el.getBoundingClientRect();
                const s = window.getComputedStyle(el);
                return {
                  tag: el.tagName,
                  className: el.className,
                  display: s.display,
                  visibility: s.visibility,
                  opacity: s.opacity,
                  width_px: Math.round(r.width),
                  height_px: Math.round(r.height),
                  in_dom: true,
                };
              };

              return {
                section_latest_posts: desc(section),
                first_card: cards[0] ? desc(cards[0]) : null,
                cards_count: cards.length,
                cards_hrefs: cards.slice(0, 5).map(c => c.getAttribute('href')),
              };
            }"""
        )
        (OUT / "02_dom_inspection.txt").write_text(
            "=== TC-34 — Evidencia del bug ===\n\n"
            "Pregunta: ¿el usuario ve los blog posts de 'Latest insights'?\n\n"
            f"{json.dumps(inspection, indent=2)}\n\n"
            "Lectura:\n"
            "  - cards_count > 0  → los artículos SÍ existen en el HTML\n"
            "  - section_latest_posts.display == 'none' → el CSS oculta toda la sección\n"
            "  - first_card.width_px / height_px = 0 → ni siquiera ocupan espacio en la página\n"
            "  - Conclusión: contenido publicado en el CMS pero invisible para usuarios.\n",
            encoding="utf-8",
        )

        # Demostración: si quitamos el display:none, los cards SÍ se ven.
        page.evaluate(
            """() => {
              const section = document.querySelector('.section_latest_posts');
              if (section) {
                section.classList.remove('hide');
                section.style.display = 'block';
              }
            }"""
        )
        # Espera a que el browser repinte y screenshot del estado "arreglado".
        page.wait_for_timeout(500)
        section_box = page.locator(".section_latest_posts").bounding_box()
        if section_box:
            page.evaluate(
                f"window.scrollTo(0, {int(section_box['y'] - 100)})"
            )
            page.wait_for_timeout(300)
        page.locator(".section_latest_posts").screenshot(
            path=str(OUT / "03_section_when_fixed.png")
        )

        context.close()
        browser.close()


if __name__ == "__main__":
    main()
