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
          <div class="benefits-carousel">
            <button class="carousel-button left" @click="prevBenefit" aria-label="Anterior">‹</button>
            <div class="benefit-card">
              <img :src="currentBenefit.icon" :alt="currentBenefit.text" />
              <p>{{ currentBenefit.text }}</p>
            </div>
            <button class="carousel-button right" @click="nextBenefit" aria-label="Próximo">›</button>
          </div>
        </div>
      </section>

      <!-- Como Funciona -->
      <section id="details" class="section-gap">
        <div class="container">
          <h3>Como Funciona</h3>
          <div class="grid grid-3">
            <div class="card" v-for="step in steps" :key="step.title">
              <img :src="step.icon" :alt="step.title" />
              <h4>{{ step.title }}</h4>
              <p>{{ step.description }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Planos & Preços -->
      <section id="plans" class="section-gap">
        <div class="container">
          <h3>Planos & Preços</h3>
          <p>Operamos via <strong>carteira principal</strong>. Ao final do mês, você recebe um único faturamento referente às operações realizadas. Não é necessário gerenciar sua carteira.</p>
        </div>
      </section>

      <!-- FAQ -->
      <section id="faq" class="section-gap">
        <div class="container">
          <h3>FAQ</h3>
          <details v-for="faq in faqs" :key="faq.question">
            <summary>{{ faq.question }}</summary>
            <p>{{ faq.answer }}</p>
          </details>
        </div>
      </section>

      <!-- Footer CTA -->
      <section class="footer-cta section-gap">
        <div class="container">
          <h3 class="cta-title">Pronto para transformar sua rastreabilidade?</h3>
          <button class="button" @click="goToSignup">Cadastre-se / Login</button>
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
      currentIndex: 0,
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
      faqs: [
        { question: 'Como garantem a segurança dos dados?', answer: 'Utilizamos criptografia avançada e contratos auditados.' },
        { question: 'Preciso conhecer blockchain?', answer: 'Não. Nossa solução abstrai toda complexidade.' },
        { question: 'Posso exportar relatórios?', answer: 'Sim, em CSV ou PDF.' },
        { question: 'Como acesso o suporte?', answer: 'Via chat e e-mail com SLA de 24h.' }
      ]
    };
  },
  computed: {
    currentBenefit() {
      return this.benefits[this.currentIndex];
    }
  },
  methods: {
    goToSignup() {
      this.$router.push('/signup');
    },
    prevBenefit() {
      this.currentIndex = (this.currentIndex + this.benefits.length - 1) % this.benefits.length;
    },
    nextBenefit() {
      this.currentIndex = (this.currentIndex + 1) % this.benefits.length;
    }
  }
};
</script>

<style scoped>
.section-gap {
  padding: 6rem 0;
}
.hero {
  background: var(--color-bg);
  text-align: center;
}
.hero-title {
  font-size: 2.5rem;
  margin-bottom: var(--sp-md);
}
.hero-subtitle {
  font-size: var(--fs-large);
  margin-bottom: var(--sp-lg);
}
.footer-cta {
  background: var(--color-muted);
  text-align: center;
}
.cta-title {
  font-size: 2rem;
  margin-bottom: var(--sp-md);
}
.benefits-carousel {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--sp-md);
}
.carousel-button {
  background: none;
  border: none;
  font-size: var(--fs-large);
  color: var(--color-text);
  cursor: pointer;
  transition: color 0.2s;
}
.carousel-button:hover,
.carousel-button:focus {
  color: var(--color-accent);
  outline: none;
}
.benefit-card {
  text-align: center;
  max-width: 240px;
}
.benefit-card img {
  width: 48px;
  height: 48px;
  margin-bottom: var(--sp-sm);
}
@media (max-width: 768px) {
  .grid-3 {
    grid-template-columns: 1fr;
  }
}
</style>