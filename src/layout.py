# ---------------------------------------------------------------------------------------------------
# librerias
from dash import html,dcc
import pandas as pd
from components import mapa,grafico_lineas, grafico_barras, grafico_circular, tabla, histograma,grafico_apiladas

# ---------------------------------------------------------------------------------------------------
# cargar la data

def load_mortality_data():
    df = pd.read_excel("data/NoFetal2019.xlsx")
    return df

def load_divipola_data():
    df = pd.read_excel("data/Divipola.xlsx")
    return df

def load_code_death_data():
    df = pd.read_excel("data/CodigosDeMuerte.xlsx")
    return df


# ---------------------------------------------------------------------------------------------------
# funcion principal
def create_layout(app):
    return html.Div([
        html.H1("Dashboard de Mortalidad en Colombia 2019", style={'textAlign': 'center'}),

        dcc.Tabs([
            dcc.Tab(label="Mapa por Departamento y Evolución Mensual", children=[

                html.H3("Mapa por Departamento y Evolución Mensual", style={'textAlign': 'center'}),
                html.Div([
                    html.Div(
                        mapa.create_map(load_mortality_data, load_divipola_data),
                        style={'display': 'flex', 'justifyContent': 'center'}
                    ),
                    html.Div(
                        grafico_lineas.create_lines(load_mortality_data, load_divipola_data),
                        style={'display': 'flex', 'justifyContent': 'center'}
                    ),
                ], style={
                    'display': 'flex',
                    'justifyContent': 'center',
                    'alignItems': 'center',
                    'flexWrap': 'wrap'  # Por si el ancho es muy pequeño, los coloca uno debajo del otro
                })

            ]),
            dcc.Tab(label="Las ciudades más violentas y con el menor indice de mortalidad", children=[
                html.H3("Las ciudades más violentas y con el menor indice de mortalidad", style={'textAlign': 'center'}),
                html.Div([
                    html.Div(
                        grafico_barras.create_bar_chart(load_mortality_data(), load_divipola_data()),
                        style={'display': 'flex', 'justifyContent': 'center'}
                    ),
                    html.Div(
                        grafico_circular.create_pie_chart(load_mortality_data(), load_divipola_data()),
                        style={'display': 'flex', 'justifyContent': 'center'}
                    ),
                ], style={
                    'display': 'flex',
                    'justifyContent': 'center',
                    'alignItems': 'center',
                    'flexWrap': 'wrap'  # Por si el ancho es muy pequeño, los coloca uno debajo del otro
                })
            ]),
            dcc.Tab(label="Listado de las 10 principales causas de muerte en Colombia, Distribución de muertes según rangos de edad y Comparación del total de muertes por sexo", children=[
                html.H3("Listado de las 10 principales causas de muerte en Colombia, Distribución de muertes según rangos de edad y Comparación del total de muertes por sexo",
                        style={'textAlign': 'center'}),
                html.Div([
                    html.Div(
                        tabla.create_table_top_causes(load_mortality_data(), load_code_death_data()),
                        style={'display': 'flex', 'justifyContent': 'center'}
                    ),
                    html.Div(
                        histograma.create_age_histogram(load_mortality_data()),
                        style={'display': 'flex', 'justifyContent': 'center'}
                    ),
                    html.Div(
                        grafico_apiladas.create_stacked_bar_sex_departments(load_mortality_data(), load_divipola_data()),
                        style={'display': 'flex', 'justifyContent': 'center'}
                    )
                ], style={
                    'display': 'flex',
                    'justifyContent': 'center',
                    'alignItems': 'center',
                    'flexWrap': 'wrap'  # Por si el ancho es muy pequeño, los coloca uno debajo del otro
                })
            ]),
        ])
    ])