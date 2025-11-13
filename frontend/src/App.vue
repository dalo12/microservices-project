<template>
  <div id="app">
    <header class="app-header">
      <h1 @click="$router.push('/')" class="logo">FlossFlix</h1>
      <nav>
        <router-link to="/">Home</router-link>
      </nav>
    </header>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Arial', sans-serif;
  background-color: var(--color-background);
  color: var(--color-text);
  line-height: 1.6;
}

.app-header {
  background: linear-gradient(135deg, var(--color-brackground) 0%, var(--color-brackground-light) 100%);
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid var(--color-primary);
}

.logo {
  color: var(--color-primary);
  font-size: 2rem;
  font-weight: bold;
  cursor: pointer;
}

.app-header nav a {
  color: var(--color-text);
  text-decoration: none;
  font-size: 1.1rem;
  transition: color 0.3s;
}

.app-header nav a:hover {
  color: var(--color-secondary);
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}
</style>