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

ARQUIVO_ENTRADA   = r"C:\Users\Usuário\Desktop\Miniprojeto_Varejo\Base_Varejo.csv"
ARQUIVO_SAIDA     = r"C:\Users\Usuário\Desktop\Miniprojeto_Varejo\df_limpo.csv"
SEPARADOR         = ";"
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
# ==========================================================================
# ETAPA 2 - VERIFICAÇÃO DE PROBLEMAS (qualidade dos dados)
# ==========================================================================
#Reporta nulos (NaN), registros duplicados duplicados e inconsistências
def diagnosticar_problemas(df: pd.DataFrame) -> None:
    linha("Etapa 2 - Qualidade de Dados")

    #Valores nulos por coluna
    print("Valores nulos(NaN) por coluna")
    print(df.isnull().sum())

    #A carga de arquivos CSV tenho como delimitador o (;) gera "colulas fantasmas"
    #mais conhecidas como "Unnamed"
    colunas_fantasmas = [c for c in df.columns if c.startwith("Unnamed")]
    if colunas_fantasmas:
        print(f"Colunas nulas ou 'fantasmas' geradas pelo delimitador (;): {colunas_fantasmas}")

    #Duplicatas
    duplicadas_completas = df.duplicated().sum()
    print(f"\nRegistros duplicados: {duplicadas_completas}")

    #Duplicata referente ao negócio, ou seja, o mesmo produto aparecendo mais de uma vez na mesma compra
    #Isso pode indicar erro de digitação ou leitura de código de barras e não uma outra unidade vendida
    dup_item_na_compra = df.duplicated(subset=['CO_ID', 'PR_ID']).sum()
    print(f"Linha com o mesmo registro de PR_ID repetido na mesma compra" f"(CO_ID): {dup_item_na_compra}")

    #Inconsistências 
    #Categoria de produtos ausentes - "#N/D"
    qtd_cat_ausente = (df["PR_CAT"] == CATEGORIA_AUSENTE).sum()
    pct_cat_ausente = qtd_cat_ausente/len(df) * 100
    print(f"\nCategoria de produtos ausentes " 
          f"('{CATEGORIA_AUSENTE}'): {qtd_cat_ausente}" 
          f"({pct_cat_ausente:.2f}% da base)")

#Datas inválidas
datas_convertidas = pd.to_datetime(df["DATA"], format="%d/%m/%Y", errors="coerce")
qtd_datas_invalidas = datas_convertidas.isna().sum()
print(f"Registros com datas inválidas: " f"{qtd_datas_invalidas}")

#Verifica a unicidade de registros das colunas CL_GENERO e CL_SEG
print(f"\nRegistros únicos na coluna CL_GENERO: {sorted(df['CL_GENERO'].unique())}")
print(f"\nRegistros únicos na coluna CL_SEG: {sorted(df['CL_SEG'].unique())}")

# ==========================================================================
# ETAPA 3 - LIMPEZA MÍNIMA DOS DADOS
# ==========================================================================
#Tratamento de nulos, duplicatas relevantesl, tipos de dados e inconsistências tipo "#N/D"
linha("Etapa 3 - Limpeza dos dados")
df = df.copy()
registros_iniciais = len(df)

#Tratamento de dados nulos
#As colunas "Unnamed: *" não trazem informação nenhuma
colunas_fantasmas = [c for c in df.columns if c.startswith("Unnamed")]
if colunas_fantasmas:
    df = df.drop(columns=colunas_fantasmas)
    print(f"Colunas 100% nulas(NaN) removidas: {colunas_fantasmas}")

#Trocando o registro "#N/D" por não informado
qtd_antes = (df["PR_CAT"] == CATEGORIA_AUSENTE).sum()
df["PR_CAT"] = df["PR_CAT"].replace(CATEGORIA_AUSENTE, "NÃO INFORMADO")
print(f"Categoria '{CATEGORIA_AUSENTE}' imputada como 'NÃO INFORMADO'" f"em {qtd_antes} registros.")
