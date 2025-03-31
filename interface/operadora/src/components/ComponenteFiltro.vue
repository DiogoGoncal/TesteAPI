<template>
  <div class="container">
    <h2>Buscar Operadoras</h2>

    <!-- Campo de pesquisa global -->
    <input
      type="text"
      v-model="filtroGlobal"
      placeholder="Filtrar por qualquer campo"
    />

    <!-- Select para filtrar por Modalidade -->
    <select v-model="modalidadeSelecionada">
      <option value="">Todas as Modalidades</option>
      <option v-for="mod in modalidades" :key="mod" :value="mod">
        {{ mod }}
      </option>
    </select>

    <!-- Exibição dos resultados -->
    <table v-if="dadosFiltrados.length">
      <thead>
        <tr>
          <th v-for="coluna in colunas" :key="coluna">
            {{ coluna }}
            <!-- Setas para ordenação -->
            <span @click="ordenar(coluna)">
              <i :class="ordenacao[coluna] === 'asc' ? 'fas fa-arrow-up' : 'fas fa-arrow-down'"></i>
            </span>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in dadosFiltrados" :key="item.Registro_ANS">
          <td>{{ item.Registro_ANS }}</td>
          <td>{{ item.CNPJ }}</td>
          <td>{{ item.Razao_Social }}</td>
          <td>{{ item.Nome_Fantasia || '-' }}</td>
          <td>{{ item.Modalidade }}</td>
          <td>{{ item.Cidade }}</td>
          <td>{{ item.UF }}</td>
        </tr>
      </tbody>
    </table>

    <p v-else>Nenhum resultado encontrado.</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      filtroGlobal: "", // Filtro global
      modalidadeSelecionada: "", // Modalidade selecionada
      dados: [],
      colunas: [
        "Registro ANS",
        "CNPJ",
        "Razão Social",
        "Nome Fantasia",
        "Modalidade",
        "Cidade",
        "UF"
      ],
      modalidades: [
        "Administradora de Benefícios",
        "Autogestão",
        "Cooperativa Médica",
        "Filantropia",
        "Medicina de Grupo",
        "Seguradora Especializada em Saúde"
      ],
      ordenacao: {
        "Registro ANS": "asc",
        CNPJ: "asc",
        "Razão Social": "asc",
        "Nome Fantasia": "asc",
        Modalidade: "asc",
        Cidade: "asc",
        UF: "asc"
      }
    };
  },
  computed: {
    // Filtra e ordena os dados
    dadosFiltrados() {
      let dadosFiltrados = this.dados.filter((item) => {
        const valores = Object.values(item).map(v => String(v).toLowerCase()).join(" ");
        const filtroGlobalAtende = valores.includes(this.filtroGlobal.toLowerCase());
        const filtroModalidadeAtende =
          !this.modalidadeSelecionada ||
          (item.Modalidade && item.Modalidade.toLowerCase() === this.modalidadeSelecionada.toLowerCase());

        return filtroGlobalAtende && filtroModalidadeAtende;
      });

      // Ordena os dados com base na ordenação atual
      const colunaOrdenada = Object.keys(this.ordenacao).find(coluna => this.ordenacao[coluna] !== null);
      if (colunaOrdenada) {
        dadosFiltrados = dadosFiltrados.sort((a, b) => {
          const valorA = a[colunaOrdenada];
          const valorB = b[colunaOrdenada];

          if (this.ordenacao[colunaOrdenada] === "asc") {
            return valorA > valorB ? 1 : valorA < valorB ? -1 : 0;
          } else {
            return valorA < valorB ? 1 : valorA > valorB ? -1 : 0;
          }
        });
      }

      return dadosFiltrados;
    }
  },
  async created() {
    await this.carregarDados();
  },
  methods: {
    async carregarDados() {
      console.log("Carregando dados...");
      try {
        const resposta = await fetch("http://127.0.0.1:8000/buscar?razao=");
        if (!resposta.ok) throw new Error("Erro ao buscar os dados");

        this.dados = await resposta.json();
        console.log("Dados carregados:", this.dados);
      } catch (erro) {
        console.error("Erro ao buscar dados:", erro);
      }
    },
    // Função para ordenar a tabela
    ordenar(coluna) {
      if (this.ordenacao[coluna] === "asc") {
        this.ordenacao[coluna] = "desc";
      } else {
        this.ordenacao[coluna] = "asc";
      }
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
  text-align: center;
}
input, select {
  display: block;
  width: 100%;
  margin: 10px 0;
  padding: 8px;
}
table {
  width: 100%;
  margin-top: 20px;
  border-collapse: collapse;
}
th, td {
  border: 1px solid #ddd;
  padding: 8px;
}
th {
  background: #f4f4f4;
  cursor: pointer;
}
th i {
  margin-left: 8px;
}
</style>
