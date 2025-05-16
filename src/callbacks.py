import pandas as pd
from dash.dependencies import Input, Output, State
from dash import html
from src.components import mapa, grafico_lineas, grafico_barras, grafico_circular, tabla, histograma, grafico_apiladas

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
        # Si ya está cargada la data, no la cargamos otra vez
        if mortality_data and divipola_data and code_death_data:
            return mortality_data, divipola_data, code_death_data

        # Cargar data
        mortality_df = pd.read_excel("data/NoFetal2019.xlsx")
        divipola_df = pd.read_excel("data/Divipola.xlsx")
        code_death_df = pd.read_excel("data/CodigosDeMuerte.xlsx")

        # Convertir a dict para almacenamiento en dcc.Store
        return mortality_df.to_dict('records'), divipola_df.to_dict('records'), code_death_df.to_dict('records')


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
                mapa.create_map(mortality_df, divipola_df),
                grafico_lineas.create_lines(mortality_df, divipola_df),
            ])
        elif tab == 'tab-2':
            return html.Div([
                grafico_barras.create_bar_chart(mortality_df, divipola_df),
                grafico_circular.create_pie_chart(mortality_df, divipola_df),
            ])
        elif tab == 'tab-3':
            return html.Div([
                tabla.create_table_top_causes(mortality_df, code_death_df),
                histograma.create_age_histogram(mortality_df),
                grafico_apiladas.create_stacked_bar_sex_departments(mortality_df, divipola_df),
            ])