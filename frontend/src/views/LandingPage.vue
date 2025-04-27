// ------------------------------
// File: src/views/LandingPage.vue
// ------------------------------
<template>
  <div>
    <AppHeader />
    <main>
      <!-- Hero -->
      <section class="hero section-gap">
        <div class="container">
          <h2 class="hero-title">Rastreabilidade Completa para Seu Rebanho</h2>
          <p class="hero-subtitle">Transparência, segurança e auditabilidade em blockchain de segunda camada.</p>
          <button class="button" @click="goToSignup">Experimente Grátis</button>
        </div>
      </section>

      <!-- Benefícios Carousel -->
      <section id="benefits" class="section-gap">
        <div class="container">
          <h3>Benefícios</h3>
          <div class="benefits-wrapper">
            <button
              v-if="showArrows"
              class="carousel-button left"
              @click="scrollLeft"
              aria-label="Anterior"
            >
              ‹
            </button>
            <div class="benefits-carousel" ref="carousel">
              <div class="benefit-card" v-for="item in benefits" :key="item.text">
                <img :src="item.icon" :alt="item.text" />
                <p>{{ item.text }}</p>
              </div>
            </div>
            <button
              v-if="showArrows"
              class="carousel-button right"
              @click="scrollRight"
              aria-label="Próximo"
            >
              ›
            </button>
          </div>
        </div>
      </section>

      <!-- Como Funciona (Escada) -->
      <section id="details" class="section-gap">
        <div class="container">
          <h3>Como Funciona</h3>
          <div class="timeline">
            <div
              class="timeline-step"
              v-for="(step, index) in steps"
              :key="step.title"
              :style="{ marginLeft: `${index * 40}px` }"
            >
              <div class="timeline-marker">{{ index + 1 }}</div>
              <div class="timeline-content">
                <img :src="step.icon" :alt="step.title" />
                <h4>{{ step.title }}</h4>
                <p>{{ step.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Cobrança Simplificada -->
      <section id="plans" class="section-gap">
        <div class="container">
          <h3 class="section-title">Cobrança Simplificada</h3>
          <div class="grid grid-3 pricing-grid">
            <div class="card pricing-card" v-for="(plan, idx) in pricing" :key="idx">
              <div class="pricing-icon">{{ plan.icon }}</div>
              <h4>{{ plan.title }}</h4>
              <p>{{ plan.description }}</p>
            </div>
          </div>
          <p class="pricing-note">
            Tudo isso sem precisar gerenciar carteiras próprias ou lidar com custos ocultos. É só usar e pagar de forma clara.
          </p>
        </div>
      </section>

      <!-- FAQ - Accordion Cards -->
      <section id="faq" class="section-gap">
        <div class="container">
          <h3 class="section-title">Perguntas Frequentes</h3>
          <div class="faq-grid">
            <div class="faq-item" v-for="(faq, idx) in faqs" :key="idx">
              <button class="faq-question" @click="toggleFaq(idx)" :aria-expanded="faq.open">
                <span>{{ faq.question }}</span>
                <span class="faq-icon">{{ faq.open ? '−' : '+' }}</span>
              </button>
              <div v-if="faq.open" class="faq-answer">
                <p>{{ faq.answer }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Footer CTA -->
      <section class="footer-cta section-gap gradient-bg">
        <div class="container footer-cta-container">
          <h3 class="cta-title">Pronto para transformar sua rastreabilidade?</h3>
          <p class="cta-subtitle">Comece hoje e veja a diferença na segurança e eficiência da sua produção.</p>
          <button class="button footer-cta-button" @click="goToSignup">Cadastre-se / Login</button>
        </div>
      </section>
    </main>
    <AppFooter />
  </div>
</template>

<script>
import AppHeader from '../components/AppHeader.vue';
import AppFooter from '../components/AppFooter.vue';

export default {
  name: 'LandingPage',
  components: { AppHeader, AppFooter },
  data() {
    return {
      benefits: [
        { icon: 'https://img.icons8.com/ios/48/000000/lock--v1.png', text: 'Imutabilidade de registros' },
        { icon: 'https://img.icons8.com/ios/48/000000/money.png', text: 'Redução de custos' },
        { icon: 'https://img.icons8.com/ios/48/000000/settings--v1.png', text: 'Integração via API' },
        { icon: 'https://img.icons8.com/ios/48/000000/speed.png', text: 'Performance otimizada' },
        { icon: 'https://img.icons8.com/ios/48/000000/security-checked.png', text: 'Segurança reforçada' }
      ],
      steps: [
        { icon: 'https://img.icons8.com/ios/48/000000/add-user-male.png', title: 'Cadastro', description: 'Crie sua conta e conecte-se à carteira principal.' },
        { icon: 'https://img.icons8.com/ios/48/000000/edit--v1.png', title: 'Registro', description: 'Insira eventos críticos (nascimento, vacinação etc.).' },
        { icon: 'https://img.icons8.com/ios/48/000000/checkmark--v1.png', title: 'Validação', description: 'Smart contracts conferem integridade automaticamente.' },
        { icon: 'https://img.icons8.com/ios/48/000000/database.png', title: 'Armazenamento', description: 'Dados off-chain e hashes on-chain sincronizados.' },
        { icon: 'https://img.icons8.com/ios/48/000000/combo-chart.png', title: 'Consulta', description: 'Acesse seu dashboard para relatórios e auditorias.' }
      ],
      pricing: [
        { icon: '💼', title: 'Faturamento Único', description: 'Receba uma única fatura mensal que consolida todas as operações realizadas, evitando múltiplos pagamentos e simplificando a gestão financeira.' },
        { icon: '📊', title: 'Relatório Detalhado', description: 'Acesse relatórios transparentes com resumo de transações, taxas aplicadas e consumo, permitindo total controle e auditoria.' },
        { icon: '📥', title: 'Exportação Flexível', description: 'Exporte em CSV, PDF ou integre via API. Facilita a contabilidade e a análise de dados conforme sua necessidade.' }
      ],
      faqs: [
        { question: 'Como garantem a segurança dos dados?', answer: 'Todos os dados são criptografados usando protocolos padrão de mercado (AES-256) e armazenados de forma imutável na blockchain, garantindo rastreabilidade e resistência a fraudes.', open: false },
        { question: 'Preciso conhecer blockchain?', answer: 'Não. Nossa plataforma abstrai toda a complexidade técnica: você utiliza a interface web e nós cuidamos da assinatura e envio das transações em segundo plano.', open: false },
        { question: 'Posso exportar relatórios?', answer: 'Sim, gere relatórios customizados com filtros por data e tipo de evento, e exporte em CSV ou PDF para integrar ao seu sistema de contabilidade.', open: false },
        { question: 'Como funciona o suporte?', answer: 'Oferecemos atendimento 24/7 via chat, e-mail e telefone, com SLA de resposta de até 2 horas para incidentes críticos.', open: false }
      ],
      showArrows: false
    };
  },
  mounted() {
    this.checkArrows();
    window.addEventListener('resize', this.checkArrows);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.checkArrows);
  },
  methods: {
    goToSignup() { this.$router.push('/login'); },
    scrollLeft() { this.$refs.carousel.scrollBy({ left: -this.$refs.carousel.offsetWidth, behavior: 'smooth' }); },
    scrollRight() { this.$refs.carousel.scrollBy({ left: this.$refs.carousel.offsetWidth, behavior: 'smooth' }); },
    checkArrows() { const c = this.$refs.carousel; this.showArrows = c.scrollWidth > c.clientWidth; },
    toggleFaq(i) { this.faqs[i].open = !this.faqs[i].open; }
  }
};
</script>

<style scoped>
.section-gap { padding: 6rem 0; }
.hero { background: var(--color-bg); text-align: center; }
.hero-title { font-size: 2.5rem; margin-bottom: var(--sp-md); }
.hero-subtitle { font-size: var(--fs-large); margin-bottom: var(--sp-lg); }

.section-title { font-size: 2rem; margin-bottom: var(--sp-lg); text-align: center; }

.pricing-grid { gap: var(--sp-lg); }
.pricing-card { display: flex; flex-direction: column; align-items: center; text-align: center; padding: var(--sp-md); border: 1px solid var(--color-border); border-radius: var(--sp-sm); transition: box-shadow 0.2s, transform 0.2s; }
.pricing-card:hover, .pricing-card:focus-within { box-shadow: 0 4px 16px rgba(0,0,0,0.1); transform: translateY(-4px); }
.pricing-icon { font-size: 2rem; margin-bottom: var(--sp-md); }
.pricing-note { margin-top: var(--sp-lg); font-style: italic; text-align: center; color: var(--color-text); }

.timeline { position: relative; margin-left: var(--sp-md); padding-left: var(--sp-lg); }
.timeline:before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 2px; background: var(--color-border); }
.timeline-step { display: flex; align-items: flex-start; margin-bottom: var(--sp-lg); }
.timeline-marker { width: 30px; height: 30px; background: var(--color-accent); color: var(--color-bg); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: var(--font-heading); margin-right: var(--sp-md); }
.timeline-content img { width: 32px; height: 32px; margin-bottom: var(--sp-sm); }
.timeline-content h4 { margin-bottom: var(--sp-sm); }
.timeline-content p { margin: 0; }

.benefits-wrapper { position: relative; display: flex; align-items: center; }
.benefits-carousel { display: flex; overflow-x: auto; scroll-behavior: smooth; gap: var(--sp-md); padding: var(--sp-sm) 0; }
.benefits-carousel::-webkit-scrollbar { display: none; }
.carousel-button { background: none; border: none; font-size: var(--fs-large); color: var(--color-text); cursor: pointer; padding: var(--sp-sm); transition: color 0.2s; z-index: 1; }
.carousel-button.left { margin-right: -var(--sp-lg); }
.carousel-button.right { margin-left: -var(--sp-lg); }
.carousel-button:hover, .carousel-button:focus { color: var(--color-accent); outline: none; }
.benefit-card { flex: 0 0 auto; text-align: center; min-width: 200px; }
.benefit-card img { width: 48px; height: 48px; margin-bottom: var(--sp-sm); }

/* FAQ Styles */
.faq-grid { display: grid; gap: var(--sp-md); }
.faq-item { border: 1px solid var(--color-border); border-radius: var(--sp-sm); overflow: hidden; }
.faq-question { width: 100%; background: var(--color-muted); border: none; padding: var(--sp-md); font-family: var(--font-heading); font-size: var(--fs-base); display: flex; justify-content: space-between; align-items: center; cursor: pointer; }
.faq-icon { font-size: var(--fs-large); }
.faq-answer { background: var(--color-bg); display: flex; align-items: center; padding: var(--sp-md); min-height: 100px; }

/* Footer CTA Styles */
.gradient-bg {
  /* Degrade vertical da cor de fundo da página (branco) para o fundo do footer (cinza) */
  background: linear-gradient(to bottom, var(--color-bg) 0%, var(--color-muted) 100%);
}
.footer-cta-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--sp-md);
  padding: var(--sp-xl) 0;
  color: var(--color-text);
}
.cta-title {
  font-size: 2.25rem;
  margin-bottom: var(--sp-sm);
}
.cta-subtitle {
  font-size: var(--fs-large);
  margin-bottom: var(--sp-md);
  max-width: 600px;
  text-align: center;
}
.footer-cta-button {
  width: 30%;
  background-color: var(--color-bg);
  color: var(--color-accent);
  border: 2px solid var(--color-accent);
  padding: var(--sp-md);
  border-radius: var(--sp-sm);
  transition: background-color 0.3s, color 0.3s;
}
.footer-cta-button:hover, .footer-cta-button:focus {
  background-color: var(--color-accent);
  color: var(--color-bg);
  outline: none;
}
@media (max-width: 768px) {
  .benefits-carousel { padding: var(--sp-md) 0; }
  .grid-3, .pricing-grid { grid-template-columns: 1fr; }
}
</style>