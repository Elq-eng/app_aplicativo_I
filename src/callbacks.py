# # ---------------------------------------------------------------------------------------------------
# # librerias
import pandas as pd
from dash.dependencies import Input, Output, State
from dash import html, dash
from src.components import mapa, grafico_lineas, grafico_barras, grafico_circular, tabla, histograma, grafico_apiladas
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# # ---------------------------------------------------------------------------------------------------
# # funcion principal
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

            BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            mortality_path = os.path.join(BASE_DIR, "data", "NoFetal2019_8.csv")
            divipola_path = os.path.join(BASE_DIR, "data", "Divipola_8.csv")
            code_death_path = os.path.join(BASE_DIR, "data", "CodigosDeMuerte_8.csv")
            mortality_df = pd.read_csv(mortality_path, sep=';', encoding='utf-8-sig')
            divipola_df = pd.read_csv(divipola_path, sep=';', encoding='utf-8-sig')
            code_death_df = pd.read_csv(code_death_path, sep=';', encoding='utf-8-sig')

            logger.info("Datos cargados y enviados a memoria.")

            logger.info("📊 Len mortality:", len(mortality_data) if mortality_data else "vacío")
            logger.info("📍 Len divipola:", len(divipola_data) if divipola_data else "vacío")
            logger.info("💀 Len code death:", len(code_death_data) if code_death_data else "vacío")

            return (
                mortality_df.to_dict('records'),
                divipola_df.to_dict('records'),
                code_death_df.to_dict('records'),
            )

        except Exception as e:
            print("❌ Error al cargar archivos CSV:", e)
            return dash.no_update, dash.no_update, dash.no_update


    @app.callback(
        Output('tab-content', 'children'),
        Input('tabs', 'value'),
        Input('memory-mortality-data', 'data'),
        Input('memory-divipola-data', 'data'),
        Input('memory-code-death-data', 'data'),
    )
    def render_tab_content(tab, mortality_data, divipola_data, code_death_data):
        # Si la data aún no llegó, mostrar mensaje
        if not mortality_data or not divipola_data or not code_death_data:
            return html.Div("Cargando datos...")

        # Convertir dict a DataFrame
        mortality_df = pd.DataFrame(mortality_data)
        divipola_df = pd.DataFrame(divipola_data)
        code_death_df = pd.DataFrame(code_death_data)

        if tab == 'tab-1':
            return html.Div([
                html.H3("Mapa por Departamento y Evolución Mensual", style={'textAlign': 'center'}),
                html.Div([
                    html.Div(
                        mapa.create_map(mortality_df, divipola_df),
                        style={'display': 'flex', 'justifyContent': 'center'}
                    ),
                    html.Div(
                        grafico_lineas.create_lines(mortality_df),
                        style={'display': 'flex', 'justifyContent': 'center'}
                    ),
                ], style={
                    'display': 'flex',
                    'justifyContent': 'center',
                    'alignItems': 'center',
                    'flexWrap': 'wrap'
                })
            ])
        elif tab == 'tab-2':
            return html.Div([
                html.H3("Las ciudades más violentas y con el menor indice de mortalidad",
                        style={'textAlign': 'center'}),
                                html.Div([
                                    html.Div(
                                        grafico_barras.create_bar_chart(mortality_df, divipola_df),
                                        style={'display': 'flex', 'justifyContent': 'center'}
                                    ),
                                    html.Div(
                                        grafico_circular.create_pie_chart(mortality_df, divipola_df),
                                        style={'display': 'flex', 'justifyContent': 'center'}
                                    ),
                                ], style={
                                    'display': 'flex',
                                    'justifyContent': 'center',
                                    'alignItems': 'center',
                                    'flexWrap': 'wrap'  # Por si el ancho es muy pequeño, los coloca uno debajo del otro
                                })
            ])
        elif tab == 'tab-3':
            return html.Div([

                html.H3(
                    "Listado de las 10 principales causas de muerte en Colombia, Distribución de muertes según rangos de edad y Comparación del total de muertes por sexo",
                        style={'textAlign': 'center'}),
                html.Div([
                    html.Div(
                        tabla.create_table_top_causes(mortality_df, code_death_df),
                        style={'display': 'flex', 'justifyContent': 'center'}
                    ),
                    html.Div(
                        histograma.create_age_histogram(mortality_df),
                        style={'display': 'flex', 'justifyContent': 'center'}
                    ),
                    html.Div(
                        grafico_apiladas.create_stacked_bar_sex_departments(mortality_df, divipola_df),
                        style={'display': 'flex', 'justifyContent': 'center'}
                    )
                ], style={
                    'display': 'flex',
                    'justifyContent': 'center',
                    'alignItems': 'center',
                    'flexWrap': 'wrap'  # Por si el ancho es muy pequeño, los coloca uno debajo del otro
                })
            ])