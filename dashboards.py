import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go



st.set_page_config(layout="wide")

# Título na barra lateral
st.sidebar.title("Seleção de Unidades")

# Importando os dados
df = pd.read_csv("AVP45.csv", sep=";", decimal=",", encoding="latin1")

# pegar os valores da coluna unidade
unidades_selecionadas = st.sidebar.multiselect("Unidades", df["UNIDADE"].unique())

# Filtrar o DataFrame com base nas unidades selecionadas
df_filtrado = df[df["UNIDADE"].isin(unidades_selecionadas)]

# Exibir o DataFrame filtrado

st.dataframe(df_filtrado)

col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

# Contar a quantidade de pagamentos por curso
pagamentos_por_curso = df_filtrado["CURSO"].value_counts().reset_index()
pagamentos_por_curso.columns = ["CURSO", "QUANTIDADE"]

# Concatenar as informações de pagamento na coluna "text"
df_filtrado.loc[:, "TEXT"] = df_filtrado["PAGAMENTO"]
# Contar a quantidade de inscritos, aprovados e reprovados na coluna "SITUACAO"
situacao_counts = df_filtrado["SITUACAO"].value_counts()
inscritos = situacao_counts.get("INSCRITO", 0)
aprovados = situacao_counts.get("APROVADO", 0)
reprovados = situacao_counts.get("REPROVADO", 0)

fig_unidades = px.bar(df_filtrado, x="SITUACAO", color="SITUACAO", title="Situação por UNIDADE")

# Calcular a soma de cada coluna
soma_colunas = df_filtrado.groupby("SITUACAO").size()

# Adicionar anotações ao gráfico
for situacao, soma in soma_colunas.items():
    fig_unidades.add_trace(go.Scatter(
        x=[situacao],
        y=[soma],
        text=[soma],
        mode='text',
        textposition='top center'
    ))

col1.plotly_chart(fig_unidades,use_container_width=True)

# Gráfico de pagamentos por curso
fig_cursos = px.pie(df_filtrado, names="PAGAMENTO", title="Pagamentos por UNIDADE", values=[1] * len(df_filtrado))

col2.plotly_chart(fig_cursos)



#Situação por cidade
fig_cidades = px.bar(df_filtrado, x="CIDADE", color="SITUACAO", title="Situação por CIDADE")

for cidade, soma in df_filtrado.groupby("CIDADE").size().items():
    fig_cidades.add_trace(go.Scatter(
        x=[cidade],
        y=[soma],
        text=[soma],
        mode='text',
        textposition='top center'
    ))
col3.plotly_chart(fig_cidades, use_container_width=True)