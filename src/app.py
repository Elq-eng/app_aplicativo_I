# ---------------------------------------------------------------------------------------------------
# librerias
import os
from dash import Dash
from src.layout import create_layout
# ---------------------------------------------------------------------------------------------------
# asignacion de variables
print("Iniciando aplicación Dash...")
app = Dash(__name__)
print("App Dash creada.")
# Exponer el servidor para Render
server = app.server
print("Server exportado.")
# ---------------------------------------------------------------------------------------------------
# layout
app.layout = create_layout(app)

# ---------------------------------------------------------------------------------------------------
# callback

# ---------------------------------------------------------------------------------------------------
# llamado de funcion principal
if __name__ == '__main__':
    port =  int(os.environ.get("PORT", 8050))
    app.run(host='0.0.0.0', port=port)