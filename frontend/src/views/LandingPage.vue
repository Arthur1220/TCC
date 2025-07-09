<template>
  <div>
    <AppHeader />
    <main role="main">
      <section class="hero section text-center">
        <div class="container">
          <h1 class="hero-title">Rastreabilidade Completa para Seu Rebanho</h1>
          <p class="hero-subtitle">Transparência, segurança e auditabilidade em blockchain de segunda camada.</p>
          <button class="button button-primary button-lg" @click="goToSignup">Experimente Grátis</button>
        </div>
      </section>

      <section id="benefits" class="section benefits-section">
        <div class="container">
          <h2 class="section-title-global">Benefícios da Rastreabilidade Inteligente</h2>
          <div class="benefits-wrapper">
            <button
              v-if="showArrows"
              class="carousel-control prev"
              @click="scrollLeft"
              aria-label="Benefício Anterior"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="24" height="24"><path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/></svg>
            </button>
            <div class="benefits-carousel" ref="carousel">
              <div class="benefit-card card" v-for="item in benefits" :key="item.text">
                <img :src="item.icon" :alt="`Ícone ${item.text}`" class="benefit-icon" />
                <p class="benefit-text">{{ item.text }}</p>
              </div>
            </div>
            <button
              v-if="showArrows"
              class="carousel-control next"
              @click="scrollRight"
              aria-label="Próximo Benefício"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="24" height="24"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/></svg>
            </button>
          </div>
        </div>
      </section>

      <section id="details" class="section how-it-works-section">
        <div class="container">
          <h2 class="section-title-global">Como Nossa Plataforma Funciona</h2>
          <div class="timeline">
            <div
              class="timeline-step"
              v-for="(step, index) in steps"
              :key="step.title"
              :class="{ 'timeline-step-even': (index + 1) % 2 === 0 }"
            >
              <div class="timeline-marker-container">
                <div class="timeline-marker">{{ index + 1 }}</div>
              </div>
              <div class="timeline-content card">
                <img :src="step.icon" :alt="`Ícone ${step.title}`" class="timeline-icon" />
                <h3 class="timeline-step-title">{{ step.title }}</h3>
                <p>{{ step.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="plans" class="section pricing-section">
        <div class="container">
          <h2 class="section-title-global">Cobrança Simplificada e Transparente</h2>
          <div class="grid pricing-grid">
            <div class="card pricing-card" v-for="(plan, idx) in pricing" :key="idx">
              <div class="pricing-icon" v-html="plan.icon"></div>
              <h3 class="pricing-card-title">{{ plan.title }}</h3>
              <p>{{ plan.description }}</p>
            </div>
          </div>
          <p class="pricing-note">
            Tudo isso sem precisar gerenciar carteiras próprias ou lidar com custos ocultos. É só usar e pagar de forma clara e previsível.
          </p>
        </div>
      </section>

      <section id="faq" class="section faq-section">
        <div class="container">
          <h2 class="section-title-global">Perguntas Frequentes (FAQ)</h2>
          <div class="faq-list">
            <div class="faq-item" v-for="(faq, idx) in faqs" :key="idx">
              <button
                class="faq-question"
                @click="toggleFaq(idx)"
                :aria-expanded="faq.open.toString()"
                :aria-controls="`faq-answer-${idx}`"
              >
                <span>{{ faq.question }}</span>
                <span class="faq-icon" aria-hidden="true">{{ faq.open ? '−' : '+' }}</span>
              </button>
              <div v-show="faq.open" :id="`faq-answer-${idx}`" class="faq-answer">
                <p>{{ faq.answer }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="footer-cta section gradient-bg text-center">
        <div class="container footer-cta-container">
          <h2 class="cta-title">Pronto para transformar sua rastreabilidade?</h2>
          <p class="cta-subtitle">Comece hoje e veja a diferença na segurança e eficiência da sua produção.</p>
          <button class="button button-primary button-lg footer-cta-button" @click="goToSignup">Cadastre-se Gratuitamente</button>
        </div>
      </section>
    </main>
    <AppFooter />
  </div>
</template>

<script>
// Seu script existente permanece o mesmo.
import AppHeader from '../components/AppHeader.vue';
import AppFooter from '../components/AppFooter.vue';

export default {
  name: 'LandingPage',
  components: { AppHeader, AppFooter },
  data() {
    return {
      benefits: [
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/lock.png', text: 'Imutabilidade de Registros' },
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/refund-2.png', text: 'Redução de Custos' },
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/flow-chart.png', text: 'Integração Facilitada' },
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/rocket.png', text: 'Alta Performance' },
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/shield.png', text: 'Segurança e Conformidade' },
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/visible.png', text: 'Transparência Total' },
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/graph-report.png', text: 'Auditoria Confiável' }
      ],
      steps: [
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/add-user-group-man-man.png', title: '1. Cadastro Rápido', description: 'Crie sua conta em minutos e conecte-se à nossa plataforma segura.' },
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/document.png', title: '2. Registro de Eventos', description: 'Insira eventos críticos como nascimento, vacinação, e movimentações de forma intuitiva.' },
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/checked-checkbox.png', title: '3. Validação em Blockchain', description: 'Smart contracts verificam e registram a integridade dos seus dados em uma blockchain L2 eficiente.' },
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/data-arrived.png', title: '4. Sincronização Segura', description: 'Seus dados off-chain são mantidos em sincronia com os hashes on-chain, garantindo segurança e acesso rápido.' },
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/combo-chart.png', title: '5. Consulta e Auditoria', description: 'Acesse seu dashboard para relatórios detalhados, insights e trilhas de auditoria completas.' }
      ],
      pricing: [
        { icon: '📄', title: 'Faturamento Único', description: 'Receba uma única fatura mensal que consolida todas as operações, simplificando sua gestão financeira.' },
        { icon: '📈', title: 'Relatórios de Uso', description: 'Acesse relatórios transparentes com resumo de transações, taxas aplicadas e consumo total para auditoria.' },
        { icon: '🔗', title: 'Exportação Flexível', description: 'Exporte dados em CSV, PDF ou integre diretamente via API, facilitando a contabilidade e a análise.' }
      ],
      faqs: [
        { question: 'Como a segurança dos meus dados é garantida?', answer: 'Utilizamos criptografia de ponta e hashes em blockchain para garantir imutabilidade, rastreabilidade e resistência a fraudes.', open: false },
        { question: 'Preciso entender de blockchain para usar?', answer: 'Não. Nossa plataforma foi desenhada para abstrair toda a complexidade. Você usa uma interface web amigável, e nós cuidamos da tecnologia.', open: false },
        { question: 'Consigo exportar relatórios para auditoria?', answer: 'Sim. Gere relatórios customizáveis com filtros avançados e exporte facilmente nos formatos CSV ou PDF.', open: false },
        { question: 'A plataforma é adequada para pequenos produtores?', answer: 'Sim! Nossa solução é escalável e pensada para atender desde pequenos produtores até grandes cooperativas, com planos flexíveis.', open: false }
      ],
      showArrows: true,
      resizeTimeout: null
    };
  },
  mounted() {
    this.$nextTick(() => this.checkArrows());
    window.addEventListener('resize', this.checkArrowsDebounced);
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.checkArrowsDebounced);
    if (this.resizeTimeout) clearTimeout(this.resizeTimeout);
  },
  methods: {
    goToSignup() { this.$router.push('/login'); },
    scrollCarousel(direction) {
      const carousel = this.$refs.carousel;
      if (!carousel) return;
      const scrollAmount = carousel.offsetWidth * 0.8;
      carousel.scrollBy({ left: direction === 'left' ? -scrollAmount : scrollAmount, behavior: 'smooth' });
    },
    scrollLeft() { this.scrollCarousel('left'); },
    scrollRight() { this.scrollCarousel('right'); },
    checkArrows() {
      const c = this.$refs.carousel;
      this.showArrows = c ? c.scrollWidth > c.clientWidth + 1 : false;
    },
    checkArrowsDebounced() {
        if (this.resizeTimeout) clearTimeout(this.resizeTimeout);
        this.resizeTimeout = setTimeout(this.checkArrows, 150);
    },
    toggleFaq(index) {
      this.faqs[index].open = !this.faqs[index].open;
      this.faqs.forEach((faq, i) => {
        if (i !== index) faq.open = false;
      });
    }
  }
};
</script>

<style scoped>
/* Estilos Globais da Página */
.section {
  padding: 5rem 1.5rem;
}
.section:nth-child(even) {
  background-color: var(--color-bg-muted);
}
.text-center {
  text-align: center;
}
.section-title-global {
  font-family: var(--font-heading);
  font-size: var(--fs-h2);
  color: var(--color-text-primary);
  text-align: center;
  margin-bottom: var(--sp-xl);
}
.section-title-global::after {
  content: '';
  display: block;
  width: 60px;
  height: 3px;
  background-color: var(--color-primary);
  margin: var(--sp-sm) auto 0;
}

/* Hero Section */
.hero {
  padding: 5rem 1.5rem; /* Padding vertical reduzido */
}
/* CORREÇÃO APLICADA: Hierarquia e responsividade dos títulos */
.title {
  font-size: var(--fs-h5); /* Tamanho menor, como um subtítulo */
  font-weight: var(--fw-semibold);
  color: var(--color-primary);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: var(--sp-sm);
}
.hero-title {
  font-size: var(--fs-h1);
  font-weight: var(--fw-bold);
  color: var(--color-text-primary);
  margin-bottom: var(--sp-md);
  line-height: 1.2;
}
.hero-subtitle {
  font-size: var(--fs-large);
  color: var(--color-text-secondary);
  margin-bottom: var(--sp-xl);
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}
.hero .button {
  font-size: var(--fs-large);
  padding: var(--sp-md) var(--sp-xl);
}

/* Benefits Section */
.benefits-section {
    background-color: var(--color-bg-component);
}
.benefits-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}
.benefits-carousel {
  display: flex;
  overflow-x: auto;
  gap: var(--sp-lg);
  padding: var(--sp-md) var(--sp-sm);
  flex-grow: 1;
  scrollbar-width: none;
}
.benefits-carousel::-webkit-scrollbar {
  display: none;
}
.carousel-control {
  background: var(--color-bg-component);
  border: var(--border-width) solid var(--color-border);
  color: var(--color-primary);
  border-radius: var(--border-radius-pill);
  width: 44px;
  height: 44px;
  display: none;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: var(--transition-base);
  box-shadow: var(--shadow-sm);
  flex-shrink: 0;
}
.carousel-control:hover {
  background-color: var(--color-primary);
  color: var(--color-text-inverted);
}
.benefit-card {
  flex: 0 0 220px;
  text-align: center;
  padding: var(--sp-lg);
}
.benefit-icon {
  width: 56px;
  height: 56px;
  margin-bottom: var(--sp-md);
}
.benefit-text {
  font-size: var(--fs-base);
  color: var(--color-text-secondary);
}

/* Timeline Section */
.timeline {
  position: relative;
  max-width: 800px;
  margin: 0 auto;
}
@media (min-width: 769px) {
  .timeline::before {
    content: '';
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    top: 0;
    bottom: 0;
    width: 3px;
    background-color: var(--color-primary-light);
  }
}
.timeline-step {
  display: flex;
  position: relative;
  margin-bottom: var(--sp-xl);
  width: 100%;
  align-items: flex-start;
}
.timeline-marker-container {
  display: flex;
  z-index: 1;
  align-items: center;
}
.timeline-marker {
  width: 40px;
  height: 40px;
  background-color: var(--color-primary);
  color: var(--color-text-inverted);
  border-radius: var(--border-radius-pill);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: var(--fw-bold);
  border: 3px solid var(--color-bg-body);
  flex-shrink: 0;
}
.timeline-content {
  flex-grow: 1;
}
.timeline-step-title {
  font-size: var(--fs-h5);
  font-weight: var(--fw-semibold);
  margin-bottom: var(--sp-xs);
}

/* Pricing Section */
.pricing-section {
  background-color: var(--color-bg-component);
}
.pricing-grid {
  display: grid;
  gap: var(--sp-lg);
}
.pricing-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: var(--sp-xl);
}
.pricing-icon {
  font-size: 2.5rem;
  margin-bottom: var(--sp-md);
  color: var(--color-primary);
}
.pricing-card-title {
  font-size: var(--fs-h4);
  margin-bottom: var(--sp-sm);
}
.pricing-note {
  margin-top: var(--sp-xl);
  font-style: italic;
  text-align: center;
  color: var(--color-text-muted);
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}

/* FAQ Section */
.faq-list {
  max-width: 800px;
  margin: 0 auto;
  display: grid;
  gap: var(--sp-sm);
}
.faq-item {
  border: var(--border-width) solid var(--color-border);
  border-radius: var(--border-radius);
  background-color: var(--color-bg-component);
}
.faq-question {
  width: 100%;
  background: none;
  border: none;
  padding: var(--sp-md) var(--sp-lg);
  font-weight: var(--fw-medium);
  font-size: var(--fs-base);
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  text-align: left;
}
.faq-icon {
  font-size: var(--fs-large);
  transition: transform var(--transition-fast);
}
.faq-question[aria-expanded="true"] .faq-icon {
  transform: rotate(45deg);
}
.faq-answer {
  padding: 0 var(--sp-lg) var(--sp-md);
  color: var(--color-text-secondary);
}

/* Footer CTA */
.footer-cta {
  padding: var(--sp-xxl) 1.5rem;
}
.cta-title {
  font-size: var(--fs-h2);
}
.cta-subtitle {
  font-size: var(--fs-large);
  color: var(--color-text-secondary);
  max-width: 600px;
  margin: var(--sp-md) auto var(--sp-lg);
}

/* =================================== */
/* === AJUSTES DE RESPONSIVIDADE === */
/* =================================== */
@media (min-width: 769px) {
  .carousel-control { display: flex; }
  .timeline-step { width: 50%; }
  .timeline-step:not(.timeline-step-even) { padding-right: var(--sp-xl); justify-content: flex-end; }
  .timeline-step-even { align-self: flex-end; padding-left: var(--sp-xl); }
  .timeline-marker-container { position: absolute; top: 0; left: 100%; transform: translateX(-50%); }
  .timeline-step-even .timeline-marker-container { left: auto; right: 100%; transform: translateX(50%); }
  .timeline-content { text-align: right; }
  .timeline-step-even .timeline-content { text-align: left; }
  .pricing-grid { grid-template-columns: repeat(3, 1fr); }
}

@media (max-width: 768px) {
  .section { padding: 3rem 1rem; }
  
  /* CORREÇÃO APLICADA: Tipografia responsiva */
  .title { font-size: calc(var(--fs-h5)); }
  .hero-title { font-size: calc(var(--fs-h1) * 0.85); line-height: 1.3; }
  .hero-subtitle { font-size: var(--fs-base); }
  .section-title-global { font-size: calc(var(--fs-h2) * 0.9); }

  /* Timeline em coluna única */
  .timeline::before { display: none; }
  .timeline-step, .timeline-step-even {
    width: 100%;
    margin-left: 0; padding: 0;
    flex-direction: row;
  }
  .timeline-marker-container {
    position: static; transform: none;
    margin-right: var(--sp-md);
    padding-top: var(--sp-xs); /* Alinhamento vertical do marcador */
  }
  .timeline-content {
    text-align: left;
    padding: var(--sp-md);
  }

  .pricing-grid { grid-template-columns: 1fr; }

  .cta-title { font-size: calc(var(--fs-h2) * 0.9); }
  .footer-cta-button { width: 90%; max-width: 320px; }
}
</style>