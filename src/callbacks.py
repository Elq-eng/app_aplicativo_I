# ---------------------------------------------------------------------------------------------------
# Librerías
import pandas as pd
import os
from dash.dependencies import Input, Output, State
from dash import html, dash
from src.components import mapa, grafico_lineas, grafico_barras, grafico_circular, tabla, histograma, grafico_apiladas

# ---------------------------------------------------------------------------------------------------
# Rutas absolutas para los archivos de datos
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(BASE_DIR, "data")

# ---------------------------------------------------------------------------------------------------
# Función principal de callbacks
def register_callbacks(app):

    @app.callback(
        Output('memory-mortality-data', 'data'),
        Output('memory-divipola-data', 'data'),
        Output('memory-code-death-data', 'data'),
        Input('tabs', 'value'),
        State('memory-mortality-data', 'data'),
        State('memory-divipola-data', 'data'),
        State('memory-code-death-data', 'data'),
    )
    def load_data_on_demand(tab, mortality_data, divipola_data, code_death_data):
        if mortality_data and divipola_data and code_death_data:
            return mortality_data, divipola_data, code_death_data

        try:
            # Rutas completas seguras
            mortality_path = os.path.join(DATA_DIR, "NoFetal2019_8.csv")
            divipola_path = os.path.join(DATA_DIR, "Divipola_8.csv")
            code_death_path = os.path.join(DATA_DIR, "CodigosDeMuerte_8.csv")

            # Leer CSVs
            mortality_df = pd.read_csv(mortality_path, sep=';', encoding='utf-8')
            divipola_df = pd.read_csv(divipola_path, sep=';', encoding='utf-8')
            code_death_df = pd.read_csv(code_death_path, sep=';', encoding='utf-8')

            print("✅ Datos cargados correctamente.")
            return (
                mortality_df.to_dict('records'),
                divipola_df.to_dict('records'),
                code_death_df.to_dict('records'),
            )

        except Exception as e:
            print("❌ Error al cargar archivos CSV:", e)
            # Devolver vacío para evitar que el callback se quede colgado
            return [], [], []

    # ---------------------------------------------------------------------------------------------------
    @app.callback(
        Output('tab-content', 'children'),
        Input('tabs', 'value'),
        Input('memory-mortality-data', 'data'),
        Input('memory-divipola-data', 'data'),
        Input('memory-code-death-data', 'data'),
    )
    def render_tab_content(tab, mortality_data, divipola_data, code_death_data):
        if not mortality_data or not divipola_data or not code_death_data:
            return html.Div("Cargando datos...")

        # Convertir a DataFrames
        try:
            mortality_df = pd.DataFrame(mortality_data)
            divipola_df = pd.DataFrame(divipola_data)
            code_death_df = pd.DataFrame(code_death_data)
        except Exception as e:
            print("❌ Error al convertir datos a DataFrame:", e)
            return html.Div("Error al procesar los datos.")

        if tab == 'tab-1':
            return html.Div([
                html.H3("Mapa por Departamento y Evolución Mensual", style={'textAlign': 'center'}),
                html.Div([
                    html.Div(mapa.create_map(mortality_df, divipola_df),
                             style={'display': 'flex', 'justifyContent': 'center'}),
                    html.Div(grafico_lineas.create_lines(mortality_df),
                             style={'display': 'flex', 'justifyContent': 'center'}),
                ], style={
                    'display': 'flex',
                    'justifyContent': 'center',
                    'alignItems': 'center',
                    'flexWrap': 'wrap'
                })
            ])

        elif tab == 'tab-2':
            return html.Div([
                html.H3("Las ciudades más violentas y con el menor índice de mortalidad",
                        style={'textAlign': 'center'}),
                html.Div([
                    html.Div(grafico_barras.create_bar_chart(mortality_df, divipola_df),
                             style={'display': 'flex', 'justifyContent': 'center'}),
                    html.Div(grafico_circular.create_pie_chart(mortality_df, divipola_df),
                             style={'display': 'flex', 'justifyContent': 'center'}),
                ], style={
                    'display': 'flex',
                    'justifyContent': 'center',
                    'alignItems': 'center',
                    'flexWrap': 'wrap'
                })
            ])

        elif tab == 'tab-3':
            return html.Div([
                html.H3("Top 10 causas de muerte, distribución por edad y sexo",
                        style={'textAlign': 'center'}),
                html.Div([
                    html.Div(tabla.create_table_top_causes(mortality_df, code_death_df),
                             style={'display': 'flex', 'justifyContent': 'center'}),
                    html.Div(histograma.create_age_histogram(mortality_df),
                             style={'display': 'flex', 'justifyContent': 'center'}),
                    html.Div(grafico_apiladas.create_stacked_bar_sex_departments(mortality_df, divipola_df),
                             style={'display': 'flex', 'justifyContent': 'center'}),
                ], style={
                    'display': 'flex',
                    'justifyContent': 'center',
                    'alignItems': 'center',
                    'flexWrap': 'wrap'
                })
            ])

        else:
            return html.Div("Tab no válida seleccionada.")
