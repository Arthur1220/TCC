// ------------------------------
// File: src/components/AppHeader.vue
// ------------------------------
<template>
  <header class="header" role="banner">
    <div class="header-container">
      <h1 class="logo" tabindex="0" @click="goHome" @keydown.enter="goHome">AnimalTracking</h1>
      <nav class="nav" role="navigation" aria-label="Main">
        <ul class="nav-list">
          <li><a href="#benefits">Benefícios</a></li>
          <li><a href="#details">Como Funciona</a></li>
          <li><a href="#plans">Preços</a></li>
          <li><a href="#faq">FAQ</a></li>
        </ul>
      </nav>
      <div class="user-icon">
        <a href="/login" aria-label="Login">
          <img src="https://img.icons8.com/ios-glyphs/30/000000/user--v1.png" alt="Login" tabindex="0" />
        </a>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'AppHeader',
  methods: {
    goHome() {
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
.header {
  position: sticky;
  top: 0;
  background: rgba(255,255,255,0.8);
  backdrop-filter: saturate(180%) blur(10px);
  border-bottom: 1px solid var(--color-border);
}
.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--sp-md) var(--sp-md);
  /* maior espaço vertical */
}
.logo {
  font-family: var(--font-heading);
  font-size: 1.75rem;
  color: var(--color-text);
  cursor: pointer;
  transition: color 0.2s, transform 0.2s;
}
.logo:hover,
.logo:focus {
  color: var(--color-accent);
  transform: scale(1.1);
  outline: none;
}
.nav-list {
  list-style: none;
  display: flex;
  gap: var(--sp-lg);
}
.nav-list a {
  font-family: var(--font-body);
  color: var(--color-text);
  text-decoration: none;
  transition: color 0.2s;
}
.nav-list a:hover,
.nav-list a:focus {
  color: var(--color-accent);
  outline: none;
}
.user-icon img {
  width: var(--sp-lg);
  height: var(--sp-lg);
  transition: transform 0.3s;
}
.user-icon img:hover,
.user-icon img:focus {
  transform: rotate(15deg) scale(1.2);
  outline: none;
}
@media (max-width: 768px) {
  .header-container {
    flex-direction: column;
    padding: var(--sp-lg);
  }
  .nav-list {
    flex-direction: column;
    gap: var(--sp-sm);
    margin-top: var(--sp-sm);
  }
}
</style>