import streamlit as st
import pandas as pd
import requests


@st.cache
def load_data_brasil_io():
    DATA_URL = 'data/covid19-5ed77dfe94aa409eb8c10d54be0ea2f2.csv'
    DATA_URL=  'https://brasil.io/dataset/covid19/caso/?format=csv'
    DATE_COLUMN = 'date'
    data = pd.read_csv(DATA_URL)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


@st.cache
def get_map_state(state):
    url = f'https://brasil.io/covid19/states/geo/?state={state}'
    json_file = requests.get(url)
    data = json_file.json()
    return data


@st.cache(allow_output_mutation=True)
def get_map_city(state):
    url = f'https://brasil.io/covid19/cities/geo/?state={state}'
    json_file = requests.get(url)
    data = json_file.json()
    return data

@st.cache
def get_view(state):
    states = {
        "AC":(-9.1247779,-71.4250386), 
        "AL": (),
        "AM": (),
        "AP": (),
        "BA": (),
        "CE": (),
        "DF": (),
        "ES": (),
        "GO": (),
        "MA": (),
        "MG": (),
        "MS": (),
        "MT": (),
        "PA": (),
        "PB": (),
        "PE": (),
        "PI": (),
        "PR": (),
        "RJ": (),
        "RN": (),
        "RO": (),
        "RR": (),
        "RS": (),
        "SC": (),
        "SE": (),
        "SP": (),
        "TO": ()

    }
    data = states.get(state)
    return data
