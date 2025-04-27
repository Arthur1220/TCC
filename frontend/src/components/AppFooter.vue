// ------------------------------
// File: src/components/AppFooter.vue
// ------------------------------
<template>
  <footer class="footer" role="contentinfo">
    <div class="footer-container">
      <div class="footer-section">
        <h4>Visão Geral</h4>
        <ul>
          <li><a href="#benefits">Benefícios</a></li>
          <li><a href="#details">Como Funciona</a></li>
          <li><a href="#plans">Preços</a></li>
          <li><a href="#faq">FAQ</a></li>
        </ul>
      </div>
      <div class="footer-section">
        <h4>Conta</h4>
        <ul>
          <li><a href="/login">Login</a></li>
          <li><a href="/signup">Cadastro</a></li>
          <li><a href="/support">Suporte</a></li>
        </ul>
      </div>
      <div class="footer-section">
        <h4>Legal</h4>
        <ul>
          <li><a href="/terms">Termos de Uso</a></li>
          <li><a href="/privacy">Privacidade</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">© 2025 AnimalTracking. Todos os direitos reservados.</div>
  </footer>
</template>

<script>
export default { name: 'AppFooter' };
</script>

<style scoped>
.footer {
  background: var(--color-muted);
  color: var(--color-text);
  font-size: var(--fs-small); /* fonte reduzida */
}
.footer-container {
  display: flex;
  flex-wrap: wrap;
  gap: var(--sp-lg);
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--sp-lg) var(--sp-md);
  justify-content: space-between;
}
.footer-section h4 {
  font-family: var(--font-heading);
  font-size: var(--fs-base);
  margin-bottom: var(--sp-sm);
}
.footer-section a {
  font-family: var(--font-body);
  color: var(--color-text);
  font-size: var(--fs-small);
}
.footer-bottom {
  text-align: center;
  padding: var(--sp-sm);
  background: var(--color-border);
}
@media (max-width: 768px) {
  .footer-container {
    flex-direction: column;
    text-align: center;
  }
}
</style>