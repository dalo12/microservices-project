<template>
  <div id="app-container">
    <header>
      <router-link to="/" class="logo">FlossFlix</router-link>
    </header>
    <main>
      <router-view />
    </main>
  </div>
</template>

<style>
/* Global Styles */
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  background: #f4f4f4;
  margin: 0;
}

#app-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

header {
  background: #fff;
  padding: 1.5rem 2rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
  color: #42b883; /* Vue Green */
}

main {
  background: #fff;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
</style>