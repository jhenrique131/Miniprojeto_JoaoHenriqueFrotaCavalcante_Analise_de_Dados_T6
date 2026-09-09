"""
==========================================================================
 MINI-PROJETO AVALIATIVO - MÓDULO 1
 Análise Exploratória de Dados (AED) - Base Varejo
 Turma: Analise_de_Dados_T6
 Aluno: João Henrique Frota Cavalcante
==========================================================================

OBJETIVO
--------
Realizar uma Análise Exploratória de Dados (AED) sobre a base "Varejo",
que contém registros reais de compras (um item por linha). O script:

  1) Carrega os dados e descreve sua estrutura;
  2) Identifica problemas de qualidade (nulos, duplicatas, inconsistências);
  3) Realiza a limpeza mínima necessária (nulos, duplicatas, tipos);
  4) Valida e explora a lógica de agrupamento por compra (CO_ID);
  5) Calcula estatísticas descritivas da coluna de número de filhos
     do cliente (CL_FHL);
  6) Explora padrões via groupby()/pivot_table();
  7) Imprime um relatório final com as principais conclusões.

COMO EXECUTAR
--------------
  - VSCode  : abra este arquivo e rode "python Miniprojeto_Varejo_AED.py"
              (o arquivo Base_Varejo.csv deve estar na mesma pasta).
  - Colab   : faça upload do Base_Varejo.csv para o ambiente e rode
              todas as células (ou execute o arquivo .py diretamente).

DICIONÁRIO DE DADOS (colunas relevantes)
-----------------------------------------
  DATA        -> data da compra (dd/mm/aaaa)
  CO_ID       -> identificador da COMPRA (se repete para os itens da
                 mesma compra; NÃO é um identificador de linha único)
  CL_ID       -> identificador do cliente
  CL_GENERO   -> gênero do cliente (M/F)
  CL_EC       -> estado civil do cliente (código)
  CL_FHL      -> número de filhos do cliente
  CL_SEG      -> segmento do cliente (A/B/C)
  PR_ID       -> identificador do produto
  PR_CAT      -> categoria do produto (contém "#N/D" quando ausente)
  PR_NOME     -> nome do produto
==========================================================================
"""
#Importação das bibliotecas
import pandas as pd
import numpy as np

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 20)

ARQUIVO_ENTRADA = "Base_Varejo.csv"
ARQUIVO_SAIDA = "df_limpo.csv"
SEPARADOR = ";"
CATEGORIA_AUSENTE = "#N/D"


#Imprime um separador visual no relatório do terminal
def linha(titulo=""):
    print("\n" + "=" * 78)
    if titulo:
        print(titulo)
        print("=" * 78)


# ==========================================================================
# ETAPA 1 - CARGA DOS DADOS
# ==========================================================================
#Carrega o arquivo CSV e exibe uma visão geral dos dados
def carregar_dados(caminho: str) -> pd.DataFrame:
    df = pd.read_csv(caminho, sep=SEPARADOR)

    linha("Etapa 1 - Carga e Visão geral dos dados")
    print(f"Arquivo carregado: {caminho}")
    print(f"Quantidade de linhas: {df.shape[0]}")
    print(f"Quantidade de colunas: {df.shape[1]}")
    print("\nTipo de Dados:")
    print(df.dtypes)
    print("\nRegistros de origem:")
    print(df.head())

    return df
