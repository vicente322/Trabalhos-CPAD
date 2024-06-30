# Análise da Dengue em Estados Brasileiros

Este trabalho foi desenvolvido por alunos da PUC-RS como Trabalho Final da disciplina Coleta, Preparacão de Análise de Dados

Autores: [Aléxia Dorneles](https://github.com/alexiadorneles), [Arthur Land Avila](https://github.com/ArthurLAvila), [Gustavo Lottermann](https://github.com/gustavo-lottermann), [Matheus Krebs](https://github.com/teteukrebs) e [Vicente Hofmeister](https://github.com/vicente322)


## Coleta de Dados

### Dengue - SINAN

Pysus

### Populacão - IBGE

Para o IBGE, os dados foram encontrados na internet em tabelas separadas e disformes

### Dados Climáticos - INMET


## Preparacão do Dados

### SINAN

Foram removidas colunas que não seriam utilizadas e filtrados os estados para usar somente os definidos pelo grupo (GO, SP, RS e ES).

No Power BI as tabelas foram unificadas em uma.

Os dados foram adaptados para o seu tipo correto. A representacao das UFs foi alterado do numeral de acordo com o IBGE para a sigla da UF. Campos de idade gestacional, raca e escolaridade foram traduzidos para seus reais significados.

### INMET

Para pegar a Umidade e Temperatura média de cada estado, pegamos as estacões de cada estado e fizemos a média de todas medicoes, por dia.

Os valores foram separados por estado e por ano, mas foram unificados em uma unica tabela no Power BI. Por estar com "." em vez de "," para o separador de casas decimais, foi necessário transformar os dados de temperatura e umidade.