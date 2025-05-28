<template>
  <div>
    <AppHeader />
    <main role="main">
      <section class="hero section text-center">
        <div class="container">
          <h1 class="title">AnimalTracking</h1>
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
                <div class="timeline-line"></div>
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
              <div class="pricing-icon" v-html="plan.icon"></div> <h3 class="pricing-card-title">{{ plan.title }}</h3>
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
// Apenas certifique-se de que os caminhos dos ícones em `data` estão corretos.
import AppHeader from '../components/AppHeader.vue';
import AppFooter from '../components/AppFooter.vue';

export default {
  name: 'LandingPage',
  components: { AppHeader, AppFooter },
  data() {
    return {
      benefits: [
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/lock.png', text: 'Imutabilidade de Registros' },
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/refund-2.png', text: 'Redução de Custos Operacionais' },
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/flow-chart.png', text: 'Integração Facilitada via API' },
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/rocket.png', text: 'Performance Otimizada em L2' },
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/shield.png', text: 'Segurança e Conformidade' },
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/visible.png', text: 'Transparência Total do Processo' },
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/graph-report.png', text: 'Auditoria Simplificada e Confiável' }
      ],
      steps: [
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/add-user-group-man-man.png', title: '1. Cadastro Rápido', description: 'Crie sua conta em minutos e conecte-se à nossa plataforma segura.' },
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/document.png', title: '2. Registro de Eventos', description: 'Insira eventos críticos como nascimento, vacinação, e movimentações de forma intuitiva.' },
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/checked-checkbox.png', title: '3. Validação em Blockchain', description: 'Smart contracts verificam e registram a integridade dos seus dados em uma blockchain L2 eficiente.' },
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/data-arrived.png', title: '4. Sincronização Segura', description: 'Seus dados off-chain são mantidos em sincronia com os hashes on-chain, garantindo segurança e acesso rápido.' },
        { icon: 'https://img.icons8.com/ios-glyphs/48/1A73E8/combo-chart.png', title: '5. Consulta e Auditoria', description: 'Acesse seu dashboard para relatórios detalhados, insights e trilhas de auditoria completas.' }
      ],
      pricing: [ // Ícones podem ser SVGs ou classes de ícones de uma biblioteca
        { icon: '📄', title: 'Faturamento Único Consolidado', description: 'Receba uma única fatura mensal que consolida todas as operações realizadas, simplificando sua gestão financeira.' },
        { icon: '📈', title: 'Relatórios Detalhados de Uso', description: 'Acesse relatórios transparentes com resumo de transações, taxas aplicadas e consumo total, permitindo controle e auditoria.' },
        { icon: '🔗', title: 'Exportação e Integração Flexível', description: 'Exporte dados em CSV, PDF ou integre diretamente via API, facilitando a contabilidade e a análise de dados.' }
      ],
      faqs: [
        { question: 'Como a segurança dos meus dados é garantida?', answer: 'Utilizamos criptografia de ponta (AES-256) para dados em repouso e em trânsito. Os registros chave são ancorados em blockchain com hashes criptográficos, garantindo imutabilidade, rastreabilidade e resistência a fraudes.', open: false },
        { question: 'Preciso ter conhecimento técnico sobre blockchain para usar a plataforma?', answer: 'Absolutamente não. Nossa plataforma foi desenhada para abstrair toda a complexidade técnica. Você interage com uma interface web amigável, e nós cuidamos de toda a interação com a blockchain em segundo plano.', open: false },
        { question: 'Consigo exportar relatórios para minha contabilidade ou auditoria?', answer: 'Sim. Você pode gerar relatórios customizáveis com filtros avançados por data, tipo de evento, animal ou lote, e exportá-los facilmente nos formatos CSV ou PDF para integração com seus sistemas.', open: false },
        { question: 'Como funciona o suporte técnico caso eu precise de ajuda?', answer: 'Oferecemos suporte técnico especializado através de múltiplos canais, incluindo chat ao vivo, e-mail e telefone. Nosso SLA de primeira resposta é de até 2 horas para incidentes críticos.', open: false },
        { question: 'A plataforma é adequada para pequenos produtores?', answer: 'Sim! Nossa solução é escalável e pensada para atender desde pequenos produtores individuais até grandes cooperativas e empresas, com planos flexíveis que se adaptam à sua necessidade.', open: false }
      ],
      showArrows: true // Inicialmente true, checkArrows pode ajustar depois
    };
  },
  mounted() {
    this.$nextTick(() => { // Garante que o DOM está pronto para refs
        this.checkArrows();
    });
    window.addEventListener('resize', this.checkArrowsDebounced);
  },
  beforeUnmount() { // Corrigido de beforeDestroy para Vue 3
    window.removeEventListener('resize', this.checkArrowsDebounced);
  },
  methods: {
    goToSignup() { this.$router.push('/login'); }, // Ou '/signup' se tiver uma rota específica
    scrollCarousel(direction) {
      const carousel = this.$refs.carousel;
      if (!carousel) return;
      const scrollAmount = carousel.offsetWidth * 0.8; // Scroll 80% da largura visível
      carousel.scrollBy({
        left: direction === 'left' ? -scrollAmount : scrollAmount,
        behavior: 'smooth'
      });
    },
    scrollLeft() { this.scrollCarousel('left'); },
    scrollRight() { this.scrollCarousel('right'); },
    checkArrows() {
      const c = this.$refs.carousel;
      if (c) {
        // Mostrar setas se o conteúdo total for maior que a área visível
        this.showArrows = c.scrollWidth > c.clientWidth + 1; // +1 para evitar problemas de arredondamento
      } else {
        this.showArrows = false;
      }
    },
    // Debounce para a função checkArrows para não disparar excessivamente no resize
    checkArrowsDebounced() {
        if (this.resizeTimeout) clearTimeout(this.resizeTimeout);
        this.resizeTimeout = setTimeout(this.checkArrows, 150);
    },
    toggleFaq(index) {
      this.faqs = this.faqs.map((faq, i) => ({
        ...faq,
        open: i === index ? !faq.open : false // Fecha outros ao abrir um
      }));
    }
  }
};
</script>

<style scoped>
/* Estilos específicos da LandingPage, usando variáveis globais */

/* Utilidade de Seção Padrão */
.section {
  padding-top: var(--sp-xxl);
  padding-bottom: var(--sp-xxl);
}
.section:nth-child(even) { /* Alternar cor de fundo para algumas seções */
  background-color: var(--color-bg-muted);
}
.text-center {
  text-align: center;
}

/* Título de Seção Global (se não tiver no style.css) */
.section-title-global {
  font-family: var(--font-heading);
  font-size: var(--fs-h2);
  color: var(--color-text-primary);
  text-align: center;
  margin-bottom: var(--sp-xl); /* Mais espaço após o título da seção */
}
.section-title-global::after { /* Pequeno sublinhado decorativo */
    content: '';
    display: block;
    width: 60px;
    height: 3px;
    background-color: var(--color-primary);
    margin: var(--sp-sm) auto 0;
}

/* Titulo Principal */
.title{
  font-size: var(--fs-h1-2); /* Usa variável global */
  font-weight: var(--fw-bold);
  color: var(--color-primary);
  text-align: center;
  margin-bottom: var(--sp-lg);
}

/* Hero Section */
.hero {
  background-color: var(--color-bg-body); /* Cor de fundo do corpo, ou um gradiente suave */
  /* Exemplo de gradiente: background-image: linear-gradient(120deg, var(--color-primary-light) 0%, var(--color-bg-component) 100%); */
  color: var(--color-text-primary); /* Ajuste se o fundo for escuro */
  padding-top: calc(var(--sp-xxl) * 1.5); /* Mais padding no topo */
  padding-bottom: calc(var(--sp-xxl) * 1.5);
}
.hero-title {
  font-size: var(--fs-h1); /* Usa variável global */
  font-weight: var(--fw-bold);
  color: var(--color-text-primary); /* Cor mais escura para contraste */
  margin-bottom: var(--sp-md);
  line-height: 1.2;
}
.hero-subtitle {
  font-size: var(--fs-large); /* Usa variável global */
  color: var(--color-text-secondary);
  margin-bottom: var(--sp-lg);
  max-width: 700px; /* Limita largura do subtítulo */
  margin-left: auto;
  margin-right: auto;
}
.hero .button { /* Botão de destaque */
    font-size: var(--fs-large);
    padding: var(--sp-md) var(--sp-xl);
}

/* Benefits Carousel Section */
.benefits-section {
    background-color: var(--color-bg-component); /* Fundo branco para esta seção */
}
.benefits-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--sp-sm); /* Espaço entre botões e carrossel */
}
.benefits-carousel {
  display: flex;
  overflow-x: auto;
  scroll-behavior: smooth;
  gap: var(--sp-lg); /* Espaço entre os cards de benefício */
  padding: var(--sp-md) 0; /* Padding vertical para o carrossel */
  flex-grow: 1;
  scrollbar-width: none; /* Firefox */
}
.benefits-carousel::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}
.carousel-control {
  background-color: var(--color-bg-component);
  border: var(--border-width) solid var(--color-border);
  color: var(--color-primary);
  border-radius: var(--border-radius-pill);
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: var(--transition-base);
  box-shadow: var(--shadow-sm);
  flex-shrink: 0;
}
.carousel-control:hover, .carousel-control:focus {
  background-color: var(--color-primary);
  color: var(--color-text-inverted);
  border-color: var(--color-primary);
  box-shadow: var(--shadow);
  transform: scale(1.05);
}
.benefit-card {
  /* A classe .card global já aplica muitos estilos */
  flex: 0 0 220px; /* Largura fixa para cada card de benefício */
  text-align: center;
  padding: var(--sp-lg); /* Mais padding interno */
}
.benefit-icon {
  width: 56px; /* Tamanho do ícone aumentado */
  height: 56px;
  margin-bottom: var(--sp-md);
  /* object-fit: contain; */ /* Para garantir que o ícone não distorça */
}
.benefit-text {
    font-size: var(--fs-base);
    color: var(--color-text-secondary);
    line-height: 1.5;
    margin-bottom: 0;
}


/* How It Works (Timeline) Section */
/* .how-it-works-section { background-color: var(--color-bg-muted); } */

.timeline {
  position: relative;
  max-width: 800px; /* Limita a largura da timeline */
  margin: 0 auto; /* Centraliza */
  padding-top: var(--sp-md);
}
/* Linha vertical central (apenas para desktop, se desejar) */
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
    border-radius: var(--border-radius-sm);
  }
}

.timeline-step {
  display: flex;
  position: relative; /* Para posicionar o marcador e conteúdo em relação a ele */
  margin-bottom: var(--sp-xl); /* Mais espaço entre os passos */
  width: 100%;
}

/* Estilo para alternar lados na timeline em desktop */
@media (min-width: 769px) {
  .timeline-step {
    width: 50%;
    padding-right: var(--sp-lg); /* Espaço do conteúdo para a linha central */
  }
  .timeline-step-even { /* Para os itens da direita */
    margin-left: 50%;
    padding-left: var(--sp-lg);
    padding-right: 0;
    flex-direction: row-reverse; /* Inverte a ordem do marcador e conteúdo */
  }
  .timeline-step-even .timeline-marker-container {
    flex-direction: row-reverse; /* Mantém o marcador à esquerda da linha no lado direito */
  }
  .timeline-step-even .timeline-content {
    text-align: left; /* Alinha texto à esquerda para itens da direita */
  }
}


.timeline-marker-container {
  display: flex;
  align-items: center;
  flex-shrink: 0;
  z-index: 1; /* Para ficar sobre a linha ::before da timeline */
}

@media (max-width: 768px) {
  .timeline-marker-container {
      margin-right: var(--sp-md); /* Espaço entre marcador e conteúdo no mobile */
  }
}
@media (min-width: 769px) {
  .timeline-marker-container {
    position: absolute;
    top: 0; /* Alinha o topo do marcador com o topo do card de conteúdo */
    left: 50%;
    transform: translateX(-50%); /* Centraliza o marcador na linha */
  }
  .timeline-step-even .timeline-marker-container {
    /* Não precisa de left/transform pois o step já está posicionado */
    /* Apenas precisa ser ajustado para o lado correto se o conteúdo for invertido */
    left: auto;
    right: 50%; /* Ou ajuste conforme necessário */
    transform: translateX(50%);
  }
}

.timeline-marker {
  width: 40px; /* Marcador maior */
  height: 40px;
  background-color: var(--color-primary);
  color: var(--color-text-inverted);
  border-radius: var(--border-radius-pill);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-heading);
  font-weight: var(--fw-bold);
  font-size: var(--fs-base);
  border: 3px solid var(--color-bg-component); /* Borda para destacar da linha de fundo */
  box-shadow: var(--shadow-sm);
}

.timeline-content {
  /* .card global já aplica background, border, padding, etc. */
  padding: var(--sp-lg); /* Padding interno do card */
  flex-grow: 1;
}

.timeline-icon {
  width: 40px; /* Ícones um pouco maiores */
  height: 40px;
  margin-bottom: var(--sp-sm);
  /* object-fit: contain; */
}
.timeline-step-title { /* Renomeado de h4 para classe */
  font-size: var(--fs-h5); /* Usando variável de título */
  color: var(--color-text-primary);
  font-weight: var(--fw-semibold);
  margin-bottom: var(--sp-xs);
}
.timeline-content p {
  margin-bottom: 0;
  color: var(--color-text-secondary);
  font-size: var(--fs-base);
}


/* Pricing Section */
.pricing-section {
    background-color: var(--color-bg-component);
}
.pricing-grid {
  /* .grid .grid-3 globais já devem funcionar. Ajuste gap se necessário. */
  gap: var(--sp-lg); /* Mantido */
}
.pricing-card {
  /* .card global já aplica estilos base */
  display: flex;
  flex-direction: column;
  align-items: center; /* Centraliza conteúdo do card */
  text-align: center;
  padding: var(--sp-xl); /* Padding maior para cards de preço */
}
.pricing-card:hover {
    border-color: var(--color-primary); /* Borda de destaque no hover */
    box-shadow: var(--shadow-lg); /* Sombra mais pronunciada */
}
.pricing-icon {
  font-size: 2.5rem; /* Ícone maior */
  margin-bottom: var(--sp-md);
  color: var(--color-primary); /* Cor de destaque para o ícone */
}
.pricing-card-title { /* Renomeado de h4 para classe */
  font-size: var(--fs-h4);
  color: var(--color-text-primary);
  margin-bottom: var(--sp-sm);
}
.pricing-card p {
    color: var(--color-text-secondary);
    margin-bottom: 0;
}
.pricing-note {
  margin-top: var(--sp-xl); /* Mais espaço acima da nota */
  font-style: italic;
  text-align: center;
  color: var(--color-text-muted);
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}

/* FAQ Section */
.faq-list { /* Renomeado de .faq-grid */
  max-width: 800px; /* Limita largura da lista de FAQ */
  margin: 0 auto; /* Centraliza */
  display: grid;
  gap: var(--sp-sm); /* Espaço menor entre itens do FAQ */
}
.faq-item {
  border: var(--border-width) solid var(--color-border);
  border-radius: var(--border-radius); /* Raio de borda maior */
  overflow: hidden; /* Para o border-radius funcionar com o botão interno */
  background-color: var(--color-bg-component);
}
.faq-question {
  width: 100%;
  background-color: transparent; /* Botão transparente, o fundo vem do .faq-item */
  border: none;
  border-bottom: var(--border-width) solid transparent; /* Borda inferior para quando aberto */
  padding: var(--sp-md) var(--sp-lg);
  font-family: var(--font-body); /* Usar font-body para perguntas */
  font-weight: var(--fw-medium); /* Um pouco mais de peso */
  font-size: var(--fs-base); /* Ou --fs-large */
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  text-align: left;
  color: var(--color-text-primary);
  transition: background-color var(--transition-fast);
}
.faq-question:hover, .faq-question:focus {
  background-color: var(--color-bg-hover);
}
.faq-item[aria-expanded="true"] .faq-question { /* Estilo quando aberto */
   border-bottom-color: var(--color-border-light);
   color: var(--color-primary);
}
.faq-icon {
  font-size: var(--fs-large); /* Usando variável */
  font-weight: var(--fw-light); /* Ícone mais leve */
  transition: transform var(--transition-fast);
}
.faq-item[aria-expanded="true"] .faq-icon {
  transform: rotate(45deg); /* Para '−' se tornar 'x' ou ajustar o ícone */
}
.faq-answer {
  /* background: var(--color-bg); Removido, fundo do .faq-item */
  padding: var(--sp-md) var(--sp-lg);
  /* min-height: 100px; Removido, altura será dinâmica */
  /* Animação de abertura/fechamento pode ser adicionada com Vue <transition> */
}
.faq-answer p {
    color: var(--color-text-secondary);
    margin-bottom: 0;
}

/* Footer CTA Section */
.gradient-bg {
  background: linear-gradient(to bottom, var(--color-bg-component) 0%, var(--color-primary-light) 100%); /* Gradiente começa com a cor da seção anterior */
}
.footer-cta-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--sp-md);
  padding: var(--sp-xxl) var(--sp-md); /* Padding maior */
  color: var(--color-text-primary); /* Ajustar se o fundo for escuro */
}
.cta-title {
  font-size: var(--fs-h2); /* Usando variável */
  color: var(--color-text-primary); /* Ajustar se o fundo for escuro */
  margin-bottom: var(--sp-sm);
}
.cta-subtitle {
  font-size: var(--fs-large);
  color: var(--color-text-secondary); /* Ajustar se o fundo for escuro */
  margin-bottom: var(--sp-lg);
  max-width: 600px;
  text-align: center;
}

/* Ajustes de Responsividade Específicos da LandingPage */
@media (max-width: 768px) {
  .section {
    padding-top: var(--sp-xl);
    padding-bottom: var(--sp-xl);
  }
  .hero {
    padding-top: var(--sp-xl);
    padding-bottom: var(--sp-xl);
  }
  .hero-title {
    font-size: calc(var(--fs-h1) * 0.8);
  }
  .hero-subtitle {
    font-size: calc(var(--fs-large) * 0.9);
  }
  .section-title-global {
    font-size: calc(var(--fs-h2) * 0.9);
    margin-bottom: var(--sp-lg);
  }

  .benefits-carousel {
    gap: var(--sp-md);
  }
  .benefit-card {
    flex-basis: 180px; /* Menor base para cards no mobile */
    padding: var(--sp-md);
  }
  .carousel-control {
    width: 36px;
    height: 36px;
  }
  .carousel-control svg {
      width: 20px;
      height: 20px;
  }


  .timeline::before { /* Esconde a linha central vertical no mobile */
    display: none;
  }
  .timeline-step,
  .timeline-step-even {
    width: 100%; /* Ocupa toda a largura */
    margin-left: 0 !important; /* Remove o estilo inline do marginLeft */
    padding-left: 0; /* Remove padding da "escada" */
    padding-right: 0;
    flex-direction: row; /* Garante marcador à esquerda, conteúdo à direita */
    align-items: flex-start; /* Alinha itens no topo */
  }
  .timeline-marker-container {
    position: static; /* Remove posicionamento absoluto */
    transform: none;
    margin-right: var(--sp-md); /* Espaço entre marcador e conteúdo */
  }
   .timeline-content {
    text-align: left; /* Garante alinhamento à esquerda */
  }


  .pricing-grid {
    /* .grid já fará o stack para 1 coluna se .grid-3 for removido/ignorado ou se não houver CSS Grid no global */
    /* Se .grid-3 for mantido do global, precisamos sobrescrever: */
    grid-template-columns: 1fr;
  }

  .cta-title {
    font-size: calc(var(--fs-h2) * 0.9);
  }
  .cta-subtitle {
    font-size: var(--fs-base);
  }
  .footer-cta-button {
      width: 80%; /* Botão CTA maior no mobile */
      max-width: 300px;
      padding: var(--sp-md);
  }
}
</style>