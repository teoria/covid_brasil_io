import streamlit as st

from municipio import monta_municipios
from estado import monta_estados
from pais import monta_pais


def main():
    st.sidebar.title("Covid 19 - Brasil.io")
    st.sidebar.subheader("Dados por município")
    taxa_mortalidade = st.sidebar.number_input('Taxa de mortalidade mundial em %',value=4.0, step=0.1)
    tipo = st.sidebar.radio("Escolha uma visualização:", ('Municípios', 'Estados', 'Brasil'))

    if tipo == 'Brasil':
        monta_pais(taxa_mortalidade)

    if tipo == "Estados":
        monta_estados(taxa_mortalidade)

    if tipo == "Municípios":
        monta_municipios(taxa_mortalidade)

    st.sidebar.title("Dados")
    st.sidebar.info(
        """
        Os dados utilizados nesta aplicação foram disponibilizados pelo Brasil.io 
        [https://brasil.io/covid19/](https://brasil.io/covid19).
"""
    )

    st.sidebar.title("Autor")
    st.sidebar.info(
        """
        Esta aplicação é mandtida por Rodrigo Carneiro. Mais informações em 
        [linkedin.com/in/rodrigoteoria](https://www.linkedin.com/in/rodrigoteoria).
"""
    )
if __name__ == "__main__":
    main()