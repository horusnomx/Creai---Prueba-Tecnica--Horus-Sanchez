# Creai.mx — Homepage Automated Test Suite

End-to-end automated test suite for the **creai.mx** homepage, built as a QA Automation Engineer technical assessment. The suite is organised into three categories — **Smoke**, **Functional** and **Regression / Technical** — and verifies that the production website remains operational across page load, key UI elements, navigation, content sections, responsive behavior, sub-pages, internationalization (ES-MX) and SEO metadata.

## Stack

| Layer | Tooling |
| --- | --- |
| Language | Python 3.11+ |
| Test runner | pytest |
| Browser automation | Playwright (Chromium, headless) |
| Pytest plugin | pytest-playwright |
| HTML reporting | pytest-html |
| Pattern | Page Object Model — single `HomePage` class in `pages/home_page.py` |

## Prerequisites

- **Python 3.11+** (developed and validated on Python 3.14)
- **pip** (bundled with modern Python distributions)
- Internet access — tests run against the live production site `https://www.creai.mx`

## Installation

```bash
# 1. Clone the repository
git clone <repo-url> creai-smoke-tests
cd creai-smoke-tests

# 2. (Recommended) create and activate a virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Download the Chromium browser binary that Playwright drives
python -m playwright install chromium
```

## How to run

```bash
# Solo smoke (go/no-go del build) — 9 tests
pytest -v -m smoke

# Solo functional
pytest -v -m functional

# Solo regression
pytest -v -m regression

# Solo mobile (cualquier viewport móvil o tablet)
pytest -v -m mobile

# Suite completa
pytest -v

# Con reporte HTML portable
pytest -v --html=report.html --self-contained-html
```

Markers (`smoke`, `functional`, `regression`, `mobile`) are registered in `pytest.ini`; the default browser is forced to Chromium via `addopts`.

## Test coverage

The matrix below maps every test case to its **Category** (Smoke / Functional / Regression), Module, file and a short description. Steps for each TC are detailed in [`test_cases_steps.md`](test_cases_steps.md).

**Category summary** — Smoke: 9 · Functional: 18 · Regression / Technical: 15 · **Total: 42**.

| ID | Category | Module | File | Description |
| --- | --- | --- | --- | --- |
| TC-01 | Smoke | 1. Page Load & Core | `test_01_page_load.py` | Homepage returns HTTP 200 via `APIRequestContext` |
| TC-02 | Regression | 1. Page Load & Core | `test_01_page_load.py` | No `console.error` messages during initial load |
| TC-03 | Regression | 1. Page Load & Core | `test_01_page_load.py` | `http://creai.mx` redirects to `https://www.creai.mx` |
| TC-04 | Smoke | 1. Page Load & Core | `test_01_page_load.py` | Homepage finishes `goto()` in under 5 seconds |
| TC-05 | Smoke | 2. Header & Hero | `test_02_header_hero.py` | Navbar logo is visible |
| TC-06 | Regression | 2. Header & Hero | `test_02_header_hero.py` | Nav contains "Services" dropdown + 3 main links |
| TC-07 | Smoke | 2. Header & Hero | `test_02_header_hero.py` | "Get started" CTA is visible in the header |
| TC-08 | Smoke | 2. Header & Hero | `test_02_header_hero.py` | Header "Contact" link points to `/contact` |
| TC-09 | Smoke | 2. Header & Hero | `test_02_header_hero.py` | Hero `<h1>` matches the documented exact text |
| TC-10 | Regression | 2. Header & Hero | `test_02_header_hero.py` | Language switcher (en / es-MX) is visible |
| TC-11 | Functional | 3. Sections & Interaction | `test_03_sections_interaction.py` | "Services" dropdown opens and exposes the 3 sub-items |
| TC-12 | Smoke | 3. Sections & Interaction | `test_03_sections_interaction.py` | Homepage shows the expected H2 section headings |
| TC-13 | Regression | 3. Sections & Interaction | `test_03_sections_interaction.py` | Client logos strip is visible and contains logos |
| TC-14 | Smoke | 3. Sections & Interaction | `test_03_sections_interaction.py` | "Success stories" section renders at least one card |
| TC-15 | Functional | 3. Sections & Interaction | `test_03_sections_interaction.py` | Clicking a FAQ item expands its answer |
| TC-16 | Functional | 3. Sections & Interaction | `test_03_sections_interaction.py` | Footer banner "Contact us" CTA points to `/contact` |
| TC-17 | Functional | 4. Responsive | `test_04_responsive.py` | Mobile viewport hides desktop nav links + "Get started" CTA |
| TC-18 | Smoke | 4. Responsive | `test_04_responsive.py` | Mobile viewport keeps the logo visible |
| TC-19 | Functional | 4. Responsive | `test_04_responsive.py` | Hamburger button opens the mobile nav |
| TC-20 | Functional | 5. Sub-pages | `test_05_subpages.py` | `/services/ai-systems-framework` H1 contains expected text |
| TC-21 | Functional | 5. Sub-pages | `test_05_subpages.py` | `/services/custom-ai-solutions-factory` H1 contains expected text |
| TC-22 | Functional | 5. Sub-pages | `test_05_subpages.py` | `/services/talent-as-a-service` H1 contains expected text |
| TC-23 | Functional | 5. Sub-pages | `test_05_subpages.py` | `/success-stories` H1 contains expected text |
| TC-24 | Functional | 5. Sub-pages | `test_05_subpages.py` | `/about-us` H1 contains expected text |
| TC-25 | Functional | 5. Sub-pages | `test_05_subpages.py` | `/knowledge-hub` H1 contains expected text |
| TC-26 | Functional | 6. Internationalization | `test_06_i18n.py` | Language switcher redirects to `/es-mx` |
| TC-27 | Functional | 6. Internationalization | `test_06_i18n.py` | `/es-mx` nav menu shows Spanish labels |
| TC-28 | Functional | 6. Internationalization | `test_06_i18n.py` | `/es-mx` H1 matches the Spanish translation |
| TC-29 | Functional | 6. Internationalization | `test_06_i18n.py` | `/es-mx/about-us` H1 matches the Spanish translation |

### Extension cases (TC-30 — TC-42)

`tests/test_07_extras.py` provides additional coverage beyond the canonical 29 cases:

| ID | Category | Description |
| --- | --- | --- |
| TC-30 | Functional | Click "Success stories" nav link navigates to `/success-stories` |
| TC-31 | Functional | Click "About us" nav link navigates to `/about-us` |
| TC-32 | Functional | Click "Knowledge hub" nav link navigates to `/knowledge-hub` |
| TC-33 | Regression | Clicking the logo on a sub-page returns to the homepage |
| TC-34 | Regression | "Latest insights" section has blog posts attached to the DOM |
| TC-35 | Regression | Tablet viewport (768×1024) has no horizontal overflow |
| TC-36 | Regression | `<title>` tag is present and meaningful (≥10 chars) |
| TC-37 | Regression | `<meta name="description">` is present with content (≥30 chars) |
| TC-38 | Regression | `<meta property="twitter:image">` exposes an absolute URL |
| TC-39 | Regression | `<meta property="og:image">` exposes an absolute URL |
| TC-40 | Regression | `<html>` declares a `lang` attribute starting with `en` |
| TC-41 | Regression | `<link rel="canonical">` points to the `creai.mx` domain |
| TC-42 | Regression | **Intentional failing test** — "Get started" CTA should respond `200 OK` but the click currently fires tracking endpoints that return `204 No Content`. Kept red as a tracking flag for the backend contract. |

## HTML report

`pytest-html` is installed and `--html=report.html --self-contained-html` produces a single, portable HTML file you can share with stakeholders without an `assets/` directory.

```bash
pytest -v --html=report.html --self-contained-html
```

The generated [`report.html`](report.html) includes:

- Environment metadata (Python version, OS, plugin versions).
- A pass/fail summary at the top with filtering controls.
- One row per test with duration, marker, outcome and an expandable section that contains the full traceback when a test fails.
- Search and outcome filters to inspect only failed / passed / skipped tests.
- Because of `--self-contained-html`, every asset (CSS, JS) is inlined — the file works offline and can be emailed as-is.

**Evidence on failure** — a `pytest_runtest_makereport` hook in `conftest.py` enriches each failed row with three artifacts, embedded inline in the report (no external files):

1. **Full-page screenshot** of the browser at the moment of the failure (base64 PNG).
2. **Page context** — the URL the browser was on and the viewport dimensions.
3. **Console error log** — every `console.error` captured during the test, when the `console_errors` fixture was active.

A typical failed run inflates the report from ~65 KB to ~4 MB (depending on the number of failures and page size), but the report stays in a single portable file.

When running locally on Windows, the test session also prints a `file://` link at the end so the report can be opened directly from the terminal.

## Bug reports

Two production bugs surfaced through the suite. Both are reproducible against `https://www.creai.mx` and are reported here in standard QA format.

### BUG-001 — "Latest insights" section is hidden on the homepage

**SUMMARY**: Blog posts in the "Latest insights" section are present in the HTML but invisible to users (`display:none`).

**DESCRIPTION**: The homepage renders the `section_latest_posts` container with the CMS-loaded blog cards (`a.latest_posts-card`) inside, but the parent container ships with the CSS class `hide`, which applies `display: none`. The 3 most recent posts published in the CMS are reachable via direct URL (`/resources/<slug>`) but never appear on the homepage. Surfaced by **TC-34**.

**STEPS TO REPRODUCE**:
1. Open `https://www.creai.mx` in any modern browser at a desktop viewport (1440×900).
2. Accept the Cookiebot consent banner.
3. Scroll past the "Success stories" carousel and the "Step into the future with AI" banner.
4. Look for a section titled "Latest insights" between Success Stories and the footer.

**EXPECTED RESULT**: The "Latest insights" H2 heading is visible, followed by 3 blog post cards (each with a date, "Blog posts" tag, title, and "Read more" link) loaded from the CMS.

**ACTUAL RESULT**: There is a vertical gap where the section should be. No heading, no cards. Inspecting the DOM shows `<div class="section_latest_posts overflow-hidden hide">` containing 3 `<a class="latest_posts-card">` nodes with valid hrefs, all collapsed to `width: 0px; height: 0px` because the parent has `display: none`.

**EVIDENCE**:
- Test run: [`tests/test_07_extras.py::test_tc34_latest_insights_has_blog_posts_in_dom`](tests/test_07_extras.py) — fails with `AssertionError: Locator expected to be visible / Actual value: hidden`.
- Full-page screenshot of the live homepage (no "Latest insights" rendered): [`evidence/01_full_page.png`](evidence/01_full_page.png).
- DOM inspection dump (cards exist, `display:none` confirmed): [`evidence/02_dom_inspection.txt`](evidence/02_dom_inspection.txt).
- Screenshot of the same section after removing the `hide` class via DevTools (proof that content is alive): [`evidence/03_section_when_fixed.png`](evidence/03_section_when_fixed.png).
- Playwright video recording of the session: [`evidence/04_recording.webm`](evidence/04_recording.webm).

---

### BUG-002 — "Get started" CTA triggers HTTP 204 responses instead of 200

**SUMMARY**: Clicking the "Get started" button in the navbar fires tracking endpoints that return HTTP 204 No Content; the contract expectation is HTTP 200 OK.

**DESCRIPTION**: The "Get started" link has `href="#"` and is wired to JavaScript handlers that emit analytics events on click. Two of those events (LinkedIn Insight Tag and Google Analytics 4) return HTTP 204 No Content. While 204 is technically valid for analytics pixels, the QA contract for this CTA specifies a 200 OK response, and a 204 leaves no payload for downstream tooling to inspect or confirm receipt. Surfaced by **TC-42**.

**STEPS TO REPRODUCE**:
1. Open `https://www.creai.mx` at desktop viewport.
2. Accept the Cookiebot consent banner.
3. Open browser DevTools → Network tab, clear, and enable "Preserve log".
4. Click the "Get started" button in the top-right of the navbar.
5. Filter the Network panel by `204` status code.

**EXPECTED RESULT**: Every dynamic response triggered by the click returns HTTP 200 OK.

**ACTUAL RESULT**: Two responses return HTTP 204:
- `POST https://px.ads.linkedin.com/wa/?medium=fetch&fmt=g` → 204
- `POST https://www.google-analytics.com/g/collect?...` → 204

**EVIDENCE**:
- Test run: [`tests/test_07_extras.py::test_tc42_get_started_button_returns_200_ok`](tests/test_07_extras.py) — fails with `'Get started' generó 2 response(s) con status 204 No Content; se esperaba 200 OK`.
- HTML report row for TC-42 (expandable traceback with the full URLs): [`report.html`](report.html).
