import streamlit as st
import pandas as pd
import plotly.express as px

try:
    from model.database import executar_select
except Exception:
    executar_select = None



connection_string = f"mssql+pymssql://{username}:{password}@{server}/{database}"
engine = create_engine(connection_string)

st.title("Dashboard VW_SEGDEP com Streamlit e Plotly")

@st.cache_data(ttl=600)
def carregar_dados():
    query = """
    SELECT
        CASE WHEN SEXO = 'M' THEN 'Masculino' ELSE 'Feminino' END AS Sexo,
        IDADE,
        CASE WHEN IDSITUACAO = 1 THEN 'Ativo' ELSE 'Inativo' END AS Situacao,
        CASE WHEN SEQDEP = 0 THEN 'Titular' ELSE 'Dependente' END AS Tipo
    FROM VW_SEGDEP
    """
    df = pd.read_sql(query, engine)
    return df

# Carrega dados do banco
df = carregar_dados()

# Mostra tabela de dados
st.subheader("Dados da VW_SEGDEP")
st.dataframe(df)

# Função para categorizar faixa etária (igual ao exemplo anterior)
def faixa_etaria(idade):
    if idade <= 9:
        return "0-9"
    elif idade <= 17:
        return "10-17"
    elif idade <= 25:
        return "18-25"
    elif idade <= 39:
        return "26-39"
    elif idade <= 59:
        return "40-59"
    else:
        return "60+"

df["Faixa Etária"] = df["IDADE"].apply(faixa_etaria)

# Gráfico 1: Distribuição por Sexo
fig_sexo = px.histogram(df, x="Sexo", title="Distribuição por Sexo")
st.plotly_chart(fig_sexo)

# Gráfico 2: Distribuição por Faixa Etária
fig_idade = px.histogram(df, x="Faixa Etária",
                        title="Distribuição por Faixa Etária",
                        category_orders={"Faixa Etária": ["0-9","10-17","18-25","26-39","40-59","60+"]})
st.plotly_chart(fig_idade)

# Gráfico 3: Situação (Ativo/Inativo)
fig_situacao = px.histogram(df, x="Situacao", title="Distribuição por Situação")
st.plotly_chart(fig_situacao)

# Gráfico 4: Tipo (Titular/Dependente)
fig_tipo = px.histogram(df, x="Tipo", title="Distribuição por Tipo")
st.plotly_chart(fig_tipo)