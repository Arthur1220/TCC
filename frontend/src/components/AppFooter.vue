// ------------------------------
// File: src/components/AppFooter.vue
// ------------------------------
<template>
  <footer class="footer" role="contentinfo">
    <div class="footer-container container"> <div class="footer-section">
        <h4 class="footer-heading">Visão Geral</h4>
        <ul class="footer-list">
          <li><a href="#benefits" class="footer-link">Benefícios</a></li>
          <li><a href="#details" class="footer-link">Como Funciona</a></li>
          <li><a href="#plans" class="footer-link">Preços</a></li>
          <li><a href="#faq" class="footer-link">FAQ</a></li>
        </ul>
      </div>
      <div class="footer-section">
        <h4 class="footer-heading">Conta</h4>
        <ul class="footer-list">
          <li><router-link to="/login" class="footer-link">Login</router-link></li>
          <li><router-link to="/signup" class="footer-link">Cadastro</router-link></li>
          <li><router-link to="/support" class="footer-link">Suporte</router-link></li>
        </ul>
      </div>
      <div class="footer-section">
        <h4 class="footer-heading">Legal</h4>
        <ul class="footer-list">
          <li><router-link to="/terms" class="footer-link">Termos de Uso</router-link></li>
          <li><router-link to="/privacy" class="footer-link">Privacidade</router-link></li>
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
  background-color: var(--color-bg-muted); /* Fundo sutil */
  color: var(--color-text-secondary); /* Texto secundário */
  font-size: var(--fs-small);
  padding-top: var(--sp-lg); /* Espaçamento no topo do footer */
  border-top: var(--border-width) solid var(--color-border-light);
}

.footer-container {
  /* A classe .container global já define max-width e padding lateral */
  display: flex;
  flex-wrap: wrap;
  gap: var(--sp-xl); /* Espaço maior entre seções */
  padding-bottom: var(--sp-lg); /* Espaçamento abaixo das seções */
  justify-content: space-between; /* Padrão, pode ser center ou start */
}

.footer-section {
  flex: 1; /* Permite que as seções cresçam */
  min-width: 180px; /* Largura mínima para cada seção antes de quebrar */
}

.footer-heading { /* Renomeado de h4 para classe específica */
  font-family: var(--font-heading);
  font-size: var(--fs-base); /* Tamanho base para os títulos do rodapé */
  font-weight: var(--fw-semibold); /* Um pouco mais de peso */
  color: var(--color-text-primary); /* Texto primário para os títulos */
  margin-bottom: var(--sp-md); /* Mais espaço abaixo do título */
}

.footer-list {
  list-style: none; /* Removido padding-left, já que é globalmente resetado */
}

.footer-list li {
  margin-bottom: var(--sp-xs); /* Espaçamento entre itens da lista */
}

.footer-link { /* Renomeado de a para classe específica */
  font-family: var(--font-body);
  color: var(--color-text-link); /* Usar cor de link padrão */
  font-size: var(--fs-small);
  text-decoration: none; /* Removido, já é padrão de 'a' */
}
.footer-link:hover, .footer-link:focus {
  color: var(--color-primary-dark); /* Escurece no hover */
  text-decoration: underline; /* Adiciona sublinhado no hover */
}

.footer-bottom {
  text-align: center;
  padding: var(--sp-md); /* Padding aumentado */
  background-color: var(--color-bg-body); /* Cor de fundo ligeiramente diferente ou a mesma do corpo */
  border-top: var(--border-width) solid var(--color-border-light);
  font-size: var(--fs-smaller); /* Fonte ainda menor para o copyright */
  color: var(--color-text-muted);
}
.footer-bottom p {
    margin-bottom: 0; /* Remove margem do parágrafo no rodapé */
}

@media (max-width: 768px) {
  .footer-container {
    flex-direction: column;
    text-align: center; /* Centraliza texto das seções no mobile */
    gap: var(--sp-lg); /* Mantém um bom espaçamento */
  }
  .footer-section {
    min-width: auto; /* Permite que ocupem 100% da largura */
  }
}
</style>