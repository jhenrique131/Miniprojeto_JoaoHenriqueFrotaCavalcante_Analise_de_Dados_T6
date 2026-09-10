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
print(f"\nPassou pela ETAPA - 1")
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
    colunas_fantasmas = [c for c in df.columns if c.startswith("Unnamed")]
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
print(f"\nPassou pela ETAPA - 2")
# ==========================================================================
# ETAPA 3 - LIMPEZA MÍNIMA DOS DADOS
# ==========================================================================
#Tratamento de nulos, duplicatas relevantesl, tipos de dados e inconsistências tipo "#N/D"
def limpar_dados(df: pd.DataFrame) -> pd.DataFrame:
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

    #Remoção de duplicatas
    antes = len(df)
    df = df.drop_duplicated(subset=["CO_ID", "PR_ID"], keep="first")
    removidas = antes - len(df)
    print(f"Duplicatas (mesmo PR_ID na mesma compra CO_ID) removidas: " f"{removidas}")

    #Ajustes de tipo de dados
    df["DATA"] = pd.to_datetime(df["DATA"], format="%d/%m/%Y", errors="coerce")

    #Colunas Categóricas: tipo category
    for col in ["CO_ID", "CL_ID", "CL_EC", "CL_FHL", "PR_ID"]:
        df[col] = df[col].astype("int64")
    print("\nTipos de dados após a limpeza")
    print(df.dtypes)

    registros_finais = len(df)
    print(f"\nRegistros antes de limpeza: {registros_iniciais}")
    print(f"\nRegistros após a limpeza: {registros_finais}")
    print(f"\nTotal de linhas removidas: " f"{registros_iniciais - registros_finais}")

    return df
print(f"\nPassou pela ETAPA - 3")

# ==========================================================================
# ETAPA 4 - VALIDAÇÃO DA REGRA CO_ID (item x compra)
# ==========================================================================
#Confirmação da compra e construção do resumo por compra
def validar_regra_co_id(df: pd.DataFrame) -> pd.DataFrame:
    linha("Etapa 4 - Validação do identificador de comrpa, campo CO_ID")
    total_linhas = len(df)
    total_compras = df["CO_ID"].nunique()
    print(f"Total de itens comprados: {total_linhas}")
    print(f"Total de compras únicas - Sem repetição/distintas: {total_compras}")
    print(f"Média de itens por compras: {total_linhas-total_compras:.2f}")

    #Resumo por compra, cliente e data da compra
    resumo_compras = df.groupby("CO_ID").agg(
        cliente=("CL_ID", "first"),
        data_compra = ("DATA", "first"),
        qtd_itens = ("PR_ID", "count"),
        qtd_categorias_distintas = ("PR_CAT", "nunique"),
    ).reset_index()

    print("\nDistribuição de itens por compra:")
    print(resumo_compras["qtd_itens"].describe())
    print("\nPrimeiras 5 compras resumidas")
    print(resumo_compras.head())

    return resumo_compras

# ==========================================================================
# ETAPA 5 - ESTATÍSTICA DESCRITIVA (número de filhos do cliente)
# ==========================================================================
#Cálculo sobre a coluna CL_FHL que é referente a quantidade de filhos dos clientes.
#Tudo é calculado sobre a base de Clientes Únicos para que o resultado não pese a favor
#de quem comprou mais itens

def estatisticas_filho(df: pd.DataFrame) -> None:
    linha("Etapa 5 - Quantidade de filhos do cliente - Estatística Descritiva")
    clientes_unicos = df.drop_duplicates(subset="CL_ID")
    filhos = clientes_unicos["CL_FHL"]
    print(f"Base que está sendo considerada:{len(clientes_unicos)} clientes únicos" 
          f"Evita contar o memso cliente várias vezes por item comprado")
    print(f"\nContagem: {filhos.count()}")
    print(f"Média: {filhos.mean()}")
    print(f"Mediana: {filhos.median()}")
    print(f"Desvio Padrão: {filhos.std()}")
    print(f"Moda: {filhos.mode().tolist()}")
    print(f"Minimo: {filhos.min()}")
    print(f"Máximo: {filhos.max()}")
    print(f"1º Quartil - 25%: {filhos.quantile(0.25)}")
    print(f"2º Quartil - 50%: {filhos.quantile(0.50)}")
    print(f"3º Quartil - 75%: {filhos.quantile(0.75)}")
    print(f"\nResumo:")
    print(filhos.describe())
    print(f"\nDistribuição de Frequência - Número de filhos, quantidade de clientes: ")
    print(filhos.value_counts().sort_index())
# ==========================================================================
# ETAPA 6 - PADRÕES DE AGRUPAMENTO
# ==========================================================================
#Exploração de agrupamentos relevantes para o negócio
def explorar_agrupamento(df: pd.DataFrame) -> None:
    linha("Etapa 6 - Padrões de Agrupamento")

    #Itens vendidos e clientes distintos por gênero - Agrupamento 1
    print("[Agrupamento 1] Itens vendidos e clientes distintos por gênero:")
    por_genero = df.groupby("CL_GENERO", observed=True).agg(
        qtd_itens_vendidos = ("PR_ID", "count"),
        clientes_distintos = ("CL_ID", "nunique"),
        compras_distintas = ("CO_ID", "nunique")
    )
    print(por_genero)

    #Itens vendidos por categoria de produtos - Agrupamento 2
    print("\n[Agrupamento 2] Itens vendidos por categoria de produto" "(top categorias):")
    por_categoria = (df.groupby("PR_CAT", observed=True)
                     .size().sort_values(ascending=False).rename("qtd_itens_vendidos")
                     )
    print(por_categoria)

    #Pivot_table de gênero versus categoria - Agrupamento 3
    print("\n[Agrupamento 3] Tabela Dinâmica de quantidade de itens por categoria versus seguimento do cliente")
    tabela_dinamica = pd.pivot_table(df,index="PR_CAT",columns="CL_SEG", 
                                     values="PR_ID", aggfunc="count", fill_value=0, observed=True)
    print(tabela_dinamica)

    #Vendas ao longo do tempo por mês - Agrupamento 4
    print("\n[Agrupamento 4] Venadas os longo do tempo por mês")
    vendas_por_mes = (df.assign(ANO_MES=df["DATA"].dt.to_period("M")
                                .groupby("ANO_MES", observed=True).size())
                                )
    print(vendas_por_mes)
# ==========================================================================
# ETAPA 7 - CONCLUSÕES E RELATÓRIO FINAL
# ==========================================================================
#Impressão dos resultados obtidos
def gerar_conclusoes(df_bruto: pd.DataFrame, df_limpo: pd.DataFrame) -> None:
    linha("Etapa 7 - Conclusões e Relatórios finais")
    total_bruto = len(df_bruto)
    total_limpo = len(df_limpo)
    total_compras = df_limpo["CO_ID"].nunique()
    total_clientes = df_limpo["CL_ID"].nunique()
    genero_top = df_limpo["CL_GENERO"].value_counts().idxmax()
    categoria_top = df_limpo["PR_CAT"].value_counts().idxmax()
    media_itens_compra = total_limpo/total_compras
    conclusoes = [
        f"A base original possuía {total_bruto} linhas (itens comprados); "
        f"após a limpeza (remoção de duplicatas de item por compra e de "
        f"colunas 100% vazias), restaram {total_limpo} linhas válidas.",

        f"A base representa {total_clientes} clientes únicos realizando "
        f"{total_compras} compras distintas, com uma média de "
        f"{media_itens_compra:.1f} itens por compra (CO_ID).",

        f"O gênero com maior volume de itens comprados é '{genero_top}', "
        f"o que pode orientar campanhas e sortimento direcionados.",

        f"A categoria de produto mais vendida é '{categoria_top}', "
        f"indicando o principal motor de vendas da rede.",

        "A coluna de número de filhos do cliente (CL_FHL) apresenta baixa "
        "variabilidade (poucos valores distintos, de 0 a 4), o que é "
        "coerente com um dado cadastral discreto e sugere que ela é mais "
        "útil como variável de segmentação do que de tendência central.",

        "Problemas remanescentes: (a) a base não possui coluna de valor "
        "monetário (preço/quantidade), o que limita análises de "
        "faturamento e ticket médio; (b) mesmo após a imputação, a "
        "categoria 'NAO INFORMADO' (antigo '#N/D') ainda representa "
        "produtos sem classificação de categoria, o que pode ser "
        "melhorado com um cadastro de produtos mais completo; (c) não há "
        "verificação cruzada de que os dados cadastrais do cliente "
        "(gênero, estado civil, filhos) são estáveis ao longo do tempo "
        "para o mesmo CL_ID.",
        
    ]
    for i, c in enumerate(conclusoes, start=1):
        print(f"{i}.{c}\n")
# ==========================================================================
# EXECUÇÃO PRINCIPAL
# ==========================================================================
#Passagem de parâmetros para os Métodos criados anteriormente
def main():
    df_bruto = carregar_dados(ARQUIVO_ENTRADA)
    diagnosticar_problemas(df_bruto)
    df_limpo = limpar_dados(df_bruto)
    validar_regra_co_id(df_limpo)
    estatisticas_filho(df_limpo)
    explorar_agrupamento(df_limpo)
    gerar_conclusoes(df_bruto, df_limpo)

    #Salva a base limpa para uso em Análises ou Dashboards
    df_limpo.to_csv(ARQUIVO_SAIDA, sep=";", index=False)
    linha("Fim da execução")
    print(f"Base limpa exportada para: {ARQUIVO_SAIDA}")
if __name__ == "__main__":
    main()




