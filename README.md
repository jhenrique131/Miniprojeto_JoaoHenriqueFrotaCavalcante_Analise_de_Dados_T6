# Mini-Projeto Avaliativo — Análise Exploratória de Dados (AED) — Base Varejo

**Turma:** Analise_de_Dados_T6
**Módulo:** 1 — Introdução à Análise de Dados

## 📋 Sobre o projeto

Este projeto realiza uma **Análise Exploratória de Dados (AED)** sobre uma base de compras de varejo (`Base_Varejo.csv`), em que cada linha representa **um item comprado** (não uma compra inteira). O objetivo é praticar o fluxo real de um analista de BI/Dados: carregar, diagnosticar, limpar, validar regras de negócio, calcular estatísticas descritivas e explorar padrões via agrupamentos, preparando a base para uso em dashboards ou análises mais avançadas.

## 🗂️ Estrutura do repositório

```
├── Miniprojeto_Varejo_AED.py     # Script principal da AED (comentado, executável)
├── Base_Varejo.csv               # Base de dados original (entrada)
├── df_limpo.csv                  # Base tratada, gerada ao final da execução
├── README.md                     # Este arquivo
├── README_NomeDoAluno_Turma.md   # Instruções de execução (padrão exigido)
```

## 🧾 Dicionário de dados

| Coluna      | Descrição                                                            |
|-------------|-----------------------------------------------------------------------|
| `DATA`      | Data da compra (dd/mm/aaaa)                                          |
| `CO_ID`     | Identificador da **compra** — repete-se para cada item da mesma compra |
| `CL_ID`     | Identificador do cliente                                              |
| `CL_GENERO` | Gênero do cliente (M/F)                                               |
| `CL_EC`     | Estado civil do cliente (código)                                      |
| `CL_FHL`    | Número de filhos do cliente                                           |
| `CL_SEG`    | Segmento do cliente (A/B/C)                                           |
| `PR_ID`     | Identificador do produto                                              |
| `PR_CAT`    | Categoria do produto (`"#N/D"` quando ausente)                        |
| `PR_NOME`   | Nome do produto                                                       |

## 🔍 Etapas realizadas pelo script

1. **Carga dos dados** — leitura com `pandas`, exibição de nº de registros, colunas e tipos.
2. **Diagnóstico de qualidade** — nulos por coluna, linhas duplicadas, categoria ausente (`#N/D`) e verificação de datas inválidas.
3. **Limpeza mínima**:
   - Remoção de colunas 100% vazias (artefato do CSV);
   - Imputação de `"#N/D"` → `"NAO INFORMADO"` na categoria do produto (mantém a venda, explicita a ausência de classificação);
   - Remoção de duplicatas de negócio (mesmo produto repetido na mesma compra);
   - Conversão de `DATA` para `datetime` e ajuste de tipos categóricos/numéricos.
4. **Validação da regra `CO_ID`** — confirma que o identificador representa a compra (vários itens por `CO_ID`) e gera um resumo por compra.
5. **Estatística descritiva de `CL_FHL`** (número de filhos do cliente) — média, mediana, desvio padrão, moda, mínimo, máximo, quartis e contagem, calculados sobre clientes únicos.
6. **Agrupamentos** — vendas por gênero, por categoria de produto, tabela dinâmica categoria × segmento, e vendas por mês.
7. **Conclusões** — bloco final com os principais insights e problemas remanescentes da base.

## ▶️ Como executar

Veja o arquivo [`README_JoaoHenriqueFrotaCavalcante_Analise_de_Dados_T6.md`] para instruções passo a passo (VSCode ou Google Colab).

## 💡 Principais insights (resumo)

- A base original tem 830.000 linhas (itens); após remover duplicatas de item por compra, restam ~733 mil linhas válidas.
- 1.000 clientes únicos realizaram ~18.470 compras, com média de ~40 itens por compra.
- `ALIMENTOS` é, disparado, a categoria mais vendida, seguida de `HIGIENE` e `LIMPEZA`.
- A base não possui coluna de valor monetário, o que limita análises de faturamento/ticket médio — uma limitação relevante para evoluções futuras.

## ⚠️ Limitações conhecidas

- Ausência de coluna de preço/valor da venda.
- ~0,4% dos itens seguem sem categoria de produto após a limpeza (agora rotulados como `NAO INFORMADO`).
- Não há verificação de consistência temporal dos dados cadastrais do cliente (gênero, estado civil, filhos) ao longo das compras.
