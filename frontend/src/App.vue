<template>
  <Teleport to="body">
    <transition name="fade">
      <LoadingSpinner 
        v-if="uiState.isLoading" 
        :message="uiState.message"
        :is-error="uiState.isError"
      />
    </transition>
  </Teleport>

  <router-view v-slot="{ Component }">
    <transition name="page" mode="out-in">
      <component :is="Component" />
    </transition>
  </router-view>
</template>

<script>
import LoadingSpinner from '@/components/LoadingSpinner.vue';
import { uiState } from '@/stores/uiStore.js';

export default {
  name: 'App',
  components: {
    LoadingSpinner
  },
  setup() {
    // Expõe o estado da UI para o template
    return { uiState };
  }
}
</script>

<style>
/* ... (Seus estilos globais, incluindo as transições .page e .fade) ... */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>