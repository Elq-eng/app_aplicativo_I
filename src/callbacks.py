import pandas as pd
from dash.dependencies import Input, Output
from dash import html
from src.components import mapa, grafico_lineas, grafico_barras, grafico_circular, tabla, histograma, grafico_apiladas

def register_callbacks(app):

    @app.callback(
        Output('tab-content', 'children'),
        Input('tabs', 'value'),
        Input('memory-mortality-data', 'data'),
        Input('memory-divipola-data', 'data'),
        Input('memory-code-death-data', 'data'),
    )
    def render_tab_content(tab, mortality_data, divipola_data, code_death_data):
        print("📦 Tab actual:", tab)
        print("📊 Len mortality:", len(mortality_data) if mortality_data else "vacío")
        print("📍 Len divipola:", len(divipola_data) if divipola_data else "vacío")
        print("💀 Len code death:", len(code_death_data) if code_death_data else "vacío")

        if not mortality_data or not divipola_data or not code_death_data:
            return html.Div("Cargando datos...")

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
