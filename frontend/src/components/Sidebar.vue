<template>
    <aside class="sidebar">
      <nav>
        <ul>
          <li
            v-for="(item, index) in items"
            :key="index"
            @click="$emit('selectItem', item)"
          >
            {{ item.label }}
          </li>
        </ul>
      </nav>
    </aside>
  </template>
  
  <script>
  export default {
    name: "Sidebar",
    props: {
      items: {
        type: Array,
        default: () => []
      }
    }
  };
  </script>
  
  <style scoped>
  .sidebar {
    width: 200px;
    background-color: var(--color-white);
    border-right: 1px solid var(--color-light-gray);
  }
  
  .sidebar ul {
    list-style: none;
    padding: 0.5rem;
  }
  
  .sidebar li {
    padding: 0.75rem;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .sidebar li:hover {
    background-color: var(--color-light-gray);
  }
  </style>
  