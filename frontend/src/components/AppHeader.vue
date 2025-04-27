// ------------------------------
// File: src/components/AppHeader.vue
// ------------------------------
<template>
  <header class="header" role="banner">
    <div class="header-container">
      <h1 class="logo" tabindex="0" @click="goHome" @keydown.enter="goHome">AnimalTracking</h1>
      <nav class="nav" role="navigation" aria-label="Main navigation">
        <ul class="nav-list">
          <li v-for="link in navLinks" :key="link.id">
            <a
              :href="link.href"
              :class="{ active: activeSection === link.id }"
              @click.prevent="scrollToSection(link.id)"
            >
              {{ link.label }}
            </a>
          </li>
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
  data() {
    return {
      navLinks: [
        { id: 'benefits', label: 'Benefícios', href: '#benefits' },
        { id: 'details', label: 'Como Funciona', href: '#details' },
        { id: 'plans', label: 'Cobrança', href: '#plans' },
        { id: 'faq', label: 'FAQ', href: '#faq' }
      ],
      activeSection: ''
    };
  },
  methods: {
    goHome() { this.$router.push('/'); },
    scrollToSection(id) {
      document.getElementById(id).scrollIntoView({ behavior: 'smooth' });
    },
    onIntersection(entries) {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          this.activeSection = entry.target.id;
        }
      });
    }
  },
  mounted() {
    const sections = this.navLinks.map(l => document.getElementById(l.id));
    const observer = new IntersectionObserver(this.onIntersection, { threshold: 0.3 });
    sections.forEach(sec => sec && observer.observe(sec));
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
  z-index: 1000;
}
.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--sp-lg) var(--sp-md);
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
.nav-list a.active {
  color: var(--color-accent);
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
    padding: var(--sp-md);
  }
  .nav-list {
    flex-direction: column;
    gap: var(--sp-sm);
    margin-top: var(--sp-sm);
  }
}
</style>