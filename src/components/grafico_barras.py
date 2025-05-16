# ---------------------------------------------------------------------------------------------------
# librerias
import pandas as pd
import plotly.express as px
from dash import dcc
# ---------------------------------------------------------------------------------------------------
# cargar la data


# ---------------------------------------------------------------------------------------------------
# funcion principal

def create_bar_chart(load_mortality_data, load_divipola_data):
    df = load_mortality_data
    divipola = load_divipola_data

    # Filtrar por homicidios (código X95)
    df['COD_MUERTE'] = df['COD_MUERTE'].astype(str).str.strip().str.upper()
    df_homicidios = df[df['COD_MUERTE'].str.startswith('X95')]

    # Unir con la tabla de divipola para obtener nombres completos (ciudades o departamentos)
    df_merge = pd.merge(df_homicidios, divipola, how="left", on="COD_MUNICIPIO")

    # Agrupar por ciudad o municipio (ajusta a la columna correcta si no es 'CIUDAD')
    top_cities = df_merge.groupby("MUNICIPIO").size().reset_index(name="Total Homicidios")

    # Obtener top 5
    top_5 = top_cities.sort_values(by="Total Homicidios", ascending=False).head(5)

    # Crear gráfico de barras
    fig = px.bar(
        top_5,
        x="MUNICIPIO",
        y="Total Homicidios",
        title="Top 5 Ciudades más Violentas (Homicidios - Código X95)",
        color="Total Homicidios",
        text="Total Homicidios",
        color_continuous_scale="Reds"
    )

    fig.update_layout(
        xaxis_title="Ciudad",
        yaxis_title="Cantidad de Homicidios",
        title_x=0.5,
        margin={"r": 0, "t": 40, "l": 0, "b": 0}
    )

    return dcc.Graph(figure=fig,style={"height": "500px", "width": "700px"} )
