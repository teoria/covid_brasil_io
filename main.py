import streamlit as st
import pandas as pd
import numpy as np

#import plotly.express as px

@st.cache
def load_data_brasil_io():
    DATA_URL = 'data/covid19-5ed77dfe94aa409eb8c10d54be0ea2f2.csv'
    DATE_COLUMN = 'date'
    data = pd.read_csv(DATA_URL)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


def get_estado(df, state, city):
    dados_estado = df.loc[(df['state'] == state) & (df['city'] == city)]
    return dados_estado

def monta_pais():
    df = load_data_brasil_io()

    dados_estado = df[ (df['place_type'] == 'state')]

    st.subheader(f"Dados de COVID no Brasil")

    dados_estado_plot = dados_estado.groupby('date').sum()
    hoje = dados_estado[dados_estado['is_last']].sum()
    dados_estado_plot = dados_estado_plot[:dados_estado_plot.shape[0]-1]
    #st.write(dados_estado_plot)
    dia_atual = 1#dados_estado_plot.first_valid_index#['date'].dt.strftime('%d-%m-%Y')[0]

    confirmados = hoje.loc['confirmed']
    mortes = hoje.loc['deaths']
    taxa = round(mortes/confirmados * 10000)/100

    st.markdown(f"O Brasil teve até o dia **{dia_atual}** "
                f"um total de **{confirmados}** casos confirmados e"
                f" **{mortes}** mortes com uma taxa de mortalidade de **{taxa}%**.")

    st.line_chart(dados_estado_plot[['confirmed','deaths']])


def monta_estados():
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
        taxa = round(hoje['death_rate'][0] * 10000) / 100

        st.markdown(f"O estado de **{state}** teve até o dia **{dia_atual}** "
                    f"um total de **{confirmados}** casos confirmados e"
                    f" **{mortes}** mortes com uma taxa de mortalidade de **{taxa}%**.")

        st.line_chart(dados_estado_plot)


def monta_municipios():
    df = load_data_brasil_io()
    states = df['state'].sort_values(ascending=True).unique()
    if states is not None:
        state = st.sidebar.selectbox('Qual o estado você deseja visualizar?', states)
        # st.write('You selected:', state)
        cities = df[df['state'] == state]['city'].unique()
        city = st.sidebar.selectbox('Qual a cidade você deseja visualizar?', cities)
        dados_estado = get_estado(df, state, city)

        st.subheader(f"Dados de COVID em {city}")

        # number = st.slider("numero de linhas do header", min_value=1, max_value=10)
        # st.table(dados_estado.head(number))
        dados_estado_plot = dados_estado[['date', 'confirmed', 'deaths']].sort_values(by=['date'], ascending=True)
        dados_estado_plot.reset_index(drop=True, inplace=True)
        dados_estado_plot.set_index(['date'], inplace=True)

        hoje = dados_estado[dados_estado['is_last']]
        hoje.reset_index(drop=True, inplace=True)
        # st.table(hoje)
        dia_atual = hoje['date'].dt.strftime('%d-%m-%Y')[0]
        # st.write( dia_atual)

        confirmados = hoje['confirmed'][0]
        mortes = hoje['deaths'][0]
        taxa = round(hoje['death_rate'][0] * 10000) / 100

        st.markdown(f"O município de **{city}** em **{state}** teve até o dia **{dia_atual}** "
                    f"um total de **{confirmados}** casos confirmados e"
                    f" **{mortes}** mortes com uma taxa de mortalidade de **{taxa}%**.")

        st.line_chart(dados_estado_plot)


def main():
    st.sidebar.title("Covid 19 - Brasil.io")
    st.sidebar.subheader("Dados por município")

    tipo = st.sidebar.radio(
    "Escolha uma visualização:",
    ( 'Municípios', 'Estados','Brasil'))

    if tipo == 'Brasil':
        monta_pais()

    if tipo == "Estados":
        monta_estados()

    if tipo == "Municípios":
        monta_municipios()

def main_map():

    st.title('Uber pickups in NYC')

    DATE_COLUMN = 'date/time'
    DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
                'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

    @st.cache
    def load_data(nrows):
        data = pd.read_csv(DATA_URL, nrows=nrows)
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis='columns', inplace=True)
        data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
        return data

    data_load_state = st.text('Loading data...')
    data = load_data(10000)
    data_load_state.text('Loading data... done!')

    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(data)

    st.subheader('Number of pickups by hour')
    hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
    st.bar_chart(hist_values)


    #st.plotly_chart(f)

    # Some number in the range 0-23
    hour_to_filter = st.slider('hour', 0, 23, 17)
    filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

    st.subheader('Map of all pickups at %s:00' % hour_to_filter)
    st.map(filtered_data)

if __name__ == "__main__":
    main()