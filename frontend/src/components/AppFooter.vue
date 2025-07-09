<template>
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-column footer-about">
          <h4 class="footer-heading">AnimalTracking</h4>
          <p class="footer-about-text">
            Uma plataforma completa para a rastreabilidade do seu rebanho, garantindo segurança e transparência com tecnologia blockchain.
          </p>
        </div>

        <div class="footer-column">
          <h4 class="footer-heading">Navegação</h4>
          <ul class="footer-links">
            <li><a href="#benefits" class="footer-link">Benefícios</a></li>
            <li><a href="#details" class="footer-link">Como Funciona</a></li>
            <li><a href="#plans" class="footer-link">Cobrança</a></li>
            <li><a href="#faq" class="footer-link">FAQ</a></li>
          </ul>
        </div>

        <div class="footer-column">
          <h4 class="footer-heading">Conta</h4>
          <ul class="footer-links">
            <li><router-link to="/login" class="footer-link">Login</router-link></li>
            <li><router-link to="/register" class="footer-link">Cadastre-se</router-link></li>
            <li><router-link to="/search-blockchain" class="footer-link">Auditoria Pública</router-link></li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <p>&copy; {{ new Date().getFullYear() }} AnimalTracking. Todos os direitos reservados.</p>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'AppFooter'
};
</script>

<style scoped>
/* --- Estrutura Principal do Footer --- */
.site-footer {
  /* Usando cores do seu design system */
  background-color: var(--color-primary); /* Fundo escuro */
  color: var(--color-white); /* Texto com cor suave */
  padding: 5rem 0 2rem;
  font-size: 0.95rem;
  /* Efeito diagonal no topo. Ajuste o valor de '10%' se quiser mais ou menos inclinação. */
  clip-path: polygon(0 10%, 100% 0, 100% 100%, 0 100%);
}

.footer-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 3rem;
  padding-bottom: 3rem;
}

/* --- Estilos das Colunas --- */
.footer-column h4 {
  font-size: var(--fs-base);
  font-weight: var(--fw-semibold);
  color: var(--color-white);
  margin-bottom: 1.5rem;
  position: relative;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.footer-column h4::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -8px;
  width: 35px;
  height: 2px;
  background-color: var(--color-white); /* Usando a sua cor primária como destaque */
}

.footer-about-text {
  line-height: 1.7;
  color: var(--color-white);
}

.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-links li {
  margin-bottom: 0.8rem;
}

.footer-links a {
  color: var(--color-white);
  text-decoration: none;
  transition: color 0.3s ease, padding-left 0.3s ease;
}

.footer-links a:hover {
  color: var(--color-white);
  padding-left: 5px; /* Efeito de deslocamento no hover */
}


/* --- Secção Inferior (Copyright) --- */
.footer-bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.1); /* Linha divisória sutil */
  padding-top: 2rem;
  text-align: center;
  font-size: var(--fs-smaller);
  color: var(--color-white);
}

.footer-bottom p {
  margin: 0;
}

/* --- Responsividade --- */
@media (max-width: 768px) {
    .site-footer {
        /* Remove ou suaviza o efeito diagonal em telas pequenas para evitar cortes estranhos */
        clip-path: polygon(0 5%, 100% 0, 100% 100%, 0 100%);
        padding-top: 4rem;
    }
    .footer-grid {
        text-align: center; /* Centraliza o texto no mobile */
    }
    .footer-column h4::after {
        left: 50%;
        transform: translateX(-50%); /* Centraliza a linha de destaque */
    }
    .footer-about-text {
        padding-right: 0;
    }
}
</style>