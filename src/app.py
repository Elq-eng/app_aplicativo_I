# ---------------------------------------------------------------------------------------------------
# librerias
import os
from dash import Dash
from src.layout import create_layout
from src.callbacks import register_callbacks
import psutil
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------------------------------
# asignacion de variables
print("Iniciando aplicación Dash...")
app = Dash(__name__)
print("App Dash creada.")
server = app.server

# ---------------------------------------------------------------------------------------------------
# layout
app.layout = create_layout(app)


# ---------------------------------------------------------------------------------------------------
# callback

register_callbacks(app)

# ---------------------------------------------------------------------------------------------------
# llamado de funcion principal
# Exponer el servidor para Render

print("Server exportado.")

if __name__ == '__main__':
    port =  int(os.environ.get("PORT", 8050))
    app.run(host='0.0.0.0', port=port, debug=False)