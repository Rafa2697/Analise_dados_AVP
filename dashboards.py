import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# Título na barra lateral
st.sidebar.title("Seleção de Unidades")

# Importando os dados
df = pd.read_csv("Ambiente Virtual do Parceiro - AVP (38).csv", sep=";", decimal=",", encoding="latin1")

# pegar os valores da coluna unidade
unidades_selecionadas = st.sidebar.multiselect("Unidades", df["UNIDADE"].unique())

# Filtrar o DataFrame com base nas unidades selecionadas
df_filtrado = df[df["UNIDADE"].isin(unidades_selecionadas)]

# Exibir o DataFrame filtrado
st.dataframe(df_filtrado)

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

fig_unidades = px.bar(df_filtrado, x="CURSO",color="SITUACAO", title="Situação por Curso", height=600)

for cidade, soma in df_filtrado.groupby("CURSO").size().items():
    fig_unidades.add_trace(go.Scatter(
        x=[cidade],
        y=[soma],
        text=[soma],
        mode='text',
        textposition='top center'
    ))
    
col1.plotly_chart(fig_unidades,use_container_width=True)

# Gráfico de pagamentos por curso
fig_cursos = px.pie(df_filtrado, names="PAGAMENTO", title="Pagamentos por UNIDADE selecionada", values=[1] * len(df_filtrado))

col2.plotly_chart(fig_cursos, use_container_width=True)



#Situação por cidade
fig_cidades = px.bar(df_filtrado, x="CIDADE", color="SITUACAO", title="Inscritos por CIDADE")

for cidade, soma in df_filtrado.groupby("CIDADE").size().items():
    fig_cidades.add_trace(go.Scatter(
        x=[cidade],
        y=[soma],
        text=[soma],
        mode='text',
        textposition='top center'
    ))
col3.plotly_chart(fig_cidades, use_container_width=True)

# Cria o agrupamento por curso
pagos_por_curso = df_filtrado[df_filtrado["PAGAMENTO"].isin(["Pago", "Bolsa 100%"])].groupby("CURSO").size().reset_index(name="quantidade")

# Cria gráfico de barras com os dados agrupados
fig_pagamentos = px.bar(pagos_por_curso, 
                       x="CURSO", 
                       y="quantidade",
                       title="Quantidade de Pagos por Curso", 
                       height=600)

# Adiciona rótulos com as quantidades
fig_pagamentos.update_traces(texttemplate='%{y}', textposition='outside')


# Exibe o gráfico
col4.plotly_chart(fig_pagamentos, use_container_width=True)