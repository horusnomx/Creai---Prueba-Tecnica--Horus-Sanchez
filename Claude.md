# creai-smoke-tests — CLAUDE.md

## Contexto
Smoke test suite para la homepage de https://www.creai.mx
Prueba técnica de QA Automation Engineer para Creai.

## Stack
- Python 3.11+
- pytest + pytest-playwright
- Playwright Chromium (headless por defecto)
- pytest-html para reporte

## Estructura
creai-smoke-tests/
├── CLAUDE.md
├── README.md
├── requirements.txt
├── pytest.ini
├── conftest.py
├── pages/home_page.py     ← todos los locators aquí (POM)
├── selector_map.md        ← generado por Antigravity, NO editar a mano
└── tests/
    ├── test_01_page_load.py
    ├── test_02_key_elements.py
    ├── test_03_navigation.py
    ├── test_04_content_sections.py
    ├── test_05_mobile_viewport.py
    └── test_06_meta_seo.py

## Convenciones de código
- Nombres de test y código: inglés
- Docstrings: español
- Locators: siempre desde pages/home_page.py, nunca inline en los tests
- Prioridad de locators: get_by_role > get_by_text > css > xpath
- Nunca usar time.sleep() — usar expect() con timeout explícito
- Cada test es independiente, sin estado compartido entre ellos
- Marks: @pytest.mark.smoke (todos), @pytest.mark.mobile (TC-23 a TC-26)

## BASE_URL
https://www.creai.mx

## Comandos clave
pytest -v                                  # todos
pytest -v -m smoke                         # solo smoke
pytest -v -m mobile                        # solo mobile
pytest -v --html=report.html               # con reporte
pytest tests/test_01_page_load.py -v       # un módulo

## Criterios de evaluación (no perder de vista)
- Correcta implementación técnica: 30%
- Cobertura de requisitos: 25%
- Buenas prácticas y legibilidad: 20%
- Uso adecuado de la herramienta: 15%
- Entregables claros y ejecutables: 10%

# Testing Journal — Creai.mx Smoke Test Suite

## 1. Análisis del challenge
- Fecha de recepción, fecha límite
- Herramienta elegida: Playwright + Python (razón: familiaridad, 
  soporte nativo async, fixtures de pytest)
- Decisión de arquitectura: Page Object Model ligero

## 2. Reconocimiento del sitio
- URL analizada: https://www.creai.mx
- Secciones identificadas: [lista]
- Elementos clave encontrados: logo, nav, CTAs, FAQ, success stories, blog
- Hallazgos relevantes: (ej. el FAQ usa accordion JS, no <details> nativo)

## 3. Casos de prueba definidos
- Mínimo requerido por el challenge: 6 casos
- Total implementado: 29 casos
- Criterio de expansión: cobertura real de UX crítico

## 4. Implementación
- [Fecha] Scaffolding y conftest.py
- [Fecha] Page Object (home_page.py)
- [Fecha] test_01 — Page load: X/4 pasaron
- [Fecha] test_02 — Key elements: X/5 pasaron
- ... etc.

## 5. Resultados de ejecución final
| Suite | Tests | Passed | Failed | Skipped |
|-------|-------|--------|--------|---------|
| Page load | 4 | 4 | 0 | 0 |
| ... | | | | |
| **Total** | **29** | **X** | **X** | **0** |

## 6. Issues encontrados / decisiones tomadas
- (ej. TC-03 redirect: el sitio ya redirige con www, se ajustó la aserción)
- (ej. TC-20 FAQ accordion: requirió wait_for_selector por animación CSS)

## 7. Instrucciones de entrega
- Repo público: https://github.com/[tu-usuario]/creai-smoke-tests
- Reporte HTML: abrir report.html en browser tras correr pytest