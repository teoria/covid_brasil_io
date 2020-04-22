import streamlit as st
import pandas as pd

import plotly.express as px

import plotly.graph_objects as go

from config_data import load_data_brasil_io

from datetime import timedelta, date


def date_range( start_date, end_date):
    for n in range( int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def append_data(df, dias_para_completar, max):
    df = df[['date', 'state', 'confirmed', 'deaths']]
    df_novo = pd.DataFrame(columns=['date', 'state', 'confirmed', 'deaths'])
    for i in range(dias_para_completar.shape[0]):
        lista_datas = date_range(dias_para_completar.iloc[i, 0]+ timedelta(1), max+ timedelta(1))

        for single_date in lista_datas:
            obj = {
                'date': single_date,
                'state': dias_para_completar.iloc[i, 1],
                'confirmed': dias_para_completar.iloc[i, 4],
                'deaths': dias_para_completar.iloc[i, 5]
            }
            df_novo = df_novo.append(obj, ignore_index=True)

    return df_novo


def monta_pais(taxa_mortalidade):
    df = load_data_brasil_io()
    filtro = (df['place_type'] == 'state')
    dados_estado = df[filtro]

    st.title(f"Dados de COVID no Brasil")

    dados_estado_plot = dados_estado.groupby('date').sum()
    hoje = dados_estado[dados_estado['is_last']].sum()
    hoje_estados = dados_estado[dados_estado['is_last']]
    dias_para_completar_filtro = hoje_estados['date'] < hoje_estados['date'].max()
    dias_para_completar = hoje_estados[dias_para_completar_filtro]

    #st.dataframe(dados_estado[dados_estado['is_last']])
    #st.dataframe(hoje)

    hoje_estados_append = append_data(
        hoje_estados,
        dias_para_completar,
        dados_estado['date'].max()
    )

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

    dados_estado = dados_estado.append(hoje_estados_append, ignore_index=True)

    #st.dataframe(dados_estado.loc[ dados_estado['date']==dados_estado['date'].max() ])
    #st.dataframe(dados_estado.loc[ dados_estado['date']==dados_estado['date'].max() ].sum())
    dados_estado_melt = pd.melt(
        dados_estado[['date', 'state', 'confirmed', 'deaths']],
        id_vars=['date', 'state'],
        value_vars=['confirmed', 'deaths'])

    df = dados_estado_melt.groupby(["date", 'variable']).sum().reset_index()

    fig = px.line(df, x="date", y="value", color='variable')

    fig.update_layout(title='Covid no Brasil',
                      xaxis_title='Data',
                      yaxis_title='Número de casos')

    df_confirmados = df[ df['variable']=='confirmed']
    df_mortos = df[ df['variable']=='deaths']

    df_confirmados['novo'] = df_confirmados['value'].shift(-1)
    df_confirmados['boo'] = df_confirmados['value'] > df_confirmados['value'].shift(-1)
    df_confirmados['novo3'] =  df_confirmados['novo'] * df_confirmados['boo'] +  \
                               df_confirmados['value'] * ~df_confirmados['boo']




    inconsistente = dias_para_completar.shape[0]>0
    if inconsistente:
        st.info("Alguns municípios ainda não atualizaram os dados e por isso o gráfico pode apresentar diferença no total de casos.")

    st.plotly_chart(fig)

    hoje_estados_indice = hoje_estados
    hoje_estados_indice['estado'] = hoje_estados['state']
    hoje_estados_indice = hoje_estados.set_index(['state'])
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

