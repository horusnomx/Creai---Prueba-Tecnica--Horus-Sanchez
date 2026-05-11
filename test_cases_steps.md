# Descripción Paso a Paso de los Test Cases (TC-01 a TC-42)

> **Discrepancias entre `selector_map.md` y DOM real**: durante la implementación se descubrió que el sitio fue actualizado tras la generación del `selector_map.md`. Los selectores reales utilizados están documentados en cada TC y en `pages/home_page.py`. Los cambios clave:
>
> - **FAQ**: componente `faq1_*` reemplazado por `faq6_*`.
> - **Clientes**: `div.clients_component` ahora vacío; el strip activo es `div.logo3_component`.
> - **Success stories**: ya no hay `div.success-stories_card`; los items son botones "Read more" con `href^="/success-stories/<slug>"`.
> - **Latest insights**: sección presente en DOM pero con clase `hide` (display:none) en este deploy.
> - **Navbar duplicado**: Webflow + Finsweet Smart Nav clonan `navbar11_component`. `.first` apunta al original (oculto detrás), `.last` al clon (interactuable). Los métodos del POM `click_nav_link()`, `click_logo()` y `open_services_dropdown()` ya usan `.last`.
> - **Cookiebot**: el dialog de consentimiento intercepta pointer events; el POM expone `dismiss_cookie_banner()` (idempotente, con fallback a remoción JS).
> - **H1 de sub-páginas**: `/services/talent-as-a-service` muestra "Talent as a Service" (no la frase larga); `/knowledge-hub` muestra "Knowledge hub" (no "Resources").

---

## Módulo 1: Page Load & Core (tests/test_01_page_load.py)

### **TC-01: La homepage devuelve HTTP 200**
1. Crear un contexto de API (`APIRequestContext`) independiente del navegador.
2. Ejecutar una petición GET directa a la base URL (`https://www.creai.mx`).
3. Capturar la respuesta del servidor.
4. Validar mediante aserción que el código de estado (`response.status`) sea exactamente `200`.

### **TC-02: No hay errores de consola en la carga inicial**
1. La fixture `console_errors` (conftest.py) suscribe un listener al evento `console` antes de la navegación.
2. Navegar a la homepage con `home.goto()`.
3. Esperar a que el `<h1>` principal sea visible (asegura que el JS y el DOM clave terminaron de cargar).
4. Validar que la lista de mensajes de tipo `error` esté vacía.

### **TC-03: Redirección automática de HTTP a HTTPS**
1. Forzar una navegación directa a la versión insegura: `http://creai.mx`.
2. Esperar a que termine la carga de la página.
3. Extraer la URL final resuelta (`page.url`).
4. Validar que la URL resultante comience con `https://www.creai.mx`.

### **TC-04: La homepage carga en menos de 5 segundos**
1. Guardar el `timestamp` del sistema actual (inicio).
2. Ejecutar la navegación a la homepage (`page.goto()`).
3. Guardar el `timestamp` justo después de que la función de navegación retorne (fin).
4. Calcular la diferencia de tiempo.
5. Validar que el tiempo transcurrido sea estrictamente menor a 5.0 segundos.

---

## Módulo 2: Header & Hero (tests/test_02_header_hero.py)

### **TC-05: Logo visible**
1. Navegar a la homepage.
2. Localizar el elemento usando el selector `.navbar11_logo-link img` (el POM aplica `.first` para evitar strict mode con duplicación de navbar).
3. Validar con `expect(locator).to_be_visible()`.

### **TC-06: Nav muestra links principales**
1. Navegar a la homepage.
2. Localizar el toggle del dropdown de servicios (`div#w-dropdown-toggle-1`) y validar su visibilidad.
3. Iterar sobre el arreglo de hrefs esperados (`/success-stories`, `/about-us`, `/knowledge-hub`).
4. Para cada href, validar que exista un `<a>` con el atributo exacto y sea visible.

### **TC-07: CTA "Get started" visible**
1. Navegar a la homepage.
2. Localizar el botón con `a.button_link` (POM aplica `.first`).
3. Validar visibilidad en viewport de escritorio.

### **TC-08: Botón "Contact" en header**
1. Navegar a la homepage.
2. Buscar `a.button.is-icon[href='/contact']` (POM aplica `.first` — el selector matchea 5 instancias entre navbars + footer).
3. Validar visibilidad.
4. Validar que el atributo `href` sea exactamente `/contact`.

### **TC-09: H1 del Hero exacto**
1. Navegar a la homepage.
2. Localizar el primer `<h1>` de la página.
3. Validar que sea visible.
4. Validar que su texto coincida carácter por carácter con `"AI-powered solutions for human-centered operations"`.

### **TC-10: Language switcher visible**
1. Navegar a la homepage.
2. Localizar el switcher con `a.locale_link` (POM aplica `.first`).
3. Validar visibilidad.

---

## Módulo 3: Secciones de la Homepage e Interacción (tests/test_03_sections_interaction.py)

### **TC-11: Interacción del dropdown "Services"**
1. Navegar a la homepage y aceptar cookies.
2. Hacer click en el toggle `div#w-dropdown-toggle-1` (usando `.last` — el clon del Smart Nav es el interactivo).
3. Scopear los items al panel abierto: `.w-dropdown-list.w--open` (clase que Webflow añade al panel activo).
4. Validar que existan exactamente 3 items con `to_have_count(3)`.
5. Para cada uno de los 3 hrefs esperados, validar `to_have_count(1)` dentro del panel.

### **TC-12: Verificación de H2s en Homepage**
1. Navegar a la homepage y aceptar cookies.
2. Para cada fragmento de H2 esperado, ejecutar `page.locator("h2:visible").filter(has_text=fragment).first`.
3. Validar visibilidad de cada uno.
4. Lista esperada (4 H2s visibles): "The future waits for no one", "Evolve and optimize your operations", "Success stories", "FAQs".
5. **Nota**: `selector_map.md` también listaba "Latest insights" pero la sección padre tiene `display:none` en el deploy actual (ver TC-34).

### **TC-13: Strip de logos de clientes**
1. Navegar a la homepage y aceptar cookies.
2. Localizar `div.logo3_component` (POM aplica `.first`).
3. Validar visibilidad del strip.
4. Validar que contenga al menos 1 imagen (`<img>`).
5. **Nota**: `selector_map.md` decía `div.clients_component`; en el DOM real esa zona (`clients-wrapper`) está vacía (height:0). El strip activo está cerca del hero.

### **TC-14: Cards de Success Stories**
1. Navegar a la homepage y aceptar cookies.
2. Localizar enlaces con `a[href^='/success-stories/']` (los CTAs "Read more" de cada card del Swiper).
3. Validar que el primer card sea visible.
4. Validar que haya al menos 1 card renderizada.
5. **Nota**: el sitio fue rediseñado — ya no existe `div.success-stories_card`; los cards son botones "Read more" dentro de un Swiper.

### **TC-15: Interacción del FAQ (Acordeón)**
1. Navegar a la homepage y aceptar cookies.
2. Scrollear hacia `div.faq6_component` (selector real; `selector_map.md` decía `faq1_*`).
3. Capturar la altura inicial del primer `.faq6_answer` (≈8px, colapsado).
4. Hacer click en la primera `.faq6_question` (POM `click_faq_item(0)`).
5. Usar `page.wait_for_function()` para esperar que la altura crezca al menos 30px por encima del baseline.
6. **Nota**: Webflow `faq6_*` no usa `aria-expanded`; el toggle se basa en animar la altura del answer.

### **TC-16: CTA del Footer**
1. Navegar a la homepage y aceptar cookies.
2. Localizar el botón con `a.button.is-icon.is-alternate`.
3. Validar visibilidad.
4. Validar que el atributo `href` sea `/contact`.

---

## Módulo 4: Responsive / Mobile View (tests/test_04_responsive.py)

*Estos tests usan la fixture `mobile_page` con viewport 375x812 (iPhone X).*

### **TC-17: Menú y CTA ocultos en móvil**
1. Cargar la homepage en viewport móvil (375x812) y aceptar cookies.
2. Validar con `to_be_hidden()` que el CTA `a.button_link` esté oculto via media queries.
3. Para cada uno de los 3 nav links principales (`/success-stories`, `/about-us`, `/knowledge-hub`), validar que estén ocultos.

### **TC-18: Logo visible en móvil**
1. Cargar la homepage en viewport móvil y aceptar cookies.
2. Localizar el logo `.navbar11_logo-link img` (POM aplica `.first`).
3. Validar que permanezca visible.

### **TC-19: Apertura del menú hamburguesa**
1. Cargar la homepage en viewport móvil y aceptar cookies.
2. Localizar `div.navbar11_menu-button` con `.last` (el clon del Smart Nav es el interactivo).
3. Validar que sea visible.
4. Validar que el primer nav link esté oculto (estado cerrado).
5. Hacer click en el botón hamburguesa.
6. Validar con `page.locator("...:visible")` que el nav link ahora sea visible en al menos una instancia tras la animación.

---

## Módulo 5: Sub-páginas principales (tests/test_05_subpages.py)

*Cada test navega directamente a la sub-página y valida que el H1 visible contenga el texto esperado (`to_contain_text` — más lenient que `to_have_text` porque algunos H1 incluyen texto adyacente concatenado en `textContent`).*

### **TC-20: /services/ai-systems-framework**
1. `page.goto("/services/ai-systems-framework", wait_until="domcontentloaded")`.
2. Localizar `h1:visible` y validar que contenga `"AI Systems Framework"`.

### **TC-21: /services/custom-ai-solutions-factory**
1. `page.goto("/services/custom-ai-solutions-factory", wait_until="domcontentloaded")`.
2. Localizar `h1:visible` y validar que contenga `"Custom AI Solutions Factory"`.

### **TC-22: /services/talent-as-a-service**
1. `page.goto("/services/talent-as-a-service", wait_until="domcontentloaded")`.
2. Localizar `h1:visible` y validar que contenga `"Talent as a Service"`.
3. **Nota**: `selector_map.md` documentaba el H1 como `"Take your projects to the next level with expert talent perfectly matched to your unique needs"`, pero el sitio actual muestra solo `"Talent as a Service"`.

### **TC-23: /success-stories**
1. `page.goto("/success-stories", wait_until="domcontentloaded")`.
2. Localizar `h1:visible` y validar que contenga `"Faster, smoother, safer operations—all with AI"`.

### **TC-24: /about-us**
1. `page.goto("/about-us", wait_until="domcontentloaded")`.
2. Localizar `h1:visible` y validar que contenga `"Your trusted leaders in AI-driven solutions"`.

### **TC-25: /knowledge-hub**
1. `page.goto("/knowledge-hub", wait_until="domcontentloaded")`.
2. Localizar `h1:visible` y validar que contenga `"Knowledge hub"`.
3. **Nota**: `selector_map.md` decía `"Resources"` pero el sitio actual muestra `"Knowledge hub"`.

---

## Módulo 6: Internacionalización (ES-MX) (tests/test_06_i18n.py)

### **TC-26: Redirección del Language Switcher**
1. Navegar a la versión en inglés (base URL) y aceptar cookies.
2. Hacer click en `a.locale_link[href*='/es-mx']` (con `.last`).
3. Esperar a que la URL contenga `/es-mx` con `expect(page).to_have_url(regex)`.

### **TC-27: Traducción del Menú de Navegación**
1. Navegar directamente a `/es-mx`.
2. Para cada etiqueta esperada (`"Servicios"`, `"Casos de éxito"`, `"Sobre nosotros"`, `"Recursos"`):
   - Buscar un link o div visible cuyo texto coincida con la etiqueta.
   - Validar visibilidad.

### **TC-28: Traducción del H1 de Homepage**
1. Navegar a `/es-mx`.
2. Localizar `h1:visible` (primer match).
3. Validar que el texto exacto sea `"Soluciones de IA centradas en las personas"`.

### **TC-29: Traducción de Sub-páginas**
1. Navegar a `/es-mx/about-us`.
2. Localizar `h1:visible` (primer match).
3. Validar que el texto exacto sea `"Tus líderes de confianza en soluciones impulsadas por IA"`.

---

## Módulo 7: Extras y contratos HTTP (tests/test_07_extras.py)

*Tests complementarios al alcance original del documento; cubren clicks en cada nav link, retorno por logo, blog en DOM, layout tablet, metadata SEO y contrato HTTP del CTA principal.*

### **TC-30: Click en "Success stories" del nav**
1. Navegar a la homepage y aceptar cookies.
2. Llamar a `home.click_nav_link("/success-stories")` (POM usa `.last` para el clon del Smart Nav).
3. Validar que la URL resultante haga match con `/success-stories/?$`.

### **TC-31: Click en "About us" del nav**
1. Navegar a la homepage y aceptar cookies.
2. Llamar a `home.click_nav_link("/about-us")`.
3. Validar que la URL haga match con `/about-us/?$`.

### **TC-32: Click en "Knowledge hub" del nav**
1. Navegar a la homepage y aceptar cookies.
2. Llamar a `home.click_nav_link("/knowledge-hub")`.
3. Validar que la URL haga match con `/knowledge-hub/?$`.

### **TC-33: Logo regresa a la home**
1. Navegar a la homepage y aceptar cookies.
2. Llamar a `home.click_nav_link("/about-us")`.
3. Validar URL en `/about-us/?$`.
4. Llamar a `home.click_logo()`.
5. Validar URL en `^https://www\.creai\.mx/?$`.

### **TC-34: Blog posts en "Latest insights" (FALLO ESPERADO)**
1. Navegar a la homepage y aceptar cookies.
2. Localizar `a.latest_posts-card`.
3. Validar con `expect(posts.first).to_be_visible()` — el test falla intencionalmente porque la sección padre tiene `display:none` en el deploy actual. Fallo esperado: expone bug de visibilidad.
4. Validar `count() >= 1`.

### **TC-35: Sin overflow horizontal en tablet**
1. Cargar la homepage con la fixture `tablet_page` (viewport 768x1024) y aceptar cookies.
2. Vía `page.evaluate()`, extraer `document.documentElement.scrollWidth` y `clientWidth`.
3. Validar `scrollWidth <= clientWidth` (sin scroll horizontal).

### **TC-36: `<title>` presente y significativo**
1. Navegar a la homepage.
2. Obtener `page.title()` y aplicar `.strip()`.
3. Validar que no esté vacío y tenga al menos 10 caracteres.

### **TC-37: Meta description presente**
1. Localizar `meta[name='description']` (`.first`).
2. Validar `to_be_attached()`.
3. Extraer atributo `content` y validar longitud ≥ 30 caracteres.

### **TC-38: Twitter image absoluta**
1. Localizar `meta[property='twitter:image']` (`.first`).
2. Validar `to_be_attached()`.
3. Validar que `content` comience con `http://` o `https://`.
4. **Nota**: el sitio no expone `og:title` ni `og:description` actualmente — solo `og:image` y `twitter:image`. El título queda cubierto por TC-36 y la descripción por TC-37.

### **TC-39: Open Graph image absoluta**
1. Localizar `meta[property='og:image']` (`.first`).
2. Validar `to_be_attached()`.
3. Validar que `content` comience con `http://` o `https://`.

### **TC-40: Atributo `lang` del `<html>`**
1. Vía `page.evaluate()`, extraer `document.documentElement.lang`.
2. Validar que no esté vacío.
3. Validar que comience con `en` (la home en inglés debe declarar `en` o variante).

### **TC-41: Canonical link**
1. Localizar `link[rel='canonical']` (`.first`).
2. Validar `to_be_attached()`.
3. Extraer atributo `href` y validar que comience con `https://www.creai.mx`.

### **TC-42: Contrato HTTP del botón "Get started" (FALLO INTENCIONAL)**
> **Estado actual**: este test está diseñado para fallar — el sitio responde HTTP 204 No Content en endpoints de tracking disparados por el click, pero la especificación pide 200 OK. Permanecerá en rojo como red flag hasta que el backend devuelva 200 o se decida cambiar la especificación.

1. Navegar a la homepage y aceptar cookies.
2. Suscribir un listener al evento `response` del browser context que acumule todas las responses.
3. Localizar el botón con `a.button_link` (`.last` — clon del Smart Nav).
4. Hacer click.
5. Esperar a que la red entre en idle con `page.wait_for_load_state("networkidle", timeout=15_000)`.
6. Filtrar las responses dinámicas (excluir assets estáticos `.css/.js/.png/etc.` y preflights `OPTIONS`).
7. Validar que NINGUNA de esas responses dinámicas tenga `status == 204`.
8. Si hay 204s, fallar con un mensaje diagnóstico que incluya las URLs afectadas.

**Hallazgo manual confirmado por el test**: el click dispara dos endpoints de tracking que responden 204:
- `https://px.ads.linkedin.com/wa/?medium=fetch&fmt=g` (LinkedIn Insight Tag)
- `https://www.google-analytics.com/g/collect?...` (Google Analytics 4)

---

## Apéndice: estructura de archivos

```
creai-smoke-tests/
├── conftest.py                              # fixtures: page, console_errors, mobile_page, tablet_page
├── pages/
│   └── home_page.py                         # Page Object Model con todos los selectores
├── tests/
│   ├── test_01_page_load.py                 # TC-01..04
│   ├── test_02_header_hero.py               # TC-05..10
│   ├── test_03_sections_interaction.py      # TC-11..16
│   ├── test_04_responsive.py                # TC-17..19 (también marcados @pytest.mark.mobile)
│   ├── test_05_subpages.py                  # TC-20..25
│   ├── test_06_i18n.py                      # TC-26..29
│   └── test_07_extras.py                    # TC-30..42 (TC-35 también @pytest.mark.mobile)
├── pytest.ini                               # markers smoke + mobile
├── requirements.txt
├── selector_map.md                          # snapshot original (Antigravity), NO editar
└── test_cases_steps.md                      # este documento
```

## Apéndice: comandos

```bash
pytest -v                                    # todos los TC (42 tests)
pytest -v -m smoke                           # todos (smoke aplica a todos los tests)
pytest -v -m mobile                          # solo TC-17, TC-18, TC-19, TC-35
pytest -v --html=report.html --self-contained-html
                                             # reporte HTML portable
pytest tests/test_05_subpages.py -v          # un módulo
pytest tests/test_07_extras.py::test_tc42_get_started_button_returns_200_ok -v
                                             # un solo TC
```
