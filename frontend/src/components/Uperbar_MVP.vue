<template>
  <aside class="uperbar">
    <nav>
      <ul>
        <li
          v-for="(item, index) in items"
          :key="index"
          @click="$emit('selectItem', item)"
          :class="{ selected: item.label === selectedItem }"
          >
          {{ item.label }}
        </li>
      </ul>
    </nav>
  </aside>
</template>
  
<script>
export default {
  name: "Uperbar",
  props: {
    items: {
      type: Array,
      default: () => []
    },
    selectedItem: {
      type: String,
      default: ""
    }
  }
};
</script>
  
<style scoped>
.uperbar {
  height: 5rem;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
}

.uperbar nav {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
}

.uperbar nav ul {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0;
  list-style: none;
}

.uperbar nav ul li {
  margin: 0 1rem;
  margin: 0 1rem;
  padding: 0.75rem;
  cursor: pointer;
  transition: color 0.3s ease;
}

.uperbar nav ul li:hover {
  text-decoration: overline;
  font-weight: bold;
}
  
.uperbar ul {
  list-style: none;
}
  
.uperbar li {
  padding: 0.75rem;
  cursor: pointer;
}

.uperbar li.selected {
  font-weight: bold;
  text-decoration: underline;
}
</style>