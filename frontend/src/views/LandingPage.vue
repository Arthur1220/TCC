<template>
  <div>
    <AppHeader />
    <main role="main">
      <section class="hero section text-center">
        <div class="hero-background"></div>
        <div class="container hero-container">
          <h1 class="hero-title">Rastreabilidade Completa para o Seu Rebanho</h1>
          <p class="hero-subtitle">Transparência, segurança e auditabilidade em blockchain de segunda camada.</p>
          <div class="hero-actions">
            <button class="button button-primary button-lg" @click="goToSignup">Comece a Usar Gratuitamente</button>
          </div>
        </div>
      </section>

      <section id="benefits" class="section benefits-section">
        <div class="container">
          <div class="section-header">
            <h2 class="section-title">Benefícios da Rastreabilidade Inteligente</h2>
            <p class="section-subtitle">Descubra como a nossa plataforma pode agregar valor e segurança à sua produção.</p>
          </div>
          <div class="benefits-grid">
            <div class="benefit-card card" v-for="item in benefits" :key="item.text">
              <div class="benefit-icon-wrapper">
                <img :src="item.icon" :alt="`Ícone ${item.text}`" class="benefit-icon" />
              </div>
              <h3 class="benefit-title">{{ item.text }}</h3>
            </div>
          </div>
        </div>
      </section>

      <section id="details" class="section how-it-works-section">
        <div class="container">
          <div class="section-header">
            <h2 class="section-title">Como a Nossa Plataforma Funciona</h2>
            <p class="section-subtitle">Um processo simples e transparente, do campo à auditoria final.</p>
          </div>
          <div class="timeline">
            <div class="timeline-step" v-for="(step, index) in steps" :key="step.title">
              <div class="timeline-marker"></div>
              <div class="timeline-content card">
                <div class="timeline-header">
                  <img :src="step.icon" :alt="`Ícone ${step.title}`" class="timeline-icon" />
                  <h3 class="timeline-step-title">{{ step.title }}</h3>
                </div>
                <p>{{ step.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="plans" class="section pricing-section">
        <div class="container">
           <div class="section-header">
            <h2 class="section-title">Cobrança Simplificada e Transparente</h2>
            <p class="section-subtitle">Sem custos ocultos. Pague apenas pelo que usa com total clareza.</p>
          </div>
          <div class="pricing-grid">
            <div class="card pricing-card" v-for="(plan, idx) in pricing" :key="idx">
              <div class="pricing-icon" v-html="plan.icon"></div>
              <h3 class="pricing-card-title">{{ plan.title }}</h3>
              <p class="pricing-description">{{ plan.description }}</p>
            </div>
          </div>
        </div>
      </section>

      <section id="faq" class="section faq-section">
        <div class="container">
          <div class="section-header">
            <h2 class="section-title">Perguntas Frequentes</h2>
            <p class="section-subtitle">Tudo o que precisa de saber para começar com confiança.</p>
          </div>
          <div class="faq-list">
            <div class="faq-item" v-for="(faq, idx) in faqs" :key="idx">
              <button class="faq-question" @click="toggleFaq(idx)" :aria-expanded="faq.open.toString()">
                <span>{{ faq.question }}</span>
                <span class="faq-icon" :class="{ 'is-open': faq.open }"></span>
              </button>
              <div v-show="faq.open" class="faq-answer">
                <p>{{ faq.answer }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="footer-cta section text-center">
        <div class="container">
          <h2 class="cta-title">Pronto para transformar a sua rastreabilidade?</h2>
          <p class="cta-subtitle">Junte-se à nova era do agronegócio digital. A sua produção merece esta segurança.</p>
          <button class="button button-primary button-lg" @click="goToSignup">Cadastre-se Gratuitamente</button>
        </div>
      </section>
    </main>
    <AppFooter />
  </div>
</template>

<script>
// O seu script permanece o mesmo
import AppHeader from '../components/AppHeader.vue';
import AppFooter from '../components/AppFooter.vue';

export default {
  name: 'LandingPage',
  components: { AppHeader, AppFooter },
  data() {
    return {
      benefits: [
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/lock.png', text: 'Imutabilidade de Registos' },
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/refund-2.png', text: 'Redução de Custos' },
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/flow-chart.png', text: 'Integração Facilitada' },
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/rocket.png', text: 'Alta Performance' },
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/shield.png', text: 'Segurança e Conformidade' },
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/visible.png', text: 'Transparência Total' },
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/graph-report.png', text: 'Auditoria Confiável' }
      ],
      steps: [
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/add-user-group-man-man.png', title: '1. Cadastro Rápido', description: 'Crie a sua conta em minutos e conecte-se à nossa plataforma segura.' },
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/document.png', title: '2. Registo de Eventos', description: 'Insira eventos críticos como nascimento, vacinação e movimentações de forma intuitiva.' },
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/checked-checkbox.png', title: '3. Validação em Blockchain', description: 'Smart contracts verificam e registam a integridade dos seus dados numa blockchain L2 eficiente.' },
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/data-arrived.png', title: '4. Sincronização Segura', description: 'Os seus dados off-chain são mantidos em sincronia com os hashes on-chain, garantindo segurança e acesso rápido.' },
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/combo-chart.png', title: '5. Consulta e Auditoria', description: 'Aceda ao seu dashboard para relatórios detalhados, insights e trilhas de auditoria completas.' }
      ],
      pricing: [
        { icon: '📄', title: 'Faturação Única', description: 'Receba uma única fatura mensal que consolida todas as operações, simplificando a sua gestão financeira.' },
        { icon: '📈', title: 'Relatórios de Uso', description: 'Aceda a relatórios transparentes com resumo de transações, taxas aplicadas e consumo total para auditoria.' },
        { icon: '🔗', title: 'Exportação Flexível', description: 'Exporte dados em CSV, PDF ou integre diretamente via API, facilitando a contabilidade e a análise.' }
      ],
      faqs: [
        { question: 'Como é garantida a segurança dos meus dados?', answer: 'Utilizamos criptografia de ponta e hashes em blockchain para garantir imutabilidade, rastreabilidade e resistência a fraudes.', open: false },
        { question: 'Preciso de entender de blockchain para usar?', answer: 'Não. A nossa plataforma foi desenhada para abstrair toda a complexidade. Você usa uma interface web amigável, e nós cuidamos da tecnologia.', open: false },
        { question: 'Consigo exportar relatórios para auditoria?', answer: 'Sim. Gere relatórios personalizáveis com filtros avançados e exporte facilmente nos formatos CSV ou PDF.', open: false },
        { question: 'A plataforma é adequada para pequenos produtores?', answer: 'Sim! A nossa solução é escalável e pensada para atender desde pequenos produtores até grandes cooperativas, com planos flexíveis.', open: false }
      ],
      showArrows: false, // O carrossel foi removido, então não é mais necessário
    };
  },
  methods: {
    goToSignup() { this.$router.push('/login'); },
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
/* ============================
   DESIGN SYSTEM V2 - LANDING PAGE
   ============================ */

/* --- Utilidades e Padrões de Secção --- */
.section {
  padding: 6rem 1.5rem;
  position: relative;
  overflow: hidden;
}
.section-header {
  text-align: center;
  margin-bottom: var(--sp-xxl);
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}
.section-title {
  font-family: var(--font-heading);
  font-size: var(--fs-h2);
  font-weight: var(--fw-bold);
  color: var(--color-text-primary);
  margin-bottom: var(--sp-sm);
}
.section-subtitle {
  font-size: var(--fs-large);
  color: var(--color-text-secondary);
  line-height: 1.6;
}

/* --- Hero Section --- */
.hero {
  padding: 8rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 80vh;
  position: relative;
}
.hero-background {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  z-index: -1;
}
.hero-container { z-index: 1; }
.hero-title {
  font-size: var(--fs-h1);
  font-weight: var(--fw-black);
  line-height: 1.1;
  margin-bottom: var(--sp-md);
  text-shadow: 0 2px 10px rgba(0,0,0,0.2);
}
.hero-subtitle {
  font-size: var(--fs-large);
  margin-bottom: var(--sp-xl);
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}
.hero-actions .button {
  transform: scale(1.1);
  box-shadow: var(--shadow-lg);
}

/* --- Benefits Section --- */
.benefits-section { background-color: var(--color-bg-body); }
.benefits-grid {
  display: grid;
  gap: var(--sp-lg);
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
}
.benefit-card {
  text-align: center;
  padding: var(--sp-xl);
  background: var(--color-bg-component);
  border: none;
  transition: var(--transition);
}
.benefit-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-lg);
}
.benefit-icon-wrapper {
  display: inline-flex;
  padding: var(--sp-md);
  background-color: var(--color-primary-light);
  border-radius: 50%;
  margin-bottom: var(--sp-lg);
}
.benefit-icon {
  width: 40px;
  height: 40px;
}
.benefit-title {
  font-size: var(--fs-h4);
  font-weight: var(--fw-bold);
  color: var(--color-text-primary);
}

/* --- How It Works (Timeline) --- */
.timeline {
  position: relative;
  max-width: 700px;
  margin: 0 auto;
}
.timeline::before {
  content: '';
  position: absolute;
  left: 24px; /* Alinhado com o centro do marcador */
  top: 0;
  bottom: 0;
  width: 2px;
  background-color: var(--color-border);
}
.timeline-step {
  position: relative;
  padding-left: 70px; /* Espaço para o marcador */
  margin-bottom: var(--sp-xxl);
}
.timeline-marker {
  position: absolute;
  left: 0;
  top: 0;
  width: 50px;
  height: 50px;
  background-color: var(--color-white);
  border: 2px solid var(--color-primary);
  color: var(--color-primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: var(--fw-bold);
  font-size: 1.25rem;
}
.timeline-content {
  background: transparent;
  border: none;
  box-shadow: none;
  padding: 0;
}
.timeline-header {
  display: flex;
  align-items: center;
  gap: var(--sp-md);
  margin-bottom: var(--sp-sm);
}
.timeline-icon { width: 32px; height: 32px; }
.timeline-step-title { font-size: var(--fs-h4); }
.timeline-content p { color: var(--color-text-secondary); max-width: none; }


/* --- Pricing Section --- */
.pricing-grid {
  display: grid;
  gap: var(--sp-lg);
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
}
.pricing-card {
  text-align: center;
  padding: var(--sp-xl);
  border: 2px solid var(--color-border);
}
.pricing-icon { font-size: 3rem; margin-bottom: var(--sp-md); }
.pricing-card-title { font-size: var(--fs-h4); }
.pricing-description { color: var(--color-text-secondary); }

/* --- FAQ Section --- */
.faq-list {
  max-width: 750px;
  margin: 0 auto;
  display: grid;
  gap: var(--sp-sm);
}
.faq-item {
  border-bottom: var(--border-width) solid var(--color-border);
}
.faq-question {
  width: 100%;
  background: none;
  border: none;
  padding: var(--sp-md) 0;
  font-weight: var(--fw-semibold);
  font-size: var(--fs-large);
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  text-align: left;
}
.faq-icon {
  width: 1.5em; height: 1.5em;
  transition: transform var(--transition);
  position: relative;
}
.faq-icon::before, .faq-icon::after {
  content: '';
  position: absolute;
  top: 50%; left: 50%;
  width: 14px; height: 2px;
  background-color: currentColor;
  transform: translate(-50%, -50%);
  transition: transform 0.2s ease;
}
.faq-icon::after { transform: translate(-50%, -50%) rotate(90deg); }
.faq-question[aria-expanded="true"] .faq-icon::after { transform: translate(-50%, -50%) rotate(0deg); }
.faq-answer {
  padding-bottom: var(--sp-lg);
  color: var(--color-text-secondary);
}

/* --- Footer CTA --- */
.cta-title { font-size: var(--fs-h2); }
.cta-subtitle {
  font-size: var(--fs-large);
  max-width: 600px;
  margin: var(--sp-md) auto var(--sp-lg);
}

/* --- Responsividade --- */
@media (max-width: 768px) {
  .section { padding: 4rem 1rem; }
  .section-header { margin-bottom: var(--sp-xl); }
  .timeline::before { left: 24px; }
  .timeline-step { padding-left: 60px; }
  .timeline-marker { width: 48px; height: 48px; left: 0; }
}
</style>