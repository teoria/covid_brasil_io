import streamlit as st
import pandas as pd

import plotly.express as px

import plotly.graph_objects as go
from config_data import load_data_brasil_io


def monta_estados(taxa_mortalidade):
    df = load_data_brasil_io()
    states = df['state'].sort_values(ascending=True).unique()
    if states is not None:
        state = st.sidebar.selectbox('Qual o estado você deseja visualizar?', states)

        dados_estado =df[(df['state'] == state)&(df['place_type']=='state')]

        st.subheader(f"Dados de COVID em {state}")


        dados_estado_plot = dados_estado[['date', 'confirmed', 'deaths']].sort_values(by=['date'], ascending=True)
        dados_estado_plot.reset_index(drop=True, inplace=True)
        dados_estado_plot.set_index(['date'], inplace=True)

        hoje = dados_estado[dados_estado['is_last']]
        hoje.reset_index(drop=True, inplace=True)
        dia_atual = hoje['date'].dt.strftime('%d-%m-%Y')[0]

        confirmados = hoje['confirmed'][0]
        mortes = hoje['deaths'][0]
        quantidade_estimada = (100 * mortes / taxa_mortalidade).astype(int)
        taxa = round(hoje['death_rate'][0] * 10000) / 100

        st.markdown(f"O estado de **{state}** teve até o dia **{dia_atual}** "
                    f"um total de **{confirmados}** casos confirmados e"
                    f" **{mortes}** mortes com uma taxa de mortalidade de **{taxa}%**.")
        if mortes > 0:
            st.markdown(f"Com base na taxa de mortalidade de outros países (**{taxa_mortalidade}%** dos infectados) "
                    f"a quantidade estimada de infectados seria de **{quantidade_estimada}** para a quantidade de mortos atual.")

        #st.line_chart(dados_estado_plot)

        dados_estado_melt = pd.melt(
            dados_estado[['date',  'confirmed', 'deaths']],
            id_vars=['date' ],
            value_vars=['confirmed', 'deaths'])

        df = dados_estado_melt.groupby(["date", 'variable']).sum().reset_index()

        fig = px.line(df, x="date", y="value", color='variable')

        fig.update_layout(title=f'Casos de Covid em {state}',
                          xaxis_title='Data',
                          yaxis_title='Número de casos')
        st.plotly_chart(fig)

