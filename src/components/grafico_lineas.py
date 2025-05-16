# ---------------------------------------------------------------------------------------------------
# librerias
import pandas as pd
import plotly.express as px
from dash import dcc

# ---------------------------------------------------------------------------------------------------
# data
meses = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
        5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
        9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }

# ---------------------------------------------------------------------------------------------------
# funcion principal

def create_lines(load_mortality_data,load_divipola_data):
    df = load_mortality_data()

    muertes_por_mes = df.groupby("MES").size().reset_index(name="MUERTES")

    muertes_por_mes = muertes_por_mes.sort_values("MES")

    muertes_por_mes["MES"] = muertes_por_mes["MES"].map(meses)

    # Crear gráfico de líneas
    fig = px.line(
        muertes_por_mes,
        x="MES",
        y="MUERTES",
        markers=True,
        title="Muertes Totales por Mes en Colombia (2019)",
        labels={"MES": "Mes", "MUERTES": "Total de Muertes"}
    )

    fig.update_layout(
        xaxis=dict(tickmode="linear"),
        margin={"r": 10, "t": 40, "l": 10, "b": 40}
    )

    return dcc.Graph(
        figure=fig,
        style={"height": "400px", "width": "700px"}
    )
