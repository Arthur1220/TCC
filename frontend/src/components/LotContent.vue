<template>
  <section class="content-panel">
    <h2>Lotes</h2>
    <p>Organize e controle seus lotes de forma eficiente.</p>
    <div class="content-placeholder">
      Listagem de lotes filtrando por "{{ filterOption }}" e buscando "{{ searchQuery }}".
    </div>
  </section>
</template>

<script>
export default {
  name: 'LotContent',
  props: {
    searchQuery: String,
    filterOption: String
  }
}
</script>

<style scoped>
.content-panel {
  background: var(--color-white);
  padding: var(--sp-lg);
  border-radius: var(--sp-sm);
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.content-placeholder {
  margin-top: var(--sp-md);
  color: var(--color-dark-gray);
}
</style>
