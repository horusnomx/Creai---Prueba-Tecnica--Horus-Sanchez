"""
Page Object Model para la homepage de https://www.creai.mx.

Encapsula todos los locators documentados en `selector_map.md`. Los tests
nunca deben definir locators inline: cualquier interacción con elementos
de la home pasa por esta clase.

Convenciones:
- Prioridad de locators: `get_by_role` > `get_by_text` > CSS > XPath.
- Selectores documentados en `selector_map.md` se mantienen como constantes
  de clase para que el mapeo sea trazable a la fuente.
- Los métodos devuelven `Locator` (lazy) — la espera por visibilidad la
  decide el test con `expect(...).to_be_visible(timeout=...)`.
"""

from __future__ import annotations

from playwright.sync_api import Locator, Page


class HomePage:
    """Page Object para la homepage de creai.mx."""

    URL: str = "/"

    # --- Nav ---
    LOGO: str = ".navbar11_logo-link img"
    SERVICES_DROPDOWN_TOGGLE: str = "div#w-dropdown-toggle-1"
    SERVICE_ITEM_FRAMEWORK: str = "a[href='/services/ai-systems-framework']"
    SERVICE_ITEM_CUSTOM: str = "a[href='/services/custom-ai-solutions-factory']"
    SERVICE_ITEM_TALENT: str = "a[href='/services/talent-as-a-service']"
    NAV_SUCCESS_STORIES: str = "a[href='/success-stories']"
    NAV_ABOUT_US: str = "a[href='/about-us']"
    NAV_KNOWLEDGE_HUB: str = "a[href='/knowledge-hub']"
    CTA_GET_STARTED: str = "a.button_link"
    CONTACT_HEADER: str = "a.button.is-icon[href='/contact']"
    LANGUAGE_SWITCHER: str = "a.locale_link"
    HAMBURGER_MENU: str = "div.navbar11_menu-button"

    # --- Sections ---
    # Nota: selector_map.md describe `div.clients_component`. El DOM real
    # tiene DOS zonas relacionadas con logos:
    #  - `div.logo3_component` cerca del hero (renderizada, con imágenes).
    #  - `div.clients-wrapper` en la sección 'Clients section' (height:0,
    #    vacía en el deploy actual).
    # Usamos `logo3_component` porque es el strip realmente visible.
    CLIENT_LOGOS_STRIP: str = "div.logo3_component"
    # selector_map.md describe `div.success-stories_card`, pero el sitio fue
    # rediseñado: los "cards" ahora son enlaces "Read more" dentro de un Swiper,
    # con href apuntando a la sub-página del caso. Se usa el href como proxy.
    SUCCESS_STORY_CARD: str = "a[href^='/success-stories/']"
    SUCCESS_STORY_READ_MORE: str = "a.button.is-secondary"

    # --- FAQ ---
    # selector_map.md indica `faq1_*`; el DOM real usa el componente `faq6_*`.
    FAQ_CONTAINER: str = "div.faq6_component"
    FAQ_QUESTION_TRIGGER: str = "div.faq6_question"
    FAQ_ANSWER: str = "div.faq6_answer"

    # --- Footer banner ---
    FOOTER_CTA: str = "a.button.is-icon.is-alternate"

    # --- Cookie consent (Cookiebot) ---
    COOKIE_DIALOG: str = "#CybotCookiebotDialog"
    COOKIE_ACCEPT_BUTTON: str = "#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"

    def __init__(self, page: Page) -> None:
        """Recibe la `page` de Playwright proporcionada por el fixture."""
        self.page = page

    def goto(self) -> None:
        """Navega a la homepage usando el `base_url` del context."""
        self.page.goto(self.URL)

    def dismiss_cookie_banner(self, timeout_ms: int = 5_000) -> None:
        """
        Acepta el banner de Cookiebot si aparece dentro de `timeout_ms`.

        Idempotente: si el banner no se monta a tiempo (o ya fue aceptado),
        retorna sin error. Aceptarlo persiste la cookie de consentimiento en
        el browser context, por lo que navegaciones posteriores en el mismo
        context ya no muestran el dialog y los clicks no son interceptados
        por `#CybotCookiebotDialogBodyUnderlay`.

        Fallback: si el botón 'Allow all' no responde, elimina el dialog y
        el underlay del DOM para garantizar que la página sea operable.
        """
        dialog = self.page.locator(self.COOKIE_DIALOG)
        try:
            dialog.wait_for(state="visible", timeout=timeout_ms)
        except Exception:
            return
        try:
            self.page.locator(self.COOKIE_ACCEPT_BUTTON).click(timeout=timeout_ms)
            dialog.wait_for(state="hidden", timeout=timeout_ms)
        except Exception:
            self.page.evaluate(
                "() => {"
                "  ['CybotCookiebotDialog', 'CybotCookiebotDialogBodyUnderlay']"
                "    .forEach(id => { const el = document.getElementById(id);"
                "                     if (el) el.remove(); });"
                "}"
            )

    # ---------- Nav ----------

    def get_logo(self) -> Locator:
        """
        Logo del navbar (img dentro del link del logo).

        El selector matchea 2 elementos porque el sitio renderiza variantes
        del navbar (desktop + móvil) en el DOM; se devuelve la primera
        instancia para evitar strict mode violations.
        """
        return self.page.locator(self.LOGO).first

    def get_nav_links(self) -> Locator:
        """
        Locator con las 4 entradas principales del nav: el toggle 'Services'
        y los links 'Success stories', 'About us' y 'Knowledge hub'.
        """
        selector = ", ".join(
            [
                self.SERVICES_DROPDOWN_TOGGLE,
                self.NAV_SUCCESS_STORIES,
                self.NAV_ABOUT_US,
                self.NAV_KNOWLEDGE_HUB,
            ]
        )
        return self.page.locator(selector)

    def get_cta_button(self) -> Locator:
        """CTA principal 'Get started' del header."""
        return self.page.locator(self.CTA_GET_STARTED).first

    def get_contact_link(self) -> Locator:
        """
        Link/botón 'Contact' del header.

        El selector matchea múltiples instancias (variantes desktop/móvil del
        navbar y banner inferior comparten `a[href='/contact']`); se devuelve
        la primera coincidencia, que corresponde al header de escritorio.
        """
        return self.page.locator(self.CONTACT_HEADER).first

    def get_services_dropdown(self) -> Locator:
        """Toggle (no abierto) del dropdown 'Services'."""
        return self.page.locator(self.SERVICES_DROPDOWN_TOGGLE)

    def open_services_dropdown(self) -> Locator:
        """
        Abre el dropdown 'Services' y devuelve los 3 items hijos del panel abierto:
        AI Systems Framework, Custom AI Solutions Factory y Talent as a Service.

        Hace click en el toggle del navbar clonado por Finsweet Smart Nav (último
        en DOM order); el original queda detrás y sus pointer events son
        interceptados por el clon.

        El locator de items se scopea a `.w-dropdown-list.w--open` (clase que
        Webflow añade al panel activo) para no contar instancias duplicadas
        de los mismos hrefs en otras zonas de la página.
        """
        self.page.locator(self.SERVICES_DROPDOWN_TOGGLE).last.click()
        open_panel = self.page.locator(".w-dropdown-list.w--open")
        items_selector = ", ".join(
            [
                self.SERVICE_ITEM_FRAMEWORK,
                self.SERVICE_ITEM_CUSTOM,
                self.SERVICE_ITEM_TALENT,
            ]
        )
        return open_panel.locator(items_selector)

    def click_nav_link(self, href: str) -> None:
        """
        Hace click en el link del nav principal cuyo href es `href`.

        Usa `.last` para target la instancia del navbar clonada por Finsweet
        Smart Nav, que es la que recibe los pointer events del usuario.
        """
        self.page.locator(f"a[href='{href}']").last.click()

    def click_logo(self) -> None:
        """
        Hace click en el logo del navbar para volver a la home.

        Usa `.last` por la misma razón que `click_nav_link`: el clon de Smart
        Nav se monta encima del navbar original.
        """
        self.page.locator(".navbar11_logo-link").last.click()

    def get_language_switcher(self) -> Locator:
        """Link de cambio de idioma (en ↔ es-MX)."""
        return self.page.locator(self.LANGUAGE_SWITCHER)

    def get_hamburger_menu(self) -> Locator:
        """Botón del menú hamburguesa (visible solo en viewport móvil)."""
        return self.page.locator(self.HAMBURGER_MENU)

    # ---------- Sections ----------

    def get_section_headings(self) -> Locator:
        """Todos los H2 de la homepage (5 visibles según `selector_map.md`)."""
        return self.page.locator("h2")

    def get_client_logos(self) -> Locator:
        """Strip/carousel de logos de clientes."""
        return self.page.locator(self.CLIENT_LOGOS_STRIP)

    def get_success_story_cards(self) -> Locator:
        """Cards de la sección 'Success stories'."""
        return self.page.locator(self.SUCCESS_STORY_CARD)

    def get_blog_posts(self) -> Locator:
        """
        Cards de la sección 'Latest insights' / 'Latest posts'.

        Inspección del DOM real: las cards usan la clase `latest_posts-card`
        y apuntan a `/resources/<slug>`. La sección padre (`section_latest_posts`)
        puede estar oculta con `display:none` (clase `hide`) según el estado
        del CMS; los cards siguen en el DOM, así que este locator devuelve
        elementos *attached* aunque no necesariamente *visible*.
        """
        return self.page.locator("a.latest_posts-card")

    # ---------- FAQ ----------

    def get_faq_items(self) -> Locator:
        """Triggers (`div.faq1_question`) dentro del contenedor FAQ."""
        return self.page.locator(self.FAQ_CONTAINER).locator(
            self.FAQ_QUESTION_TRIGGER
        )

    def click_faq_item(self, index: int) -> None:
        """Hace click en el FAQ trigger en la posición `index` (0-based)."""
        self.get_faq_items().nth(index).click()

    # ---------- Footer ----------

    def get_footer_cta(self) -> Locator:
        """Botón 'Contact us' del banner inferior."""
        return self.page.locator(self.FOOTER_CTA)
