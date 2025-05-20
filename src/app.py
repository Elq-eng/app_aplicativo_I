# ---------------------------------------------------------------------------------------------------
# librerias
import os
from src.layout import create_layout
from src.callbacks import register_callbacks
import pandas as pd
from dash import Dash, dcc
from dash.dependencies import Input, Output


# ---------------------------------------------------------------------------------------------------
# asignacion de variables
print("Iniciando aplicación Dash...")
app = Dash(__name__)
server = app.server
print("App Dash creada.")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Rutas completas seguras
mortality_path = os.path.join(DATA_DIR, "NoFetal2019_8.csv")
divipola_path = os.path.join(DATA_DIR, "Divipola_8.csv")
code_death_path = os.path.join(DATA_DIR, "CodigosDeMuerte_8.csv")

print("📂 Cargando archivos:")
print(f"  ➤ {mortality_path}")
print(f"  ➤ {divipola_path}")
print(f"  ➤ {code_death_path}")

# ---------------------------------------------------------------------------------------------------
# Layout: incluye los dcc.Store para guardar los datos en memoria
app.layout = create_layout(app)

# ---------------------------------------------------------------------------------------------------
# Callback para cargar los datos en los Stores
@app.callback(
    Output('memory-mortality-data', 'data'),
    Output('memory-divipola-data', 'data'),
    Output('memory-code-death-data', 'data'),
    Input('tabs', 'value')  # se puede usar cualquier input para disparar la carga
)
def load_data(_):
    mortality_df = pd.read_csv(mortality_path, sep=';', encoding='utf-8-sig')
    divipola_df = pd.read_csv(divipola_path, sep=';', encoding='utf-8-sig')
    code_death_df = pd.read_csv(code_death_path, sep=';', encoding='utf-8-sig')
    print("Datos cargados y enviados a memoria.")
    return (
        mortality_df.to_dict('records'),
        divipola_df.to_dict('records'),
        code_death_df.to_dict('records'),
    )

# ---------------------------------------------------------------------------------------------------
# Registrar callbacks de la aplicación que usan esos datos desde los Stores
register_callbacks(app)

print("Server exportado.")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run(host='0.0.0.0', port=port, debug=False)
