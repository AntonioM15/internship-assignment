<template>
  <router-view/>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
@import url('css/colors.css');

/* Make sure that html and body fill the whole page */
html, body {
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Inter', sans-serif;
}

*,
*::before,
*::after {
  box-sizing: inherit;
}
</style>
