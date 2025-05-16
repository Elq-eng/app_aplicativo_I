# ---------------------------------------------------------------------------------------------------
# librerias
import os
from dash import Dash
from src.layout import create_layout
from src.callbacks import register_callbacks

# ---------------------------------------------------------------------------------------------------
# asignacion de variables
print("Iniciando aplicación Dash...")
app = Dash(__name__)
print("App Dash creada.")


# ---------------------------------------------------------------------------------------------------
# layout
app.layout = create_layout(app)

# ---------------------------------------------------------------------------------------------------
# callback
register_callbacks(app)
# ---------------------------------------------------------------------------------------------------
# llamado de funcion principal
# Exponer el servidor para Render
server = app.server
print("Server exportado.")

if __name__ == '__main__':
    port =  int(os.environ.get("PORT", 8050))
    app.run(host='0.0.0.0', port=port, debug=False)