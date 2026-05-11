## Nav
- **Selector del logo (img o svg en el header):** `.navbar11_logo-link img`
- **Href y texto de cada link del nav principal:**
  - `div#w-dropdown-toggle-1` - Texto: "Services" (Dropdown)
  - `a[href='/success-stories']` - Texto: "Success stories"
  - `a[href='/about-us']` - Texto: "About us"
  - `a[href='/knowledge-hub']` - Texto: "Knowledge hub"
- **Selector del botón/link "Get started":** `a.button_link`
- **Selector del botón/link "Contact" del header:** `a.button.is-icon[href='/contact']`
- **Selector del dropdown "Services" y sus 3 items hijos:**
  - Dropdown Toggle: `div#w-dropdown-toggle-1`
  - Item 1: `a[href='/services/ai-systems-framework']` ("AI Systems Framework")
  - Item 2: `a[href='/services/custom-ai-solutions-factory']` ("Custom AI Solutions Factory")
  - Item 3: `a[href='/services/talent-as-a-service']` ("Talent as a Service")
- **Selector del language switcher (en / es-MX):** `a.locale_link`

## Hero
- **Texto exacto del H1:** "AI-powered solutions for human-centered operations"

## Sections
- **Selector e inner text de cada H2 visible en la homepage:**
  - `h2` - "The future waits for no one. We are a team of AI innovators driven to transform the way your business operates"
  - `h2` - "Evolve and optimize your operations with our unique AI solutions"
  - `h2` - "Success stories"
  - `h2` - "Latest insights"
  - `h2` - "FAQs"
- **Selector del strip de logos de clientes (el carousel):** `div.clients_component`
- **Cuántos logos de clientes hay visibles:** 8 logos visibles/en rotación.

## Success Stories
- **Selector de las cards de success stories:** `div.success-stories_card`
- **Selector del botón "Read more" dentro de cada card:** `a.button.is-secondary`

## FAQ
- **Selector del contenedor FAQ:** `div.faq1_component`
- **Selector del trigger de cada pregunta (el elemento clickeable):** `div.faq1_question` (o el elemento `h3` que contiene)
- **¿Es un <details>/<summary> o un div con JS?:** Está implementado con elementos `<div>` utilizando JS para el toggle (no son etiquetas nativas `<details>`/`<summary>`).

## Footer/Banner
- **Selector del botón "Contact us" del banner inferior:** `a.button.is-icon.is-alternate`

## Mobile (redimensiona el browser a 375px de ancho)
- **¿Aparece un menú hamburguesa? ¿Cuál es su selector?:** Sí. Selector: `div.navbar11_menu-button`
- **¿El logo sigue visible? ¿Mismo selector?:** Sí, sigue visible y mantiene el mismo selector (`.navbar11_logo-link`).
- **¿El CTA "Get started" sigue visible o se oculta?:** Se oculta en el header móvil (es reemplazado por el ícono de "Contact" y el menú hamburguesa).

## Sub-paginas (H1 y H2)

### 1. AI Systems Framework (/services/ai-systems-framework)
- **H1:** AI Systems Framework
- **H2:**
  - Reimagine your business potential
  - Our Methodology: Strata
  - 01 Discovery
  - 02 Strategy
  - 03 Change
  - Expert-driven assessment
  - Leading your future vision
  - Partnership beyond solutions
  - Ready to bring your initiatives to life?

### 2. Custom AI Solutions Factory (/services/custom-ai-solutions-factory)
- **H1:** Custom AI Solutions Factory
- **H2:**
  - Revolutionize the way you operate
  - Driving full-spectrum innovation for business transformation
  - Building custom AI solutions that drive impact
  - Resource Allocation Optimization
  - Smart Labeling & Pattern Detection
  - Sales Opportunities Optimization
  - AI-Powered Virtual Agents
  - Digital Platform AI Builder
  - AI Process Automation & Integration
  - AI-Driven Competitive Intelligence
  - Expert-driven assessment
  - Leading your future vision
  - Partnership beyond solutions
  - Ready to bring your initiatives to life?

### 3. Talent as a Service (/services/talent-as-a-service)
- **H1:** Take your projects to the next level with expert talent perfectly matched to your unique needs
- **H2:**
  - Build your dream team of top talent.
  - Empowering your team with expert talent
  - Our specialized expertise at your service
  - Global reaching with localized impact
  - Efficiency through flexibility
  - Seamless collaboration
  - Full project ownership
  - Scalability at speed
  - Expert-driven assessment
  - Leading your future vision
  - Partnership beyond solutions
  - Ready to bring your initiatives to life?

### 4. Success Stories (/success-stories)
- **H1:** Faster, smoother, safer operations—all with AI
- **H2:**
  - Sura
  - Inter
  - Vensure
  - T-Systems
  - Cargo Expreso
  - Get the latest news
  - Ready to bring your initiatives to life?

### 5. About Us (/about-us)
- **H1:** Your trusted leaders in AI-driven solutions
- **H2:**
  - Ahead of the curve, beyond boundaries
  - Excellence is in our DNA
  - Our story
  - Our leadership team
  - Expert-driven assessment
  - Leading your future vision
  - Partnership beyond solutions
  - Ready to bring your initiatives to life?

### 6. Knowledge Hub (/knowledge-hub)
- **H1:** Resources
- **H2:**
  - Creai's Blog
  - Subscribe to our newsletter
  - Get the latest news
  - Ready to bring your initiatives to life?

---

## Español (ES-MX)

### 1. Homepage (/es-mx)
- **Nav Principal:**
  - Links: "Servicios", "Casos de éxito", "Sobre nosotros", "Recursos"
  - Botón "Get started": "Empezar"
  - Botón "Contact": "Contactar"
  - Dropdown "Servicios" (Items hijos):
    1. "Framework de Sistemas de IA"
    2. "Soluciones de IA personalizadas"
    3. "Talento como servicio"
- **Hero:**
  - H1 Exacto: "Soluciones de IA centradas en las personas"
- **Sections (H2 visibles):**
  - "El futuro no espera a nadie. Somos un equipo de innovadores en IA, comprometidos con transformar la forma en que opera tu negocio."
  - "Escala y optimiza tus operaciones con nuestras soluciones únicas de inteligencia artificial"
  - "Casos de éxito"
  - "Tendencias y novedades"
  - "FAQs"
- **Success Stories:**
  - Botón "Read more": "Leer historias de éxito"

### 2. Sub-páginas (ES-MX)

#### Framework de Sistemas de IA (/es-mx/services/ai-systems-framework)
- **H1:** Framework de Sistemas de IA
- **H2:**
  - Reimagina el potencial de tu negocio
  - Abriendo el camino hacia la transformación con IA
  - No te limites a adaptarte: lidera el camino.
  - Casos de éxito
  - FAQs

#### Soluciones de IA personalizadas (/es-mx/services/custom-ai-solutions-factory)
- **H1:** Soluciones de IA personalizadas
- **H2:**
  - Revoluciona tu forma de operar
  - Impulsamos la innovación en todos los niveles para transformar negocios
  - Evaluación y consultoría

#### Talento como servicio (/es-mx/services/talent-as-a-service)
- **H1:** Lleva tus proyectos al siguiente nivel con talento perfectamente adaptado a tus necesidades únicas
- **H2:**
  - Expertos de alto nivel seleccionados según las necesidades de tu proyecto
  - Tú evolucionas, nosotros nos adaptamos
  - Creado para ver el panorama completo
  - Ahorra dinero, tiempo y esfuerzo en contratación—nosotros lo hacemos todo por ti.
  - Impulsa el talento de tu equipo
  - FAQs

#### Casos de éxito (/es-mx/success-stories)
- **H1:** Operaciones más rápidas, fluidas y seguras, todo con IA
- **H2:**
  - Entérate de las últimas noticias
  - *(Nota: Los títulos de las historias individuales Sura, Inter, Vensure están etiquetados como H3 en esta página).*

#### Sobre nosotros (/es-mx/about-us)
- **H1:** Tus líderes de confianza en soluciones impulsadas por IA
- **H2:**
  - Nuestra historia
  - Nuestra ruta para la innovación
  - Prensa

#### Recursos (/es-mx/knowledge-hub)
- **H1:** Recursos
- **H2:**
  - Recursos
  - *(Nota: Las categorías como "Destacado" y los títulos de artículos están bajo etiquetas H3).*
