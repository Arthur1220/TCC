<template>
  <footer class="footer" role="contentinfo">
    <div class="footer-container container">
      <div class="footer-section footer-about">
        <h3 class="logo-footer">AnimalTracking</h3>
        <p class="footer-description">
          Rastreabilidade completa e segura para o seu rebanho, utilizando tecnologia blockchain para garantir transparência e confiança.
        </p>
      </div>

      <div class="footer-section">
        <h4 class="footer-heading">Navegação</h4>
        <ul class="footer-list">
          <li><a href="#benefits" class="footer-link">Benefícios</a></li>
          <li><a href="#details" class="footer-link">Como Funciona</a></li>
          <li><a href="#plans" class="footer-link">Cobrança</a></li>
          <li><a href="#faq" class="footer-link">FAQ</a></li>
        </ul>
      </div>

      <div class="footer-section">
        <h4 class="footer-heading">Conta</h4>
        <ul class="footer-list">
          <li><router-link to="/login" class="footer-link">Login</router-link></li>
          <li><router-link to="/register" class="footer-link">Cadastre-se</router-link></li>
          <li><router-link to="/search-blockchain" class="footer-link">Auditoria Pública</router-link></li>
        </ul>
      </div>

      <div class="footer-section">
        <h4 class="footer-heading">Legal</h4>
        <ul class="footer-list">
          <li><router-link to="/terms" class="footer-link">Termos de Uso</router-link></li>
          <li><router-link to="/privacy" class="footer-link">Política de Privacidade</router-link></li>
        </ul>
      </div>
    </div>

    <div class="footer-bottom">
      <p>&copy; {{ currentYear }} AnimalTracking. Todos os direitos reservados.</p>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'AppFooter',
  computed: {
    currentYear() {
      return new Date().getFullYear();
    }
  }
};
</script>

<style scoped>
.footer {
  background-color: var(--color-bg-muted);
  color: var(--color-text-secondary);
  font-size: var(--fs-small);
  padding-top: var(--sp-xxl); /* Mais espaço no topo */
  border-top: var(--border-width) solid var(--color-border-light);
}

.footer-container {
  display: grid;
  gap: var(--sp-xl); /* Espaço entre as colunas */
  padding-bottom: var(--sp-xxl);
}

/* Layout Desktop com 4 colunas */
@media (min-width: 768px) {
  .footer-container {
    grid-template-columns: 2fr 1fr 1fr 1fr; /* Coluna da logo maior */
  }
}

.footer-section {
  min-width: 0; /* Ajuda no alinhamento do grid */
}

.logo-footer {
  font-family: var(--font-heading);
  font-size: var(--fs-h4);
  font-weight: var(--fw-bold);
  color: var(--color-primary);
  margin-bottom: var(--sp-sm);
}

.footer-description {
  color: var(--color-text-muted);
  line-height: var(--lh-base);
  padding-right: var(--sp-lg); /* Espaço para não encostar na próxima coluna */
}

.footer-heading {
  font-family: var(--font-body); /* Fonte mais moderna para os títulos */
  font-size: var(--fs-base);
  font-weight: var(--fw-semibold);
  color: var(--color-text-primary);
  margin-bottom: var(--sp-md);
  text-transform: uppercase; /* Deixa os títulos em maiúsculas */
  letter-spacing: 0.5px;
}

.footer-list {
  list-style: none;
}

.footer-list li {
  margin-bottom: var(--sp-xs);
}

.footer-link {
  color: var(--color-text-secondary); /* Cor mais suave para os links */
  text-decoration: none;
  transition: color var(--transition-fast);
}

.footer-link:hover,
.footer-link:focus {
  color: var(--color-primary);
  text-decoration: underline;
}

.footer-bottom {
  text-align: center;
  padding: var(--sp-md);
  background-color: var(--color-bg-body);
  border-top: var(--border-width) solid var(--color-border-light);
  font-size: var(--fs-smaller);
  color: var(--color-text-muted);
}

.footer-bottom p {
  margin: 0;
}

/* Responsividade para Telas Menores */
@media (max-width: 767px) {
  .footer-container {
    grid-template-columns: 1fr; /* Força uma única coluna */
    text-align: center; /* Centraliza todo o texto */
  }

  .footer-description {
    padding-right: 0; /* Remove o padding extra no mobile */
  }
  
  .footer-heading {
    margin-top: var(--sp-lg); /* Adiciona espaço entre as seções no mobile */
  }
}
</style>