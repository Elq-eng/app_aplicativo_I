# ---------------------------------------------------------------------------------------------------
# librerias
import pandas as pd
import plotly.express as px
from dash import dcc


# ---------------------------------------------------------------------------------------------------
# funcion principal
def create_age_histogram(df):
    df = df.copy()

    # Quitar valores nulos
    df = df[df['GRUPO_EDAD1'].notna()]

    # Contar muertes por grupo de edad
    edad_counts = df['GRUPO_EDAD1'].value_counts().sort_index().reset_index()
    edad_counts.columns = ['Rango Edad', 'Total de Muertes']

    # Crear gráfico
    fig = px.bar(
        edad_counts,
        x='Rango Edad',
        y='Total de Muertes',
        title='Distribución de muertes por rangos de edad quinquenales',
        labels={'Rango Edad': 'Rango de Edad', 'Total de Muertes': 'Cantidad de Muertes'},
        template='plotly_white'
    )

    return dcc.Graph(figure=fig, style={"height": "500px", "width": "800px"})