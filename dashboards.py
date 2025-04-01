import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# Título na barra lateral
st.sidebar.title("Seleção de Unidades")
uploaded_file = st.file_uploader("Choose a file") # Adiciona o uploader
if uploaded_file is not None:
    # Importando os dados
    df = pd.read_csv(uploaded_file, sep=";", decimal=",", encoding="latin1")
    
    # Resto do código continua aqui...
else:
    st.warning('Por favor, faça o upload de um arquivo CSV (separado por virgulas) para começar a análise.')
    st.stop()

# pegar os valores da coluna unidade
unidades_selecionadas = st.sidebar.multiselect("Unidades", df["UNIDADE"].unique())
# Filtrar o DataFrame com base nas unidades selecionadas
df_filtrado = df[df["UNIDADE"].isin(unidades_selecionadas)]


# Exibir o DataFrame filtrado
st.dataframe(df_filtrado)


col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
col5 = st.columns(1)

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


# Calcula a altura com base no número de cursos
height = len(pagos_por_curso) * 50  # Ajuste o multiplicador conforme necessário

# Cria gráfico de barras com os dados agrupados

fig_pagamentos = px.bar(pagos_por_curso, 
                       x="CURSO", 
                       y="quantidade",
                       title="Quantidade de Pagos por Curso")

# Adiciona rótulos com as quantidades
fig_pagamentos.update_traces(texttemplate='%{y}', textposition='outside')


# Exibe o gráfico
col4.plotly_chart(fig_pagamentos, use_container_width=True)

# Calcula a idade com base na data de nascimento
df_filtrado["IDADE"] = df_filtrado["DTNASC"].apply(
    lambda x: min(datetime.now().year - datetime.strptime(x, "%d/%m/%Y").year, 100)
)

# Cria faixas etárias
def get_faixa_etaria(idade):
    if idade < 20:
        return "Até 19 anos"
    elif idade < 30:
        return "20-29 anos"
    elif idade < 40:
        return "30-39 anos"
    elif idade < 50:
        return "40-49 anos"
    elif idade < 60:
        return "50-59 anos"
    else:
        return "60+ anos"

df_filtrado["FAIXA_ETARIA"] = df_filtrado["IDADE"].apply(get_faixa_etaria)

# Agrupa os dados por faixa etária
idade_counts = df_filtrado.groupby("FAIXA_ETARIA").size().reset_index(name="quantidade")

# Ordena as faixas etárias
ordem_faixas = ["Até 19 anos", "20-29 anos", "30-39 anos", "40-49 anos", "50-59 anos", "60+ anos"]
idade_counts["FAIXA_ETARIA"] = pd.Categorical(idade_counts["FAIXA_ETARIA"], categories=ordem_faixas, ordered=True)
idade_counts = idade_counts.sort_values("FAIXA_ETARIA")

# Cria o gráfico de barras para mostrar a quantidade de alunos por faixa etária
fig_idades = px.bar(
    idade_counts,
    x="FAIXA_ETARIA",
    y="quantidade",
    title="Quantidade de Alunos por Faixa Etária",
    labels={"FAIXA_ETARIA": "Faixa Etária", "quantidade": "Quantidade"},
)

# Adiciona rótulos com as quantidades
fig_idades.update_traces(texttemplate='%{y}', textposition='outside')

# Exibe o gráfico
col5[0].plotly_chart(fig_idades, use_container_width=True)