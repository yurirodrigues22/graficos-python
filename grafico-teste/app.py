# app.py
import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib

#      cd C:\Users\estagioti\Desktop\python
#      venv\Scripts\activate
#      streamlit run app.py


# evita erro do Tkinter quando matplotlib tenta abrir janelas
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from queries import QUERIES, FALLBACK

# tenta importar a função que executa selects (do seu projeto)
try:
    from model.database import executar_select
except Exception:
    executar_select = None


# -----------------------------
# Mapas de análises (definidos no topo para evitar NameError)
# -----------------------------
MAP_GERAL = {
    "Distribuição por Sexo (Segurados)": "sexo_segurados",
    "Perfil Etário da População (Segurados)": "idade_segurados",
    "Alerta (Segurados)": "alerta_segurados",
    "Situação (Segurados)": "situacao_segurados",
    "Carteira (Segurados)": "carteira_segurados",
    "Titular vs Dependente": "titular"
}

MAP_TITULAR = { 
    "Sexo (Titulares)": "sexo_titulares",
    "Carteira (Titulares)": "carteira_titulares",
}

MAP_DEP = {
    "Parentesco (Dependentes)": "parentesco_dependentes",
    "Situação (Dependentes)": "situacao_dependentes",
    "Alerta (Dependentes)": "alerta_dependentes"
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
    """Executa a query (ou retorna fallback)."""
    if analise not in QUERIES:
        return FALLBACK.get(analise, ([], []))
    if executar_select is None:
        # ambiente sem BD: retorna fallback
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


def build_chart(df: pd.DataFrame, chart_type: str, cor: str = "#4C78A8"):
    """Retorna figura matplotlib pronta ou None se df vazio."""
    if df.empty:
        return None
    fig, ax = plt.subplots(figsize=(12, 6))
    if chart_type == "Gráfico de Barras":
        sns.barplot(data=df, x="Categoria", y="Quantidade", ax=ax, color=cor)
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
    else:
        ax.pie(df["Quantidade"], labels=df["Categoria"], autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        plt.tight_layout()
    return fig


def render_tab(titulo: str, opcoes_map: dict, cor: str, key_prefix: str, metric_label: str):
    """
    Renderiza uma aba com:
      - coluna esquerda: controles (selects) + métrica + tabela
      - coluna direita: gráfico
    """
    # layout - controles à esquerda (narrow), conteúdo à direita (wide)
    left_col, right_col = st.columns([0.35, 0.65])

    with left_col:
        st.subheader(titulo)
        opcao = st.selectbox("Escolha a análise:", list(opcoes_map.keys()), key=f"{key_prefix}_analysis")
        chart_type = st.selectbox("Tipo de visualização:", ["Gráfico de Barras", "Gráfico de Pizza"],
                                  key=f"{key_prefix}_chart")

        # consulta os dados já aqui para mostrar a métrica e a tabela
        analise = opcoes_map[opcao]
        labels, valores = consultar(analise)
        df = pd.DataFrame({"Categoria": labels, "Quantidade": valores})
        total = int(df["Quantidade"].sum()) if not df.empty else 0

        st.metric(metric_label, total)
        st.dataframe(df, use_container_width=True)

    with right_col:
        if df.empty:
            st.info("Sem dados para essa análise.")
        else:
            fig = build_chart(df, chart_type, cor)
            if fig:
                st.pyplot(fig)
            return

        fig = build_chart(df, chart_type, cor)
        if fig:
            st.pyplot(fig)
        st.dataframe(df, use_container_width=True)


# -----------------------------
# Configuração da página
# -----------------------------
st.set_page_config(page_title="Dashboard Beneficiários", layout="wide")
st.title("📈 Análise de Perfil dos Beneficiários")
st.write("Este painel apresenta a distribuição dos beneficiários com base nos dados extraídos do sistema.")

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3 = st.tabs(["▤ Geral", "👤 Titulares", "👥 Dependentes"])

with tab1:
    render_tab("Análises Gerais", MAP_GERAL, cor="#e74c3caa", key_prefix="geral", metric_label="Beneficiários Cadastrados")

with tab2:
    render_tab("Titulares", MAP_TITULAR, cor="#00bfffaa", key_prefix="titular", metric_label="Titulares Cadastrados")

with tab3:
    render_tab("Dependentes", MAP_DEP, cor="#32cd32aa", key_prefix="dependente", metric_label="Dependentes Cadastrados")




# -----------------------------
# Estilo
# -----------------------------
st.markdown("""
 <style>
    .block-container {
        max-width: 100vw !important;
        max-height: 100vh !important;
        padding: 3rem 2rem;
        border-radius: 8px;
    }

    div[data-testid="column"] {
        flex: 1 !important;
        min-width: 0 !important;
        padding: 0.5rem;
    }

    h1 {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #2c3e50;
        margin-bottom: 1rem;
    }

    .stDataFrame {
        border: 1px solid #ddd;
        border-radius: 6px;
        background-color: #fff;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        color: #2c3e50;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)
