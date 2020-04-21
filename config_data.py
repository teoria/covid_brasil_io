import streamlit as st
import pandas as pd

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
