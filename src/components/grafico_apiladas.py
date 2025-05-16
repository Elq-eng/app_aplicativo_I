# ---------------------------------------------------------------------------------------------------
# librerias
import pandas as pd
import plotly.express as px
from dash import dcc


# ---------------------------------------------------------------------------------------------------
# funcion principal
def create_stacked_bar_sex_departments(load_mortality_data, load_divipola_data):
    df = load_mortality_data
    divipola = load_divipola_data

    # Asegurar que los códigos sean del mismo tipo
    df['COD_DEPARTAMENTO'] = df['COD_DEPARTAMENTO'].astype(str)
    divipola['COD_DEPARTAMENTO'] = divipola['COD_DEPARTAMENTO'].astype(str)

    # Hacer merge con divipola para obtener el nombre del departamento
    df = pd.merge(df, divipola, on="COD_DEPARTAMENTO", how="left")

    # Verificar si la columna del nombre se llama así, si no, actualiza este nombre
    if 'DEPARTAMENTO' in df.columns:
        nombre_col = 'DEPARTAMENTO'
    else:
        nombre_col = df.columns[-1]  # última columna como nombre del departamento si no lo identificamos

    # Agrupar por departamento y sexo
    grouped = df.groupby([nombre_col, 'SEXO']).size().reset_index(name="Total Muertes")

    # Crear gráfico de barras apiladas
    fig = px.bar(
        grouped,
        x=nombre_col,
        y="Total Muertes",
        color="SEXO",
        title="Comparación de muertes por sexo en cada departamento",
        labels={"SEXO": "Sexo", "Total Muertes": "Cantidad de Muertes"},
        barmode="stack"
    )

    fig.update_layout(
        xaxis_title="Departamento",
        yaxis_title="Cantidad de Muertes",
        title_x=0.5,
        xaxis={'categoryorder': 'total descending'},
        margin={"r": 0, "t": 30, "l": 0, "b": 100}
    )

    return dcc.Graph(figure=fig, style={"height": "600px", "width": "100%"})