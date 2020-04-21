import streamlit as st
import pandas as pd

import plotly.express as px

import plotly.graph_objects as go
from config_data import load_data_brasil_io


def monta_pais(taxa_mortalidade):
    df = load_data_brasil_io()
    filtro = (df['place_type'] == 'state')
    dados_estado = df[filtro]

    st.title(f"Dados de COVID no Brasil")

    dados_estado_plot = dados_estado.groupby('date').sum()
    hoje = dados_estado[dados_estado['is_last']].sum()
    hoje_estados = dados_estado[dados_estado['is_last']]
    dados_estado_plot = dados_estado_plot[:dados_estado_plot.shape[0]-1]

    dia_atual = dados_estado.reset_index()['date'].max().strftime('%d-%m-%Y')

    confirmados = hoje.loc['confirmed'].astype(int)
    mortes = hoje.loc['deaths'].astype(int)
    taxa = round(mortes/confirmados * 10000)/100
    quantidade_estimada = (100 * mortes / taxa_mortalidade).astype(int)
    st.markdown(f"O Brasil teve até o dia **{dia_atual}** "
                f"um total de **{confirmados}** casos confirmados e"
                f" **{mortes}** mortes com uma taxa de mortalidade de **{taxa}%**.")
    if mortes > 0:
        st.markdown(f"Com base na taxa de mortalidade de outros países (**{taxa_mortalidade}%** dos infectados) "
                f"a quantidade estimada de infectados seria de **{quantidade_estimada}** para a quantidade de mortos atual.")

    dados_estado_melt = pd.melt(
        dados_estado[['date', 'state', 'confirmed', 'deaths']],
        id_vars=['date', 'state'],
        value_vars=['confirmed', 'deaths'])

    df = dados_estado_melt.groupby(["date", 'variable']).sum().reset_index()

    fig = px.line(df, x="date", y="value", color='variable')

    fig.update_layout(title='Covid no Brasil',
                      xaxis_title='Data',
                      yaxis_title='Número de casos')
    st.plotly_chart(fig)

    hoje_estados_indice = hoje_estados
    hoje_estados_indice['estado'] = hoje_estados['state']
    hoje_estados_indice = hoje_estados.set_index(['state'] )
    hoje_estados_plot = hoje_estados_indice[['confirmed', 'deaths', 'estado']]

    estados_list = hoje_estados_plot['estado']
    confirmados_list = hoje_estados_plot['confirmed']
    mortos_list = hoje_estados_plot['deaths']

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=estados_list,
        y=confirmados_list,
        name='Casos Confirmados',
        marker_color='royalblue'
    ))


    fig.update_layout(barmode='group', xaxis_tickangle=-45, xaxis={'categoryorder':'total descending'})
    fig.update_layout(title='Casos Confirmados',
                      xaxis_title='Data',
                      yaxis_title='Número de casos')
    st.plotly_chart(fig)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=estados_list,
        y=mortos_list,
        name='Mortes',
        marker_color='firebrick'
    ))
    fig.update_layout(barmode='group', xaxis_tickangle=-45, xaxis={'categoryorder':'total descending'})
    fig.update_layout(title='Mortes',
                      xaxis_title='Data',
                      yaxis_title='Número de casos')
    st.plotly_chart(fig)

