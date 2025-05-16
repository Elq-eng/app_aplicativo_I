# ---------------------------------------------------------------------------------------------------
# librerias
import pandas as pd
import plotly.express as px
from dash import dcc
# ---------------------------------------------------------------------------------------------------
# cargar la data


coord_departamentos = {
    "AMAZONAS": {"lat": -1.4436, "lon": -71.5724},
    "ANTIOQUIA": {"lat": 6.5790, "lon": -75.4740},
    "ARAUCA": {"lat": 7.0292, "lon": -70.7591},
    "ATLÁNTICO": {"lat": 10.6966, "lon": -74.8741},
    "BARRANQUILLA D.E.": {"lat": 10.6966, "lon": -74.8741},
    "BOLÍVAR": {"lat": 9.2312, "lon": -74.6780},
    "CARTAGENA D.T. Y C.": {"lat": 9.2312, "lon": -74.6780},
    "BOYACÁ": {"lat": 5.4545, "lon": -73.3620},
    "CALDAS": {"lat": 5.2983, "lon": -75.2479},
    "CAQUETÁ": {"lat": 0.8699, "lon": -73.8419},
    "CASANARE": {"lat": 5.7589, "lon": -71.5720},
    "CAUCA": {"lat": 2.7089, "lon": -76.6102},
    "CESAR": {"lat": 9.3373, "lon": -73.6536},
    "CHOCÓ": {"lat": 5.6642, "lon": -76.8732},
    "BUENAVENTURA D.E.": {"lat": 5.6642, "lon": -76.8732},
    "CÓRDOBA": {"lat": 8.4016, "lon": -75.8000},
    "CUNDINAMARCA": {"lat": 4.6813, "lon": -74.1070},
    "BOGOTÁ, D.C.": {"lat": 4.6813, "lon": -74.1070},
    "GUAINÍA": {"lat": 2.5854, "lon": -69.0000},
    "GUAVIARE": {"lat": 2.0000, "lon": -72.5000},
    "HUILA": {"lat": 2.5359, "lon": -75.5277},
    "LA GUAJIRA": {"lat": 11.3548, "lon": -72.5200},
    "MAGDALENA": {"lat": 10.5085, "lon": -74.2168},
    "SANTA MARTA D.T. Y C.": {"lat": 10.5085, "lon": -74.2168},
    "META": {"lat": 3.4984, "lon": -73.5560},
    "NARIÑO": {"lat": 1.2892, "lon": -77.3579},
    "NORTE DE SANTANDER": {"lat": 8.0836, "lon": -72.6369},
    "PUTUMAYO": {"lat": 0.5703, "lon": -76.2943},
    "QUINDÍO": {"lat": 4.4610, "lon": -75.6674},
    "RISARALDA": {"lat": 5.3158, "lon": -75.9921},
    "ARCHIPIÉLAGO DE SAN ANDRÉS, PROVIDENCIA Y SANTA CATALINA": {"lat": 12.5567, "lon": -81.7185},
    "SANTANDER": {"lat": 7.1254, "lon": -73.1198},
    "SUCRE": {"lat": 9.3047, "lon": -75.3978},
    "TOLIMA": {"lat": 4.4389, "lon": -75.2327},
    "VALLE DEL CAUCA": {"lat": 3.8009, "lon": -76.6413},
    "VAUPÉS": {"lat": 0.8550, "lon": -70.8120},
    "VICHADA": {"lat": 5.3196, "lon": -69.5784}
}


# ---------------------------------------------------------------------------------------------------
# funcion principal

def create_map(load_mortality_data,load_divipola_data):
    df = load_mortality_data
    divipola = load_divipola_data

    # Agrupar cantidad de muertes por código de departamento
    df_grouped = df.groupby("COD_DEPARTAMENTO").size().reset_index(name="MUERTES")

    # Agregar coordenadas al dataframe divipola
    divipola["lat"] = divipola["DEPARTAMENTO"].str.upper().map(lambda d: coord_departamentos.get(d, {}).get("lat"))
    divipola["lon"] = divipola["DEPARTAMENTO"].str.upper().map(lambda d: coord_departamentos.get(d, {}).get("lon"))

    # Unir mortalidad con info de coordenadas
    df_merged = pd.merge(df_grouped, divipola, how="left", on="COD_DEPARTAMENTO")


    # Crear visualización tipo scatter_geo
    fig = px.scatter_geo(
        df_merged,
        lat="lat",
        lon="lon",
        size="MUERTES",
        size_max=30,
        color="MUERTES",
        hover_name="DEPARTAMENTO",
        color_continuous_scale="Reds",
        projection="natural earth",
        title="Muertes Totales por Departamento en Colombia (2019)"
    )

    fig.update_geos(fitbounds="locations", visible=True,scope="south america")
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})

    return dcc.Graph(figure=fig,style={"height": "500px", "width": "700px"} )