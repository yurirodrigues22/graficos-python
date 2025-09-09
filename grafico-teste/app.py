# app.py
import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib

# evita erro do Tkinter quando matplotlib tenta abrir janelas
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# tenta importar a função que executa selects (do seu projeto)
try:
    from model.database import executar_select
except Exception:
    executar_select = None

# -----------------------------
# Queries (copiadas do seu código original)
# -----------------------------
sql_sexo = """
    SELECT 
        CASE WHEN SEXO = 'M' THEN 'Masculino' ELSE 'Feminino' END AS genero,
        COUNT(*)
    FROM VW_SEGDEP
    GROUP BY genero
"""

sql_idade = """
    SELECT 
        CASE 
            WHEN IDADE BETWEEN 0 AND 9 THEN '0-9'
            WHEN IDADE BETWEEN 10 AND 17 THEN '10-17'
            WHEN IDADE BETWEEN 18 AND 25 THEN '18-25'
            WHEN IDADE BETWEEN 26 AND 39 THEN '26-39'
            WHEN IDADE BETWEEN 40 AND 59 THEN '40-59'
            ELSE '60+'
        END AS faixa,
        COUNT(*)
    FROM VW_SEGDEP
    GROUP BY 
        CASE 
            WHEN IDADE BETWEEN 0 AND 9 THEN '0-9'
            WHEN IDADE BETWEEN 10 AND 17 THEN '10-17'
            WHEN IDADE BETWEEN 18 AND 25 THEN '18-25'
            WHEN IDADE BETWEEN 26 AND 39 THEN '26-39'
            WHEN IDADE BETWEEN 40 AND 59 THEN '40-59'
            ELSE '60+'
        END
    ORDER BY 1
"""

sql_titular_dependente = """
    SELECT 
        CASE WHEN SEQDEP = 0 THEN 'Titular' ELSE 'Dependente' END AS tipo,
        COUNT(*)
    FROM VW_SEGDEP
    GROUP BY CASE WHEN SEQDEP = 0 THEN 'Titular' ELSE 'Dependente' END
"""

sql_situacao_dependentes = """
    SELECT 
        CASE WHEN SITUACAO = 1 THEN 'Ativo' ELSE 'Inativo' END AS status,
        COUNT(*)
    FROM VW_SEGDEP
    GROUP BY CASE WHEN SITUACAO = 1 THEN 'Ativo' ELSE 'Inativo' END
"""

sql_alerta_dependentes = """
    SELECT 
        CASE WHEN MSG_ALERTA IS NOT NULL AND MSG_ALERTA <> '' THEN 'Com alerta' ELSE 'Sem alerta' END AS alerta,
        COUNT(*)
    FROM VW_SEGDEP
    GROUP BY CASE WHEN MSG_ALERTA IS NOT NULL AND MSG_ALERTA <> '' THEN 'Com alerta' ELSE 'Sem alerta' END
"""

sql_parentesco_dependentes = """
   SELECT 
        CASE 
            WHEN IDGRAU_PARENTESCO = 1 THEN 'Cônjuge'
            WHEN IDGRAU_PARENTESCO = 2 THEN 'Filho(a)'
            WHEN IDGRAU_PARENTESCO = 3 THEN 'Pai/Mãe'
            ELSE 'Desconhecido'
        END AS parentesco,
        COUNT(*) AS quantidade
    FROM VW_SEGDEP
    WHERE SEQDEP <> 0
    GROUP BY 
        CASE 
            WHEN IDGRAU_PARENTESCO = 1 THEN 'Cônjuge'
            WHEN IDGRAU_PARENTESCO = 2 THEN 'Filho(a)'
            WHEN IDGRAU_PARENTESCO = 3 THEN 'Pai/Mãe'
            ELSE 'Desconhecido'
        END
"""

sql_sexo_titulares = """
    SELECT 
        CASE WHEN SEXO = 'M' THEN 'Masculino' ELSE 'Feminino' END AS genero,
        COUNT(*)
    FROM VW_SEGDEP
    WHERE SEQDEP = 0
    GROUP BY genero
"""

sql_carteira = """
    SELECT 
        CASE 
            WHEN CARTEIRA_UNIMED IS NOT NULL AND CARTEIRA_UNIMED <> '' THEN 'Nova'
            WHEN CARTEIRA_UNIMED_OLD IS NOT NULL AND CARTEIRA_UNIMED_OLD <> '' THEN 'Antiga'
            ELSE 'Nenhuma'
        END AS tipo,
        COUNT(*)
    FROM VW_SEGDEP
    GROUP BY CASE 
            WHEN CARTEIRA_UNIMED IS NOT NULL AND CARTEIRA_UNIMED <> '' THEN 'Nova'
            WHEN CARTEIRA_UNIMED_OLD IS NOT NULL AND CARTEIRA_UNIMED_OLD <> '' THEN 'Antiga'
            ELSE 'Nenhuma'
        END
"""

# -----------------------------
# Mapeamento de chaves (inclui aliases para compatibilidade)
# -----------------------------
QUERIES = {
    "sexo": sql_sexo,
    "idade": sql_idade,
    "titular": sql_titular_dependente,
    "titular_dependente": sql_titular_dependente,
    "situacao": sql_situacao_dependentes,
    "situacao_dependentes": sql_situacao_dependentes,
    "alerta": sql_alerta_dependentes,
    "alerta_dependentes": sql_alerta_dependentes,
    "dependentes_parentesco": sql_parentesco_dependentes,
    "parentesco_dependentes": sql_parentesco_dependentes,
    "sexo_titulares": sql_sexo_titulares,
    "carteira": sql_carteira,
}

FALLBACK = {
    "sexo": (['Masculino', 'Feminino'], [0, 0]),
    "idade": (['0-9', '10-17', '18-25', '26-39', '40-59', '60+'], [0, 0, 0, 0, 0, 0]),
    "titular": (['Titular', 'Dependente'], [0, 0]),
    "titular_dependente": (['Titular', 'Dependente'], [0, 0]),
    "situacao": (['Ativo', 'Inativo'], [0, 0]),
    "situacao_dependentes": (['Ativo', 'Inativo'], [0, 0]),
    "alerta": (['Com alerta', 'Sem alerta'], [0, 0]),
    "alerta_dependentes": (['Com alerta', 'Sem alerta'], [0, 0]),
    "dependentes_parentesco": (['Cônjuge', 'Filho(a)', 'Pai/Mãe', 'Desconhecido'], [0, 0, 0, 0]),
    "parentesco_dependentes": (['Cônjuge', 'Filho(a)', 'Pai/Mãe', 'Desconhecido'], [0, 0, 0, 0]),
    "sexo_titulares": (['Masculino', 'Feminino'], [0, 0]),
    "carteira": (['Nova', 'Antiga', 'Nenhuma'], [0, 0, 0]),
}

# -----------------------------
# Funções auxiliares
# -----------------------------
def _to_int_safe(v):
    try:
        return int(v)
    except Exception:
        try:
            return int(float(v))
        except Exception:
            return 0

@st.cache_data(show_spinner=False)
def consultar(analise: str):
    if analise not in QUERIES:
        return FALLBACK.get(analise, ([], []))
    if executar_select is None:
        return FALLBACK.get(analise, ([], []))
    sql = QUERIES[analise]
    try:
        rows = executar_select(sql)
        labels = [r[0] for r in rows]
        valores = [_to_int_safe(r[1]) for r in rows]
        return labels, valores
    except Exception as e:
        st.warning(f"Erro ao consultar banco: {e}") 
        return FALLBACK.get(analise, ([], []))

# -----------------------------
# Interface Streamlit
# -----------------------------
st.set_page_config(page_title="Dashboard Beneficiários", layout="wide")
st.title("📈 Análise de Perfil dos Beneficiários")
st.write("Este painel apresenta a distribuição dos beneficiários com base nos dados extraídos do sistema.")

# opções exibidas no sidebar
OPTIONS = {
    "Distribuição por Sexo": "sexo",
    "Perfil Etário da População": "idade",
    "Titular vs Dependente": "titular",
    "Situação (dependentes)": "situacao",
    "Alerta (dependentes)": "alerta",
    "Parentesco (dependentes)": "dependentes_parentesco",
    "Sexo (apenas titulares)": "sexo_titulares",
    "Carteira Segurados": "carteira",
}

analise_key = st.sidebar.selectbox("O que você deseja analisar?", list(OPTIONS.keys()))
analise = OPTIONS[analise_key]

# escolha do tipo de gráfico
chart_type = st.sidebar.selectbox("Tipo de visualizaçao", ["Gráfco de Barras", "Gráfico de Pizza"])

labels, valores = consultar(analise)
df = pd.DataFrame({"Categoria": labels, "Quantidade": valores})

st.metric("Beneficiários Cadastrados:", int(df["Quantidade"].sum()) if not df.empty else 0)

# cria gráfico com tamanho ajustável
fig, ax = plt.subplots(figsize=(12, 6))

if df.empty:
    st.info("Sem dados para essa análise (modo offline ou resultado vazio).")
else:
    if chart_type == "Gráfco de Barras":  # <- corrigido para bater com o texto do selectbox
        colors = ["#ff0000a9"]
        sns.barplot(
            data=df,
            x="Categoria",
            y="Quantidade",
            ax=ax,
            palette=colors[: len(df)]
        )
        ax.set_xlabel("")
        ax.set_ylabel("Quantidade")
        ax.set_title(analise_key)
        plt.xticks(rotation=30)
    elif chart_type == "Gráfico de Pizza":
        colors = ["#ff0000a9", "#ffa832", "#e74c3c", "#e67e22", "#fd3a2d",  "#ffcc33"]
        ax.pie(
            df["Quantidade"],
            labels=df["Categoria"],
            autopct="%1.1f%%",
            startangle=90,
            colors=colors[: len(df)]
        )
        ax.axis("equal")
        ax.set_title(analise_key)

# layout lado a lado (2 colunas)
col1, col2 = st.columns([0.65, 0.35])  

with col1:
    st.pyplot(fig, clear_figure=True, use_container_width=False)

with col2:
    st.markdown("### 🧾 Resumo dos Dados")
    st.dataframe(df, use_container_width=True)
    
st.markdown("""
 <style>
    /* container central ocupa 100% da viewport */
    .block-container {
        max-width: 100vw !important;
        max-height: 100vh !important;
        padding: 3rem 2rem;          /* espaçamento mais equilibrado */
           /* fundo claro e suave */
        border-radius: 8px;          /* cantos levemente arredondados */
    }

    /* garante que colunas nunca forcem scroll horizontal */
    div[data-testid="column"] {
        flex: 1 !important;
        min-width: 0 !important;
        padding: 0.5rem;
    }

    /* título mais destacado */
    h1 {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #2c3e50;
        margin-bottom: 1rem;
    }

    /* tabelas com borda suave */
    .stDataFrame {
        border: 1px solid #ddd;
        border-radius: 6px;
        background-color: #fff;
    }

    /* métricas com destaque visual */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        color: #2c3e50;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)
