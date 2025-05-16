# ---------------------------------------------------------------------------------------------------
# librerias
import pandas as pd
from dash import dcc
from dash import dash_table
import plotly.figure_factory as ff
# ---------------------------------------------------------------------------------------------------
# cargar la data


# ---------------------------------------------------------------------------------------------------
# funcion principal


def create_table_top_causes(load_mortality_data, load_code_death_data):
    df = load_mortality_data
    codes = load_code_death_data

    df['COD_MUERTE'] = df['COD_MUERTE'].str.strip().str.upper()
    codes['Código de la CIE-10 cuatro caracteres'] = codes[
        'Código de la CIE-10 cuatro caracteres'].str.strip().str.upper()

    top_causes = df.groupby('COD_MUERTE').size().reset_index(name='Total Casos')

    merged = pd.merge(
        top_causes,
        codes[['Código de la CIE-10 cuatro caracteres', 'Descripcion  de códigos mortalidad a cuatro caracteres']],
        how='left',
        left_on='COD_MUERTE',
        right_on='Código de la CIE-10 cuatro caracteres'
    )

    merged = merged[['COD_MUERTE', 'Descripcion  de códigos mortalidad a cuatro caracteres', 'Total Casos']]
    merged.columns = ['Código', 'Nombre de la Causa', 'Total de Casos']
    merged = merged.sort_values(by='Total de Casos', ascending=False).head(8)

    return dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in merged.columns],
        data=merged.to_dict('records'),
        style_cell={
            'whiteSpace': 'normal',
            'height': 'auto',
            'textAlign': 'left',
        },
        style_table={'overflowX': 'auto'},
        style_header={
            'backgroundColor': '#2C3E50',
            'color': 'white',
            'fontWeight': 'bold'
        },
        style_data_conditional=[
            {'if': {'row_index': 'odd'}, 'backgroundColor': '#f9f9f9'}
        ]
    )