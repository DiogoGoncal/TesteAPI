<template>
  <div>
    <h1>Consulta de Operadoras</h1>
    <BuscarOperadoras />
  </div>
</template>

<script>
import BuscarOperadoras from "./components/ComponenteFiltro.vue";

export default {
  components: {
    BuscarOperadoras
  }
};
</script>

<style>
h1 {
  text-align: center;
  margin-bottom: 20px;
}
</style>
