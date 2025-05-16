# ---------------------------------------------------------------------------------------------------
# librerias
import pandas as pd
import plotly.express as px
from dash import dcc
# ---------------------------------------------------------------------------------------------------
# cargar la data


# ---------------------------------------------------------------------------------------------------
# funcion principal

def create_pie_chart(load_mortality_data, load_divipola_data):
    df = load_mortality_data
    divipola = load_divipola_data

    # Merge para obtener el nombre del municipio
    df_merge = pd.merge(df, divipola, how='left', on='COD_MUNICIPIO')


    # Agrupar por nombre de municipio y contar muertes
    muertes_ciudades = df_merge.groupby('MUNICIPIO').size().reset_index(name="Total Muertes")

    # Obtener las 10 ciudades con menor número de muertes
    bottom_10 = muertes_ciudades.sort_values(by="Total Muertes", ascending=True).head(10)

    # Gráfico circular
    fig = px.pie(
        bottom_10,
        values="Total Muertes",
        names="MUNICIPIO",
        title="10 Ciudades con Menor Índice de Mortalidad",
        color_discrete_sequence=px.colors.sequential.Blues
    )

    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(title_x=0.5)

    return dcc.Graph(figure=fig,style={"height": "500px", "width": "700px"} )
