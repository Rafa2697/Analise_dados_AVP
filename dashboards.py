import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(layout="wide")

# Título na barra lateral
st.sidebar.title("Seleção de Unidades")
uploaded_file = st.file_uploader("Arquivo extraído do vestibular, analítico.") # Adiciona o uploader
# Segundo file uploader (independente do primeiro)
uploaded_file_2 = st.file_uploader("Arquivo extraído de matrícula, analítico")

# Processamento do primeiro arquivo
if uploaded_file is not None:
    
    df = pd.read_csv(uploaded_file, sep=";", decimal=",", encoding="latin1")
    unidades_selecionadas = st.sidebar.multiselect("Unidades (Vestibular)", df["UNIDADE"].unique())
    df_filtrado = df[df["UNIDADE"].isin(unidades_selecionadas)]
    
    #opção para mostrar a planilha crua
    if st.checkbox("Mostrar planilha de dados", value=False):
        st.dataframe(df_filtrado)
    
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5, col6 = st.columns(2)
    
     # Gráfico de inscritos por curso
    inscritos_por_curso = df_filtrado.groupby("CURSO").size(). reset_index(name="quantidade")
    fig_unidades = px.bar(inscritos_por_curso, x="CURSO", y="quantidade", color="CURSO", title="Situação de inscritos por Curso", height=600)
    # Adiciona rótulos com as quantidades
    fig_unidades.update_traces(texttemplate='%{y}', textposition='outside')
    # ajustes visuais (esconde legenda repetitiva e evita sobreposição de rótulos longos)
    fig_unidades.update_layout(showlegend=False, xaxis_tickangle=-45, margin=dict(b=140))
    col1.plotly_chart(fig_unidades,use_container_width=True)
    
    # Gráfico de pagamentos por curso
    fig_cursos = px.pie(df_filtrado, names="PAGAMENTO", title="Pagamentos por UNIDADE selecionada", values=[1] * len(df_filtrado))
    col2.plotly_chart(fig_cursos, use_container_width=True)

    #Situação por cidade
    inscritos_por_cidade = df_filtrado.groupby("CIDADE").size().reset_index(name="quantidade")
    fig_cidades = px.bar(inscritos_por_cidade, 
            x="CIDADE", 
            y="quantidade",
            title="Quantidade de Inscritos por Cidade",
            height=650)
    fig_cidades.update_traces(texttemplate='%{y}', textposition='outside')
    fig_cidades.update_layout(showlegend=False, xaxis_tickangle=-45, margin=dict(b=140))
    col3.plotly_chart(fig_cidades, use_container_width=True)

    # Cria o agrupamento por curso
    pagos_por_curso = df_filtrado[df_filtrado["PAGAMENTO"].isin(["Pago", "Bolsa 100%"])].groupby("CURSO").size().reset_index(name="quantidade")
    # Cria gráfico de barras com os dados agrupados
    fig_pagamentos = px.bar(pagos_por_curso, 
            x="CURSO", 
            y="quantidade",
            color="CURSO",
            title="Quantidade de Pagos por Curso",
            height=600)
    # Adiciona rótulos com as quantidades
    fig_pagamentos.update_traces(texttemplate='%{y}', textposition='outside')
    # Exibe o gráfico
    fig_pagamentos.update_layout(showlegend=False, xaxis_tickangle=-45, margin=dict(b=140))
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
    col5.plotly_chart(fig_idades, use_container_width=True)
    
    #pagantes por idade
    df_filtrado["IDADE_PAGO"] = df_filtrado["PAGAMENTO"].apply(lambda x: 1 if x in ["Pago", "Bolsa 100%"] else 0)
    idade_counts = df_filtrado[df_filtrado["IDADE_PAGO"] == 1].groupby("FAIXA_ETARIA").size().reset_index(name="quantidade")
    
    # Ordena as faixas etárias
    ordem_faixas = ["Até 19 anos", "20-29 anos", "30-39 anos", "40-49 anos", "50-59 anos", "60+ anos"]
    idade_counts["FAIXA_ETARIA"] = pd.Categorical(idade_counts["FAIXA_ETARIA"], categories=ordem_faixas, ordered=True)
    idade_counts = idade_counts.sort_values("FAIXA_ETARIA")
    
    # Cria o gráfico de barras para mostrar a quantidade de alunos por faixa etária
    fig_idades_p = px.bar(
        idade_counts,
        x="FAIXA_ETARIA",
        y="quantidade",
        title="Quantidade de pagos por Faixa Etária",
        labels={"FAIXA_ETARIA": "Faixa Etária", "quantidade": "Quantidade"},
    )
    fig_idades_p.update_traces(texttemplate='%{y}', textposition='outside')
    
    col6.plotly_chart(fig_idades_p, use_container_width=True)
    
###########################################################

# Processamento do segundo arquivo
if uploaded_file_2 is not None:
    
    df_2 = pd.read_csv(uploaded_file_2, sep=";", decimal=",", encoding="latin1") # Adiciona o uploader
    
    unidades_selecionadas_2 = st.sidebar.multiselect("Unidades (Matrícula)", df_2["unidade"].unique())
    
    df_filtrado_2 = df_2[df_2["unidade"].isin(unidades_selecionadas_2)]# Adiciona o uploader
    #st.dataframe(df_filtrado_2)
    
    col1, col2 = st.columns(2)
    
    #pegar o ano de dtpgto de df_filtrado_2
    df_filtrado_2["dtpgto"] = pd.to_datetime(df_filtrado_2["dtpgto"], format="%d/%m/%Y")
    df_filtrado_2["ano_mes"] = df_filtrado_2["dtpgto"].dt.strftime("%Y-%m")
    
    # Agrupa por ano_mes e conta as ocorrências
    contagem_por_mes = df_filtrado_2.groupby("ano_mes").size().reset_index(name="quantidade")
    
    # Cria o gráfico de barras
    fig = px.bar(contagem_por_mes, 
                x="ano_mes", 
                y="quantidade",
                title="Quantidade de Pagamentos por Mês",
                labels={"ano_mes": "Período", "quantidade": "Quantidade de Pagamentos"})
    
    # Adiciona os valores sobre as barras
    fig.update_traces(texttemplate='%{y}', textposition='outside')
    
    # Primeiro, crie uma contagem das situações de matrícula
    df_matriculas = df_filtrado_2.groupby("matricula").size().reset_index(name="contagem")

    # Agora crie o gráfico de pizza corretamente
    fig2 = px.pie(df_matriculas, 
                values="contagem",  # Usa a contagem como valores
                names="matricula",  # Usa a situação da matrícula como nomes
                title="Situação das Matrículas")

    col1.plotly_chart(fig,use_container_width=True)
    col2.plotly_chart(fig2,use_container_width=True)

if uploaded_file is None and uploaded_file_2 is None:
    st.warning('Por favor, faça o upload de pelo menos um arquivo CSV (separado por virgula) para começar a análise.')
    st.stop()










