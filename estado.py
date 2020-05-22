import streamlit as st
import pandas as pd
import json
import plotly.express as px
import requests
import folium


import plotly.graph_objects as go
from config_data import load_data_brasil_io, get_map_state, get_map_city , get_view
import pydeck as pdk


def get_color(f):
    st.write(f)
    return  [0,0,0]


def monta_estados(taxa_mortalidade):
    df = load_data_brasil_io()
    states = df['state'].sort_values(ascending=True).unique()
    if states is not None:
        state = st.sidebar.selectbox('Qual o estado você deseja visualizar?', states)

        dados_estado =df[(df['state'] == state)&(df['place_type']=='state')]
        dados_estado_cities =df[(df['state'] == state)&(df['place_type'] != 'state')]

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

        data_state = get_map_state(state)
        data_cities = get_map_city(state)
        view = get_view(state)

        slide =  st.slider('Semana epidemiológica', 0, 255, 1 )

        dia_atual_mapa = dados_estado_cities[dados_estado_cities.is_last==True]

        st.write(  dia_atual_mapa)
        for feature in data_cities['features']:
            id_city = feature['id']
            dados =dia_atual_mapa[dia_atual_mapa.city_ibge_code == id_city].reset_index().T.rename(columns={0: 'dados'})
            feature['properties'] = dados.to_dict()

        # m = folium.Map(location=[45.5236, -122.6750])
        # html = m.get_root().render()
        # st.markdown(html.encode('utf8'),False)
        #st.write(data_cities)
        # Set the viewport location
        view_state = pdk.ViewState(
            longitude=view[1],
            latitude=view[0],
            zoom=6,
            min_zoom=1,
            max_zoom=60,
            pitch=50,#40.5,
            bearing=0)#-27.36

        geojson = pdk.Layer(
            'GeoJsonLayer',
            data_state,
            opacity=1,
            #stroked=False,
            filled=True,
            #extruded=True,
            #wireframe=True,
            get_fill_color=[255,  255, 255],
            get_line_color=[100, 100, 90],
            #pickable=True
        )

        geojson2 = pdk.Layer(
            'GeoJsonLayer',
            data_cities,
            opacity=0.8,
            stroked=False,
            filled=True,
            extruded=True,
            wireframe=True,
            get_elevation='properties.dados.deaths*1000',
            get_fill_color='[255/2, properties.dados.confirmed  , 255]',
            get_line_color=[0, slide, 255],
            pickable=True
        )
        max_val=1000
        min_val=0

        # Combined all of it and render a viewport
        r = pdk.Deck(layers=[geojson,geojson2],
                     tooltip={"html": f"<b>Color Value:</b> {state}", "style": {"color": "white"}},

                     initial_view_state=view_state,
                     height=800,
                     width=800,
                     map_style="mapbox://styles/mapbox/light-v9",
                     mapbox_key='pk.eyJ1IjoidGVvcmlhIiwiYSI6ImNqODRpNWJrNjA5dGIyd3FoMnZ6am13NjcifQ.OgxGf081lfoKQAOhlYh1Tg'
                     )
        st.pydeck_chart(r)

        dados_estado_melt = pd.melt(
            dados_estado[['date', 'confirmed', 'deaths']],
            id_vars=['date'],
            value_vars=['confirmed', 'deaths'])

        df = dados_estado_melt.groupby(["date", 'variable']).sum().reset_index()

        fig = px.line(df, x="date", y="value", color='variable')

        fig.update_layout(title=f'Casos de Covid em {state}',
                          xaxis_title='Data',
                          yaxis_title='Número de casos')
        st.plotly_chart(fig)
#
# """This app demonstrates the use of the awesome [deck.gl]() framework for visual
# exploratory data analysis of large datasets.
#
# Deck.gl is now (as of Streamlit v. 0.53) supported via the
# [`st.pydeck_chart`](https://docs.streamlit.io/api.html?highlight=pydeck#streamlit.pydeck_chart)
# function.
#
# We use data from the
# [Global Power Plant Database](http://datasets.wri.org/dataset/globalpowerplantdatabase) to
# illustrate the locations, fuel types and capacities of the worlds power plants.
# """
#
#
# import pathlib
#
# import pandas as pd
# import pydeck as pdk
# import streamlit as st
#
# POWER_PLANT_PATH = (
#     pathlib.Path.cwd() / "gallery/global_power_plant_database/global_power_plant_database.csv"
# )
#
# POWER_PLANT_URL = (
#     "https://raw.githubusercontent.com/MarcSkovMadsen/awesome-streamlit/master/"
#     "gallery/global_power_plant_database/global_power_plant_database.csv"
# )
#
# LATITUDE_COLUMN = "latitude"
# LONGITUDE_COLUMN = "longitude"
#
# LOCATIONS = {
#     "Orsted Copenhagen HQ": {"latitude": 55.676098, "longitude": 12.568337},
#     "Orsted Boston": {"latitude": 2.361145, "longitude": -71.057083},
# }
# ORSTED_CPH_HQ = LOCATIONS["Orsted Copenhagen HQ"]
#
# FUEL_COLORS = {
#     "Oil": "black",
#     "Solar": "green",
#     "Gas": "black",
#     "Other": "gray",
#     "Hydro": "blue",
#     "Coal": "black",
#     "Petcoke": "black",
#     "Biomass": "green",
#     "Waste": "green",
#     "Cogeneration": "gray",
#     "Storage": "orange",
#     "Wind": "green",
# }
#
# COLORS_R = {"black": 0, "green": 0, "blue": 0, "orange": 255, "gray": 128}
#
# COLORS_G = {"black": 0, "green": 128, "blue": 0, "orange": 165, "gray": 128}
#
# COLORS_B = {"black": 0, "green": 0, "blue": 255, "orange": 0, "gray": 128}
#
#
# class ViewStateComponent:
#     """Component to let the user set the initial view state to for example Copenhagen or Boston"""
#
#     def __init__(self):
#         self.latitude = ORSTED_CPH_HQ["latitude"]
#         self.longitude = ORSTED_CPH_HQ["longitude"]
#         self.zoom = 1
#         self.pitch = 40.0
#
#     def edit_view(self):
#         """Lets the user edit the attributes"""
#         location = st.sidebar.selectbox("Location", options=list(LOCATIONS.keys()), index=0)
#         self.latitude = LOCATIONS[location]["latitude"]
#         self.longitude = LOCATIONS[location]["longitude"]
#
#         self.zoom = st.sidebar.slider("Zoom", min_value=0, max_value=20, value=self.zoom)
#         self.pitch = st.sidebar.slider(
#             "Pitch", min_value=0.0, max_value=100.0, value=self.pitch, step=10.0
#         )
#
#     @property
#     def view_state(self) -> pdk.ViewState:
#         """The ViewState according to the attributes
#
#         Returns:
#             pdk.ViewState -- [description]
#         """
#         return pdk.ViewState(
#             longitude=self.longitude,
#             latitude=self.latitude,
#             zoom=self.zoom,
#             min_zoom=0,
#             max_zoom=15,
#             pitch=self.pitch,
#             # bearing=-27.36,
#         )
#
#
# class GlobalPowerPlantDatabaseApp:
#     """The main app showing the Global Power Plant Database"""
#
#     def __init__(self):
#         self.view_state_component = ViewStateComponent()
#         self.data = self.get_data()
#         self.show_data = False
#
#     @staticmethod
#     @st.cache
#     def get_data() -> pd.DataFrame:
#         """The Global Power Plant data
#
#         Returns:
#             pd.DataFrame -- The Global Power Plant data cleaned and transformed
#         """
#         try:
#             data = pd.read_csv(POWER_PLANT_PATH)
#         except FileNotFoundError:
#             data = pd.read_csv(POWER_PLANT_URL)
#
#         # Clean
#         data.primary_fuel = data.primary_fuel.fillna("NA")
#         data.capacity_mw = data.capacity_mw.fillna(1)
#
#         # Transform
#         data["primary_fuel_color"] = data.primary_fuel.map(FUEL_COLORS)
#         data["primary_fuel_color"] = data["primary_fuel_color"].fillna("gray")
#         data["color_r"] = data["primary_fuel_color"].map(COLORS_R)
#         data["color_g"] = data["primary_fuel_color"].map(COLORS_G)
#         data["color_b"] = data["primary_fuel_color"].map(COLORS_B)
#         data["color_a"] = 140
#
#         return data[
#             [
#                 "capacity_mw",
#                 LATITUDE_COLUMN,
#                 LONGITUDE_COLUMN,
#                 "primary_fuel_color",
#                 "color_r",
#                 "color_g",
#                 "color_b",
#                 "color_a",
#             ]
#         ]
#
#     def _scatter_plotter_layer(self):
#         return pdk.Layer(
#             "ScatterplotLayer",
#             data=self.data,
#             get_position=[LONGITUDE_COLUMN, LATITUDE_COLUMN],
#             get_fill_color="[color_r, color_g, color_b, color_a]",
#             get_radius="capacity_mw*10",
#             pickable=True,
#             opacity=0.8,
#             stroked=False,
#             filled=True,
#             wireframe=True,
#         )
#
#     def _deck(self):
#         return pdk.Deck(
#             map_style="mapbox://styles/mapbox/light-v9",
#             initial_view_state=self.view_state_component.view_state,
#             layers=[self._scatter_plotter_layer()],
#             tooltip={"html": "<b>Color Value:</b> {primary_fuel}", "style": {"color": "white"}},
#         )
#
#     def view(self):
#         """Main view of the app"""
#         # self.view_state_component.edit_view() # Does not work
#         st.write(__doc__)
#
#         st.pydeck_chart(self._deck())
#
#         st.write(
#             """The maps shows the power plant
#
# - **location** by latitude, longitude coordinates
# - **fuel type** by color and
# - **capacity in MW** by bubble size
# """
#         )
#         st.json(FUEL_COLORS)
#
#         st.write(
#             """Unfortunately **tooltips are not supported**. And there are also other issues.
# See
#
# - [Issue 984](https://github.com/streamlit/streamlit/issues/984)
# - [Issue 985](https://github.com/streamlit/streamlit/issues/985)"""
#         )
#
#
# APP = GlobalPowerPlantDatabaseApp()
# APP.view()